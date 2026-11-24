// Generates images (and image-to-video clips) with LetzAI, billed to the organisation in .env.
// Usage: node tools/letzai.mjs tools/ai-media.json [name ...]
// Reads LETZAI_API_KEY, LETZAI_BASE_URL, LETZAI_ORGANIZATION_ID from .env (never committed).
// Originals land in assets/img-src/ (git-ignored); tools/ai-media.lock.json records job ids + source URLs.
import { readFileSync, writeFileSync, mkdirSync, existsSync } from 'node:fs';
import { dirname, join } from 'node:path';

const root = new URL('..', import.meta.url).pathname;
const env = Object.fromEntries(
  readFileSync(join(root, '.env'), 'utf8').split(/\r?\n/).filter((l) => l.includes('='))
    .map((l) => [l.slice(0, l.indexOf('=')).trim(), l.slice(l.indexOf('=') + 1).trim()]));
const base = env.LETZAI_BASE_URL || 'https://api.letz.ai';
const headers = { Authorization: `Bearer ${env.LETZAI_API_KEY}`, 'Content-Type': 'application/json' };
const [, , specFile, ...only] = process.argv;
const spec = JSON.parse(readFileSync(specFile, 'utf8'));
const outDir = join(root, 'assets/img-src');
mkdirSync(outDir, { recursive: true });
const lockFile = join(root, 'tools/ai-media.lock.json');
const lock = existsSync(lockFile) ? JSON.parse(readFileSync(lockFile, 'utf8')) : {};
const saveLock = () => writeFileSync(lockFile, JSON.stringify(lock, null, 1));
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const want = (n) => (only.length ? only.includes(n) : !lock[n]);

async function poll(kind, id, name) {
  for (let i = 0; i < 300; i++) {
    await sleep(4000);
    const s = await (await fetch(`${base}/${kind}/${id}`, { headers })).json();
    if (s.status === 'ready' || s.status === 'saved') return s;
    if (['failed', 'interrupted', 'not_allowed'].includes(s.status)) throw new Error(`${name}: ${s.status} ${s.statusDetail || ''}`);
  }
  throw new Error(`${name}: timed out (${id})`);
}

async function download(url, file) {
  const buf = Buffer.from(await (await fetch(url)).arrayBuffer());
  writeFileSync(file, buf);
  return file;
}

async function image(img) {
  const body = {
    prompt: `${img.prompt}. ${img.style === false ? '' : spec.style}`.trim(),
    width: img.width, height: img.height, baseModel: spec.imageModel, mode: spec.imageMode,
    hasWatermark: false, hideFromUserProfile: true, organizationId: env.LETZAI_ORGANIZATION_ID,
  };
  const res = await fetch(`${base}/images`, { method: 'POST', headers, body: JSON.stringify(body) });
  const job = await res.json();
  if (!res.ok) throw new Error(`${img.name}: ${res.status} ${JSON.stringify(job)}`);
  const s = await poll('images', job.id, img.name);
  const url = s.imageVersions?.original || Object.values(s.imageVersions || {})[0];
  const ext = (url.split('?')[0].split('.').pop() || 'jpg').toLowerCase();
  await download(url, join(outDir, `${img.name}.${ext}`));
  lock[img.name] = { kind: 'image', id: job.id, url, file: `assets/img-src/${img.name}.${ext}` }; saveLock();
  return `${img.name}: ok`;
}

async function video(v) {
  const src = lock[v.from];
  if (!src) throw new Error(`${v.name}: source image "${v.from}" not generated yet`);
  const body = {
    prompt: v.prompt, imageUrl: src.url, organizationId: env.LETZAI_ORGANIZATION_ID,
    ...(v.width ? { width: v.width, height: v.height } : {}),
    settings: { mode: spec.videoMode, duration: v.duration, resolution: spec.videoResolution },
  };
  const res = await fetch(`${base}/videos`, { method: 'POST', headers, body: JSON.stringify(body) });
  const job = await res.json();
  if (!res.ok) throw new Error(`${v.name}: ${res.status} ${JSON.stringify(job)}`);
  const s = await poll('videos', job.id, v.name);
  const url = s.videoVersions?.original || Object.values(s.videoVersions || {})[0];
  await download(url, join(outDir, `${v.name}.mp4`));
  lock[v.name] = { kind: 'video', id: job.id, url, file: `assets/img-src/${v.name}.mp4` }; saveLock();
  return `${v.name}: ok`;
}

async function edit(ed) {
  const src = lock[ed.from];
  if (!src) throw new Error(`${ed.name}: source image "${ed.from}" not generated yet`);
  const body = {
    mode: 'context', prompt: ed.prompt, imageUrl: src.url, baseModel: spec.imageModel,
    settings: { resolution: '2k', aspect_ratio: ed.aspect || '16:9', model: spec.imageModel },
    organizationId: env.LETZAI_ORGANIZATION_ID, hidePrompt: true,
  };
  const res = await fetch(`${base}/image-edits`, { method: 'POST', headers, body: JSON.stringify(body) });
  const job = await res.json();
  if (!res.ok) throw new Error(`${ed.name}: ${res.status} ${JSON.stringify(job)}`);
  const s = await poll('image-edits', job.id, ed.name);
  const url = s.generatedImageCompletion?.imageVersions?.original || s.imageCompletionChoices?.[0]?.imageVersions?.original;
  if (!url) throw new Error(`${ed.name}: no result url`);
  const ext = (url.split('?')[0].split('.').pop() || 'jpg').toLowerCase();
  await download(url, join(outDir, `${ed.name}.${ext}`));
  lock[ed.name] = { kind: 'image', id: job.id, url, file: `assets/img-src/${ed.name}.${ext}` }; saveLock();
  return `${ed.name}: ok`;
}

const imgs = (spec.images || []).filter((i) => want(i.name));
const results = [];
for (let i = 0; i < imgs.length; i += 3) results.push(...(await Promise.allSettled(imgs.slice(i, i + 3).map(image))));
const eds = (spec.edits || []).filter((x) => want(x.name));
for (let i = 0; i < eds.length; i += 3) results.push(...(await Promise.allSettled(eds.slice(i, i + 3).map(edit))));
for (const v of (spec.videos || []).filter((x) => want(x.name))) results.push(...(await Promise.allSettled([video(v)])));
for (const r of results) console.log(r.status === 'fulfilled' ? r.value : `FAILED ${r.reason.message}`);
if (!results.length) console.log('Nothing to generate.');
