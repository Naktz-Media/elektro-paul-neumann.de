/* Elektro Paul Neumann – Smart Buildings OS · interactions (no dependencies) */
(() => {
  const root = document.documentElement;
  root.classList.add('js');
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const fine = matchMedia('(hover: hover) and (pointer: fine)').matches;
  const clamp = (v, a = 0, b = 1) => Math.min(b, Math.max(a, v));

  /* ---------- header, progress, dock ---------- */
  const header = $('.site-header'), progress = $('.progress'), dock = $('.dock');
  let lastY = scrollY;
  const onScrollUI = () => {
    const y = scrollY, max = document.body.scrollHeight - innerHeight;
    if (progress) progress.style.transform = `scaleX(${max > 0 ? y / max : 0})`;
    if (header) {
      header.classList.toggle('scrolled', y > 40);
      const menuOpen = $('.menu-btn')?.getAttribute('aria-expanded') === 'true';
      header.classList.toggle('hide', !menuOpen && y > 400 && y > lastY + 4);
      if (y < lastY - 4) header.classList.remove('hide');
    }
    if (dock) dock.classList.toggle('hide', y > lastY + 4 && y > 300);
    lastY = y;
  };

  /* ---------- mobile menu ---------- */
  const btn = $('.menu-btn'), menu = $('#mobile-menu');
  if (btn && menu) {
    btn.addEventListener('click', () => {
      const open = btn.getAttribute('aria-expanded') !== 'true';
      btn.setAttribute('aria-expanded', open);
      menu.hidden = !open;
      document.body.style.overflow = open ? 'hidden' : '';
      $$('nav a', menu).forEach((a, i) => { a.style.animationDelay = `${i * 35}ms`; });
    });
  }

  /* ---------- mega menu ---------- */
  $$('.has-mega').forEach((m) => {
    const link = $('.nav-link', m);
    link.addEventListener('click', (ev) => {
      if (!fine && !m.classList.contains('open')) { ev.preventDefault(); m.classList.add('open'); }
    });
    document.addEventListener('click', (ev) => { if (!m.contains(ev.target)) m.classList.remove('open'); });
    m.addEventListener('keydown', (ev) => { if (ev.key === 'Escape') { m.classList.remove('open'); link.focus(); } });
  });

  /* ---------- reveal ---------- */
  const io = 'IntersectionObserver' in window && !reduce ? new IntersectionObserver((entries) => {
    entries.forEach((en) => { if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); } });
  }, { rootMargin: '0px 0px -10% 0px', threshold: 0.06 }) : null;
  $$('.reveal, .reveal-clip, .route-map').forEach((el) => {
    if (!io) { el.classList.add('in'); return; }
    const sib = el.parentElement ? [...el.parentElement.children].filter((c) => c.classList.contains('reveal')) : [];
    const k = sib.indexOf(el);
    if (k > 0) el.style.transitionDelay = `${Math.min(k, 5) * 80}ms`;
    io.observe(el);
  });

  /* ---------- hero rotating word ---------- */
  const swap = $('.swap');
  if (swap && !reduce) {
    const words = $$('span', swap); let i = 0;
    setInterval(() => {
      const cur = words[i]; i = (i + 1) % words.length; const nxt = words[i];
      cur.classList.remove('on'); cur.classList.add('out');
      nxt.classList.remove('out'); nxt.classList.add('on');
      setTimeout(() => cur.classList.remove('out'), 800);
    }, 2600);
  }

  /* ---------- scroll-lit words ---------- */
  const lits = $$('.lit');
  lits.forEach((el) => {
    const words = el.textContent.trim().split(/\s+/);
    el.innerHTML = words.map((w) => `<span class="w">${w}</span> `).join('');
  });

  /* ---------- counters ---------- */
  const counters = $$('[data-count]');
  if (counters.length && 'IntersectionObserver' in window) {
    const cio = new IntersectionObserver((entries) => entries.forEach((en) => {
      if (!en.isIntersecting) return;
      const el = en.target, end = Number(el.dataset.count), from = Number(el.dataset.from || 0);
      cio.unobserve(el);
      if (reduce) { el.textContent = end; return; }
      const t0 = performance.now(), dur = 1600;
      const step = (t) => {
        const p = clamp((t - t0) / dur); const e = 1 - Math.pow(1 - p, 4);
        el.textContent = Math.round(from + (end - from) * e);
        if (p < 1) requestAnimationFrame(step);
      };
      requestAnimationFrame(step);
    }), { threshold: 0.5 });
    counters.forEach((c) => cio.observe(c));
  }

  /* ---------- scene control ---------- */
  const stage = $('.scene-stage');
  if (stage) {
    const imgs = $$('img[data-scene]', stage), btns = $$('.scene-btn'), cap = $('.scene-caption b'), capP = $('.scene-caption span');
    const set = (name) => {
      const b = btns.find((x) => x.dataset.scene === name); if (!b) return;
      btns.forEach((x) => x.setAttribute('aria-pressed', x === b));
      imgs.forEach((im) => im.classList.toggle('on', im.dataset.scene === name));
      const v = JSON.parse(b.dataset.values);
      $$('.meter').forEach((m) => {
        const k = m.dataset.k; const val = v[k];
        $('.meter-bar i', m).style.setProperty('--v', `${k === 'temp' ? ((val - 16) / 10) * 100 : val}%`);
        $('output', m).textContent = k === 'temp' ? `${val}°` : `${val}%`;
      });
      if (cap) { cap.style.opacity = 0; setTimeout(() => { cap.textContent = b.dataset.title; capP.textContent = b.dataset.text; cap.style.opacity = 1; }, 200); }
    };
    btns.forEach((b) => b.addEventListener('click', () => { set(b.dataset.scene); auto = false; }));
    let auto = !reduce, k = 0;
    set(btns[0].dataset.scene);
    const sio = new IntersectionObserver((en) => { stage.dataset.visible = en[0].isIntersecting ? '1' : ''; }, { threshold: 0.4 });
    sio.observe(stage);
    setInterval(() => {
      if (!auto || !stage.dataset.visible) return;
      k = (k + 1) % btns.length; set(btns[k].dataset.scene);
    }, 4200);
  }

  /* ---------- horizontal pinned projects ---------- */
  const hs = $('.hscroll'), track = $('.hscroll-track'), hbar = $('.hbar');
  const sizeH = () => {
    if (!hs || !track) return;
    if (innerWidth <= 980 || reduce) { hs.style.height = ''; track.style.transform = ''; return; }
    const dist = track.scrollWidth - innerWidth;
    hs.style.height = `${dist + innerHeight}px`;
    hs.dataset.dist = dist;
  };
  const moveH = () => {
    if (!hs || !track || innerWidth <= 980 || reduce) return;
    const r = hs.getBoundingClientRect(); const dist = Number(hs.dataset.dist || 0);
    const p = clamp(-r.top / (hs.offsetHeight - innerHeight || 1));
    track.style.transform = `translate3d(${-p * dist}px,0,0)`;
    if (hbar) hbar.style.setProperty('--hp', p);
  };

  /* ---------- scroll-linked effects ---------- */
  const heroes = $$('.hero, .media-hero');
  const steps = $('.steps');
  const onScrollFX = () => {
    heroes.forEach((h) => { const r = h.getBoundingClientRect(); h.style.setProperty('--p', clamp(-r.top / r.height).toFixed(3)); });
    lits.forEach((el) => {
      const r = el.getBoundingClientRect(); const words = $$('.w', el);
      const p = clamp((innerHeight * 0.85 - r.top) / (r.height + innerHeight * 0.45));
      const n = Math.round(p * words.length);
      words.forEach((w, i) => w.classList.toggle('on', i < n));
    });
    if (steps) { const r = steps.getBoundingClientRect(); steps.style.setProperty('--sp', clamp((innerHeight * 0.8 - r.top) / (innerHeight * 0.6)).toFixed(3)); }
    moveH();
  };
  let ticking = false;
  const onScroll = () => {
    if (ticking) return; ticking = true;
    requestAnimationFrame(() => { onScrollUI(); if (!reduce) onScrollFX(); ticking = false; });
  };
  addEventListener('scroll', onScroll, { passive: true });
  addEventListener('resize', () => { sizeH(); onScroll(); });
  sizeH(); onScrollUI(); if (!reduce) onScrollFX(); else $$('.lit .w').forEach((w) => w.classList.add('on'));
  addEventListener('load', () => { sizeH(); onScroll(); });

  /* ---------- project index preview ---------- */
  const prev = $('.pindex-preview');
  if (prev) {
    const rows = $$('.pi-row'), pics = $$('img', prev), capI = $('.pindex-cap .idx', prev), capB = $('.pindex-cap b', prev);
    const act = (i) => {
      rows.forEach((r, k) => r.classList.toggle('on', k === i));
      pics.forEach((p, k) => p.classList.toggle('on', k === i));
      capI.textContent = `${String(i + 1).padStart(2, '0')} / ${rows.length}`; capB.textContent = rows[i].dataset.name;
    };
    rows.forEach((r, i) => { r.addEventListener('pointerenter', () => act(i)); r.addEventListener('focus', () => act(i)); });
    act(0);
  }

  /* ---------- background videos: play only while visible ---------- */
  const vids = $$('video[data-autoplay]');
  if (vids.length && 'IntersectionObserver' in window && !reduce) {
    const vio = new IntersectionObserver((entries) => entries.forEach((en) => {
      if (en.isIntersecting) en.target.play().catch(() => {}); else en.target.pause();
    }), { threshold: 0.2 });
    vids.forEach((v) => vio.observe(v));
  }

  /* ---------- pointer effects (desktop) ---------- */
  if (fine && !reduce) {
    $$('.spot').forEach((c) => c.addEventListener('pointermove', (ev) => {
      const r = c.getBoundingClientRect();
      c.style.setProperty('--mx', `${ev.clientX - r.left}px`); c.style.setProperty('--my', `${ev.clientY - r.top}px`);
    }));
    $$('.magnetic').forEach((b) => {
      b.addEventListener('pointermove', (ev) => {
        const r = b.getBoundingClientRect();
        b.style.transform = `translate(${(ev.clientX - r.left - r.width / 2) * 0.18}px, ${(ev.clientY - r.top - r.height / 2) * 0.28}px)`;
      });
      b.addEventListener('pointerleave', () => { b.style.transform = ''; });
    });
    const ci = $('.cursor-img');
    if (ci) {
      let x = 0, y = 0, tx = 0, ty = 0, raf = 0;
      const loop = () => { x += (tx - x) * 0.16; y += (ty - y) * 0.16; ci.style.left = `${x}px`; ci.style.top = `${y}px`; raf = requestAnimationFrame(loop); };
      $$('.svc-row').forEach((row) => {
        row.addEventListener('pointerenter', (ev) => {
          tx = x = ev.clientX; ty = y = ev.clientY;
          $$('img', ci).forEach((im) => im.classList.toggle('on', im.dataset.for === row.dataset.key));
          ci.classList.add('on'); cancelAnimationFrame(raf); loop();
        });
        row.addEventListener('pointermove', (ev) => { tx = ev.clientX; ty = ev.clientY; });
        row.addEventListener('pointerleave', () => { ci.classList.remove('on'); setTimeout(() => cancelAnimationFrame(raf), 400); });
      });
    }
  }

  /* ---------- chapter scrollspy ---------- */
  const chapLinks = $$('.chapters a[href^="#"]');
  if (chapLinks.length && 'IntersectionObserver' in window) {
    const map = new Map(chapLinks.map((a) => [a.getAttribute('href').slice(1), a]));
    const cio = new IntersectionObserver((entries) => entries.forEach((en) => {
      if (en.isIntersecting) { chapLinks.forEach((a) => a.classList.remove('on')); map.get(en.target.id)?.classList.add('on'); }
    }), { rootMargin: '-40% 0px -55% 0px' });
    map.forEach((_, id) => { const s = document.getElementById(id); if (s) cio.observe(s); });
  }

  /* ---------- project filter ---------- */
  $$('.filter').forEach((f) => f.addEventListener('click', () => {
    $$('.filter').forEach((x) => { x.classList.toggle('is-on', x === f); x.setAttribute('aria-pressed', x === f); });
    const run = () => {
      $$('.pcard').forEach((c) => c.classList.toggle('is-hidden', f.dataset.filter !== 'all' && c.dataset.cat !== f.dataset.filter));
      $('.proj-grid')?.classList.toggle('filtered', f.dataset.filter !== 'all');
    };
    if (document.startViewTransition && !reduce) document.startViewTransition(run); else run();
  }));

  /* ---------- YouTube: load only after consent ---------- */
  const loadYT = (box, autoplay) => {
    box.innerHTML = `<iframe src="https://www.youtube-nocookie.com/embed/${box.dataset.yt}?rel=0${autoplay ? '&autoplay=1' : ''}" title="YouTube video" allow="autoplay; encrypted-media; picture-in-picture; fullscreen" allowfullscreen></iframe>`;
  };
  let ytOk = false;
  try { ytOk = sessionStorage.getItem('yt-consent') === '1'; } catch (e) { /* storage blocked */ }
  $$('.yt').forEach((box) => {
    if (ytOk) { loadYT(box, false); return; }
    $('.yt-btn', box).addEventListener('click', () => {
      try { sessionStorage.setItem('yt-consent', '1'); } catch (e) { /* ignore */ }
      $$('.yt').forEach((b) => loadYT(b, b === box));
    });
  });

  /* ---------- lightbox with thumbnails ---------- */
  const lb = $('.lightbox');
  if (lb) {
    const im = $('figure img', lb), cap = $('figcaption', lb), thumbs = $('.lb-thumbs', lb);
    let group = [], idx = 0, lastFocus = null;
    const show = (i) => {
      idx = (i + group.length) % group.length;
      const a = group[idx];
      im.src = a.getAttribute('href'); im.alt = $('img', a)?.alt || '';
      cap.textContent = `${a.dataset.caption || ''}${group.length > 1 ? `  ·  ${idx + 1} / ${group.length}` : ''}`;
      $$('button', thumbs).forEach((t, k) => t.classList.toggle('on', k === idx));
      $$('button', thumbs)[idx]?.scrollIntoView({ inline: 'center', block: 'nearest', behavior: reduce ? 'auto' : 'smooth' });
      const multi = group.length > 1;
      $('.lb-prev', lb).hidden = !multi; $('.lb-next', lb).hidden = !multi; thumbs.hidden = !multi;
      if (multi) { const n = new Image(); n.src = group[(idx + 1) % group.length].getAttribute('href'); }
    };
    const open = (a) => {
      group = $$(`[data-lightbox="${a.dataset.lightbox}"]`);
      thumbs.innerHTML = group.map((g, k) => `<button type="button" aria-label="Photo ${k + 1}"><img src="${$('img', g)?.currentSrc || $('img', g)?.src || ''}" alt=""></button>`).join('');
      $$('button', thumbs).forEach((t, k) => t.addEventListener('click', () => show(k)));
      lastFocus = document.activeElement;
      lb.hidden = false; document.body.style.overflow = 'hidden';
      show(group.indexOf(a)); $('.lb-close', lb).focus();
    };
    const close = () => { lb.hidden = true; im.src = ''; document.body.style.overflow = ''; lastFocus?.focus(); };
    document.addEventListener('click', (ev) => { const a = ev.target.closest('[data-lightbox]'); if (a) { ev.preventDefault(); open(a); } });
    $('.lb-close', lb).addEventListener('click', close);
    $('.lb-prev', lb).addEventListener('click', () => show(idx - 1));
    $('.lb-next', lb).addEventListener('click', () => show(idx + 1));
    $('figure', lb).addEventListener('click', (ev) => { if (ev.target.tagName !== 'IMG') close(); });
    document.addEventListener('keydown', (ev) => {
      if (lb.hidden) return;
      if (ev.key === 'Escape') close();
      if (ev.key === 'ArrowLeft') show(idx - 1);
      if (ev.key === 'ArrowRight') show(idx + 1);
    });
    let x0 = null;
    lb.addEventListener('touchstart', (ev) => { x0 = ev.touches[0].clientX; }, { passive: true });
    lb.addEventListener('touchend', (ev) => {
      if (x0 === null) return; const dx = ev.changedTouches[0].clientX - x0;
      if (Math.abs(dx) > 50) show(idx + (dx < 0 ? 1 : -1)); x0 = null;
    });
  }
})();
