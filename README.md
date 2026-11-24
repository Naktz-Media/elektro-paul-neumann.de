# elektro-paul-neumann.de

New website for **Elektro Paul Neumann – Paul Neumann Smart Buildings**, electrical, KNX and security technology in Cologne and on Mallorca (since 1980).

Static site, no framework and no third-party requests: fonts (Montserrat), images and videos are hosted locally. YouTube videos load only after the visitor clicks (privacy-enhanced mode). English content, taken from the current en.elektro-paul-neumann.de (crawled 24 Nov 2026).

## Pages

| Page | File |
|---|---|
| Home | `index.html` |
| Services overview + 8 service pages | `services.html`, `services/*.html` |
| Projects overview + 14 project pages with photo galleries | `projects.html`, `projects/*.html` |
| Careers | `careers.html` |
| Contact | `contact.html` |
| Imprint & privacy policy | `imprint.html` |

## Editing

All pages are generated – do not edit the HTML by hand.

```
python tools/build.py
```

- `tools/source-en.json` – all texts, FAQ, video IDs and image references, extracted from the old site (`tools/extract.py`)
- `tools/build.py` – page templates, service/project order, names and the few copy overrides
- `tools/images.json` – image key → local file (large + small)
- `assets/css/site.css`, `assets/js/site.js` – design and interactions (menu, reveal, gallery lightbox, YouTube consent, project filter)

Re-download the original photos: `python tools/fetch_images.py`.

## AI images and video (LetzAI)

The home hero (image + 5 s background video), the KNX page hero and the eight service tiles are generated with LetzAI (Seedream 5.5 for images, MiniMax H3 Max 768p for the video), billed to the Evai organisation.

```
NODE_USE_ENV_PROXY=1 node tools/letzai.mjs tools/ai-media.json [name ...]
python tools/ai_to_web.py
python tools/build.py
```

Prompts are in `tools/ai-media.json`. The script reads `LETZAI_API_KEY` and `LETZAI_ORGANIZATION_ID` from `.env` (not in the repo). Originals go to `assets/img-src/` (ignored), web versions to `assets/img/ai/`.

## View locally

```
python -m http.server 5180
```

then open http://localhost:5180.

## To clarify before launch

- German (and Spanish) versions – the old site had DE / EN / ES
- The second Cologne number (+49 221 431 352) is unlabelled on the old site – fax?
- Imprint: check legal form, chamber (Handwerkskammer) and professional title; privacy policy needs updating to the new hosting
- Project texts are short (Wilma Wunder has none) – longer case studies would help
