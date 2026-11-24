"""Generate every HTML page of the site from tools/source-en.json + tools/images.json.

    python tools/build.py

Edit content in the JSON (or the overrides below), never in the generated HTML.
"""
import html, json, os, re

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = json.load(open(f"{R}/tools/source-en.json", encoding="utf-8"))
IMG = json.load(open(f"{R}/tools/images.json", encoding="utf-8"))

PHONE, PHONE_HREF = "+49 (0) 221 - 431 351", "tel:+49221431351"
PHONE2, PHONE2_HREF = "+49 (0) 221 - 431 352", "tel:+49221431352"
MAIL = "info@elektro-paul-neumann.de"
MAPS = "https://maps.app.goo.gl/d2gkWFqJvXmDB9e87"

# ---------------------------------------------------------------- content config
SERVICES = [  # old slug, new slug, short name, tagline, icon
    ("beleuchtungssysteme", "lighting-systems", "Lighting systems", "Lighting design at the highest level", "light"),
    ("knx-systemintegrator", "knx-system-integration", "KNX system integration", "Intelligent building technology with high standards", "knx"),
    ("alarmanlagen", "alarm-systems", "Alarm systems", "Your protection starts with the right alarm system", "alarm"),
    ("smart_home", "smart-home", "Smart Home", "Comfort, security and efficiency – controlled from anywhere", "home"),
    ("videoueberwachung", "video-surveillance", "Video surveillance", "Your protection starts with a clear picture", "camera"),
    ("video_gegensprechanlagen", "video-intercoms", "Video intercom systems", "More safety through visual control", "intercom"),
    ("multiroom_audio", "multiroom-audio", "Multi-room audio", "Sound comfort in every room", "audio"),
    ("service_elektriker", "electrical-service", "Electrical service", "Tailor-made electrical support for every project", "service"),
]
# old slug -> (new slug, display name, subtitle, category)
PROJECTS = {
    "villa_xxl": ("villa-xxl-mallorca", "Villa XXL Mallorca", "Exclusive villa · 2017 – 2020", "Residential"),
    "penthouse_xxl": ("penthouse-xxl", "Penthouse XXL", "Cologne · 2017 – 2018", "Residential"),
    "townhouse": ("townhouse", "Townhouse", "Cologne · 2017 – 2018", "Residential"),
    "bayer04_leverkusen": ("bayer-04-leverkusen", "Bayer 04 Leverkusen", "Fußball GmbH · 2013 – 2015", "Commercial"),
    "tuev_rheinland": ("tuev-rheinland", "TÜV Rheinland", "Office renovation", "Commercial"),
    "wdr_studios_koeln": ("wdr-studios-koeln", "WDR Studios Köln", "KNX building technology", "Commercial"),
    "stroeer_media_se": ("stroeer-media-se", "Ströer Media SE", "Office & building technology", "Commercial"),
    "hotel_im_wasserturm": ("hotel-im-wasserturm", "Hotel im Wasserturm", "Cologne · 2015", "Commercial"),
    "gerling_ring_karree": ("gerling-ring-karree", "Gerling Ring Karree", "Cologne", "Commercial"),
    "hitschler_international": ("hitschler-international", "Hitschler International GmbH & Co. KG", "Cologne", "Commercial"),
    "rheinland_versicherung": ("rheinland-versicherung", "Rheinland Versicherung", "Cologne", "Commercial"),
    "kluck_umweltlogistik": ("kluck-umweltlogistik", "Kluck Umweltlogistik", "Cologne, Pulheim", "Commercial"),
    "leuchtenzentrum": ("leuchtenzentrum", "Leuchtenzentrum", "Leverkusen", "Commercial"),
    "wilma_wunder": ("wilma-wunder", "Wilma Wunder", "Cologne", "Commercial"),
}
BRANDS = ["Telenot", "Vanderbilt", "Indexa", "ABUS", "Axis", "Avigilon", "Geutebrück", "Mobotix", "CBC"]

# ---------------------------------------------------------------- helpers
e = html.escape


TILE = {"beleuchtungssysteme": "lighting", "knx-systemintegrator": "knx", "alarmanlagen": "alarm", "smart_home": "smarthome",
        "videoueberwachung": "video", "video_gegensprechanlagen": "intercom", "multiroom_audio": "audio", "service_elektriker": "service"}


def tile_key(old):
    k = f"ai/tile-{TILE[old]}"
    return k if k in IMG else f"services/{old}/card"


def img(key, size="l"):
    v = IMG.get(key)
    return v[size] if v and v.get(size) else None


def tidy(h):
    """Clean the html that came out of the old CMS."""
    h = re.sub(r"(\s*<br>\s*)+(?=<(p|ul|ol|/))", "", h)
    h = re.sub(r"^(\s*<br>\s*)+|(\s*<br>\s*)+$", "", h)
    h = h.replace("<p></p>", "").replace("<p> </p>", "")
    h = re.sub(r"(\S)<(strong|a)\b", r"\1 <\2", h)          # space before inline tags
    h = re.sub(r"</(strong|a)>(?=[\w(€0-9])", r"</\1> ", h)  # space after inline tags
    h = re.sub(r"(\s*<br>\s*){2,}", "<br>", h)
    h = h.replace("<p> ", "<p>").replace(" </p>", "</p>")
    # list items made of "<strong>Title</strong><br>text" become feature cards
    def feat(m):
        items = re.findall(r"<li>(.*?)</li>", m.group(1), re.S)
        if items and all(re.match(r"\s*(<p>)?\s*<strong>[^<]+</strong>\s*<br>", i) for i in items):
            cards = []
            for i in items:
                t, rest = re.match(r"\s*(?:<p>)?\s*<strong>([^<]+)</strong>\s*<br>(.*?)(?:</p>)?\s*$", i, re.S).groups()
                cards.append(f'<li class="feature"><h4>{t.strip()}</h4><p>{rest.strip()}</p></li>')
            return '<ul class="features">' + "".join(cards) + "</ul>"
        return '<ul class="checks">' + m.group(1) + "</ul>"
    h = re.sub(r"<ul>(.*?)</ul>", feat, h, flags=re.S)
    h = re.sub(r"<li><p>(.*?)</p></li>", r"<li>\1</li>", h, flags=re.S)
    return h.strip()


def text(h):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", h)).strip()


ICONS = {
    "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "chev": '<path d="M9 6l6 6-6 6"/>',
    "down": '<path d="M6 9l6 6 6-6"/>',
    "phone": '<path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2"/>',
    "mail": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/>',
    "pin": '<path d="M12 21s-7-6.2-7-11.5A7 7 0 0 1 19 9.5C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/>',
    "play": '<path d="M8 5v14l11-7z" fill="currentColor" stroke="none"/>',
    "close": '<path d="M6 6l12 12M18 6L6 18"/>',
    "left": '<path d="M15 6l-6 6 6 6"/>',
    "check": '<path d="M5 12.5l4.5 4.5L19 7.5"/>',
    "plus": '<path d="M12 5v14M5 12h14"/>',
    "grid": '<rect x="4" y="4" width="7" height="7" rx="1.5"/><rect x="13" y="4" width="7" height="7" rx="1.5"/><rect x="4" y="13" width="7" height="7" rx="1.5"/><rect x="13" y="13" width="7" height="7" rx="1.5"/>',
    "light": '<path d="M9 18h6M10 21h4M12 3a6 6 0 0 0-3.5 10.9c.6.5 1 1.2 1 2.1h5c0-.9.4-1.6 1-2.1A6 6 0 0 0 12 3z"/>',
    "knx": '<circle cx="12" cy="12" r="2.5"/><circle cx="4.5" cy="5" r="1.8"/><circle cx="19.5" cy="5" r="1.8"/><circle cx="4.5" cy="19" r="1.8"/><circle cx="19.5" cy="19" r="1.8"/><path d="M6 6.3l4.2 4.1M18 6.3l-4.2 4.1M6 17.7l4.2-4.1M18 17.7l-4.2-4.1"/>',
    "alarm": '<path d="M12 3l7.5 3v5.5c0 4.6-3.2 8.3-7.5 9.5-4.3-1.2-7.5-4.9-7.5-9.5V6z"/><path d="M12 8.5v4M12 15.5v.5"/>',
    "home": '<path d="M3.5 11L12 4l8.5 7"/><path d="M6 9.5V20h12V9.5"/><path d="M10 15.5a2.8 2.8 0 0 1 4 0M8.6 13.4a4.8 4.8 0 0 1 6.8 0"/>',
    "camera": '<path d="M3 7.5l13-3.5 1.5 5.5-13 3.5z"/><path d="M17 8.3l3.5-1v5l-3-.2M8 12.2L9.5 17H5"/>',
    "intercom": '<rect x="6" y="2.5" width="12" height="19" rx="2.5"/><circle cx="12" cy="8" r="2.5"/><path d="M9.5 14h5M9.5 17h5"/>',
    "audio": '<rect x="5" y="2.5" width="14" height="19" rx="2.5"/><circle cx="12" cy="14.5" r="3.5"/><circle cx="12" cy="7" r="1.5"/>',
    "service": '<path d="M14.5 6.5a4 4 0 0 0-5.3 5.3L4 17l3 3 5.2-5.2a4 4 0 0 0 5.3-5.3l-2.5 2.5-2.3-.7-.7-2.3z"/>',
}


def icon(name, cls="i"):
    return f'<svg class="{cls}" viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">{ICONS[name]}</svg>'


def picture(key, alt, pre, cls="", sizes="100vw", eager=False):
    l, s = img(key), img(key, "s")
    if not l:
        return ""
    srcset = f' srcset="{pre}{s} 640w, {pre}{l} 1600w" sizes="{sizes}"' if s and s != l else ""
    load = 'fetchpriority="high"' if eager else 'loading="lazy"'
    return f'<img class="{cls}" src="{pre}{l}"{srcset} alt="{e(alt)}" {load} decoding="async">'


def eyebrow(t, cls=""):
    return f'<p class="eyebrow {cls}">{e(t)}</p>' if t else ""


def yt(vid, title):
    return (f'<div class="yt" data-yt="{vid}"><button type="button" class="yt-btn" aria-label="Play video: {e(title)}">'
            f'<span class="yt-play">{icon("play")}</span><span class="yt-note">To protect your data, the YouTube video only loads after you click. '
            f'By playing it you agree to a connection to YouTube (privacy-enhanced mode).</span></button></div>')


ICONS.update({
    "upright": '<path d="M7 17L17 7M8 7h9v9"/>',
    "sun": '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/>',
    "sunset": '<path d="M17 18a5 5 0 0 0-10 0M12 2v7M4.2 10.2l1.4 1.4M1 18h2M21 18h2M18.4 11.6l1.4-1.4M23 22H1M8 6l4-4 4 4"/>',
    "film": '<rect x="3" y="4" width="18" height="16" rx="2"/><path d="M7 4v16M17 4v16M3 9h4M3 15h4M17 9h4M17 15h4"/>',
    "shield": '<path d="M12 3l7.5 3v5.5c0 4.6-3.2 8.3-7.5 9.5-4.3-1.2-7.5-4.9-7.5-9.5V6z"/><path d="M9 12l2 2 4-4"/>',
    "blinds": '<path d="M4 4h16M5 4v9M19 4v9M5 7h14M5 10h14M5 13h14M12 13v6"/><circle cx="12" cy="20" r="1"/>',
    "thermo": '<path d="M14 14.8V5a2 2 0 0 0-4 0v9.8a4 4 0 1 0 4 0z"/><path d="M12 9v7"/>',
    "wave": '<path d="M3 12h2l2-6 3 12 3-9 2 5 2-2h4"/>',
})

# ---------------------------------------------------------------- layout
NAV = [("index.html", "Home"), ("services.html", "Services"), ("services/knx-system-integration.html", "KNX"),
       ("projects.html", "Projects"), ("careers.html", "Careers"), ("contact.html", "Contact")]


def header(pre, active):
    links = []
    for href, label in NAV:
        cur = ' aria-current="page"' if active == label else ""
        if label == "Services":
            items = "".join(
                f'<a class="mega-item" href="{pre}services/{s}.html">{picture(tile_key(o), "", pre, "mega-thumb", "46px")}<span><b>{e(n)}</b><small>{e(t)}</small></span></a>'
                for o, s, n, t, ic in SERVICES)
            links.append(
                f'<div class="has-mega"><a href="{pre}{href}"{cur} class="nav-link">Services {icon("down", "i caret")}</a>'
                f'<div class="mega"><div class="mega-inner"><div class="mega-grid">{items}</div>'
                f'<a class="mega-feature" href="{pre}projects.html">{picture("projects/villa_xxl/cover", "", pre, "", "260px")}<b>14 reference projects</b><small>From villas on Mallorca to stadiums and studios →</small></a></div></div></div>')
        elif label != "Home":
            links.append(f'<a href="{pre}{href}"{cur} class="nav-link">{label}</a>')
    mob = "".join(f'<a href="{pre}{h}">{l}{icon("upright")}</a>' for h, l in NAV)
    mob_s = "".join(f'<a class="sub" href="{pre}services/{s}.html">{e(n)}</a>' for _, s, n, _, _ in SERVICES)
    return f'''<a class="skip" href="#main">Skip to content</a>
<div class="progress" aria-hidden="true"></div>
<header class="site-header" id="top">
  <div class="bar">
    <a class="brand" href="{pre}index.html" aria-label="Elektro Paul Neumann – Smart Buildings, home"><img src="{pre}assets/brand/logo.svg" alt="Paul Neumann Smart Buildings" width="172" height="34"></a>
    <nav class="nav" aria-label="Main">{"".join(links)}</nav>
    <div class="bar-cta">
      <a class="phone-link" href="{PHONE_HREF}" aria-label="Call {PHONE}">{icon("phone")}</a>
      <a class="btn btn-light btn-sm magnetic" href="{pre}contact.html">Let’s talk {icon("arrow")}</a>
      <button class="menu-btn" type="button" aria-expanded="false" aria-controls="mobile-menu"><span></span><span></span><span class="sr">Menu</span></button>
    </div>
  </div>
</header>
<div class="mobile-menu" id="mobile-menu" hidden>
  <nav aria-label="Mobile">{mob}<p class="mm-label">Services</p>{mob_s}</nav>
</div>'''


def footer(pre):
    svc = "".join(f'<li><a href="{pre}services/{s}.html">{e(n)}</a></li>' for _, s, n, _, _ in SERVICES)
    return f'''<footer class="site-footer">
  <div class="wrap">
    <div class="foot-grid">
      <div class="foot-intro"><img src="{pre}assets/brand/logo.svg" alt="Paul Neumann Smart Buildings" width="210" height="42" loading="lazy">
        <p>Electrical, KNX and security technology in Cologne and on Mallorca. Planning, installation and maintenance – since 1980.</p>
        <a class="btn btn-glass btn-sm" href="{pre}contact.html">Request consultation {icon("arrow")}</a></div>
      <div><h3>Services</h3><ul>{svc}</ul></div>
      <div><h3>Cologne</h3><address><a href="{MAPS}" rel="noopener">Emil-Hoffmann-Straße 39-43<br>Halle 1 + 2<br>50996 Köln</a><br><br><a href="{PHONE_HREF}">{PHONE}</a><br><a href="{PHONE2_HREF}">{PHONE2}</a><br><a href="mailto:{MAIL}">{MAIL}</a></address></div>
      <div><h3>Mallorca</h3><address>Avinguda del Rei Jaume I, 109<br>07180 Santa Ponça<br>Illes Balears, Spain<br><br><a href="{PHONE_HREF}">{PHONE}</a></address>
        <h3 style="margin-top:34px">Company</h3><ul><li><a href="{pre}projects.html">Projects</a></li><li><a href="{pre}careers.html">Careers</a></li><li><a href="{pre}imprint.html">Imprint &amp; privacy</a></li></ul></div>
    </div>
    <div class="foot-word" aria-hidden="true">Smart Buildings</div>
    <div class="foot-bottom"><span>© Elektro Paul Neumann · Dirk Woronow · Since 1980</span><span><a href="{pre}imprint.html">Imprint</a> · <a href="{pre}imprint.html#privacy">Privacy</a> · <a href="#top">Back to top ↑</a></span></div>
  </div>
</footer>
<nav class="dock" aria-label="Quick contact">
  <a href="{PHONE_HREF}">{icon("phone")}Call</a><a href="mailto:{MAIL}">{icon("mail")}Email</a><a href="{pre}contact.html">{icon("arrow")}Contact</a>
</nav>'''


JSONLD = {
    "@context": "https://schema.org", "@type": "Electrician", "name": "Elektro Paul Neumann",
    "alternateName": "Paul Neumann Smart Buildings", "url": "https://elektro-paul-neumann.de/",
    "email": MAIL, "telephone": "+49221431351", "foundingDate": "1980",
    "areaServed": ["Köln", "Deutschland", "Mallorca"],
    "address": {"@type": "PostalAddress", "streetAddress": "Emil-Hoffmann-Straße 39-43, Halle 1 + 2",
                "postalCode": "50996", "addressLocality": "Köln", "addressCountry": "DE"},
    "department": [{"@type": "Electrician", "name": "Elektro Paul Neumann – Mallorca",
                    "address": {"@type": "PostalAddress", "streetAddress": "Avinguda del Rei Jaume I, 109",
                                "postalCode": "07180", "addressLocality": "Santa Ponça", "addressRegion": "Illes Balears", "addressCountry": "ES"}}],
}


def page(path, title, desc, body, active="", extra_head=""):
    pre = "../" * path.count("/")
    og = img("ai/hero-home") or img("home/hero")
    doc = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta name="theme-color" content="#0e0e0f">
<meta name="color-scheme" content="dark">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:image" content="{pre}{og}">
<link rel="icon" href="{pre}assets/brand/icon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="{pre}assets/brand/touchIcon180.png">
<link rel="preload" href="{pre}assets/fonts/montserrat-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{pre}assets/css/site.css">
{extra_head}</head>
<body>
{header(pre, active)}
<main id="main">
{body}
</main>
{footer(pre)}
<div class="lightbox" hidden role="dialog" aria-modal="true" aria-label="Image viewer">
  <button class="lb-close" type="button" aria-label="Close">{icon("close")}</button>
  <button class="lb-prev" type="button" aria-label="Previous image">{icon("left")}</button>
  <figure><img alt=""><figcaption></figcaption></figure>
  <div class="lb-thumbs"></div>
  <button class="lb-next" type="button" aria-label="Next image">{icon("chev")}</button>
</div>
<script src="{pre}assets/js/site.js" defer></script>
</body>
</html>
'''
    out = f"{R}/{path}"
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, "w", encoding="utf-8").write(doc)


def cta(pre, title="Let’s talk.", sub="From the first consultation to the final installation – in Cologne, throughout Germany and on Mallorca."):
    return f'''<section class="cta center">
  <div class="wrap">
    <p class="eyebrow reveal">Get in touch</p>
    <h2 class="cta-title metal reveal">{e(title)}</h2>
    <p class="lead reveal">{e(sub)}</p>
    <div class="cta-contacts reveal"><a class="btn btn-light magnetic" href="{PHONE_HREF}">{icon("phone")} {PHONE}</a><a class="btn btn-glass magnetic" href="mailto:{MAIL}">{icon("mail")} {MAIL}</a></div>
  </div>
</section>'''


def media_hero(key, alt, pre):
    return f'<div class="hero-media">{picture(key, alt, pre, "", "100vw", eager=True)}</div>'


def marquee(items, big=False):
    row = "".join(f"<span>{e(x)}</span>" for x in items)
    return f'<div class="marquee{" big" if big else ""}" aria-hidden="true"><div class="marquee-track">{row}{row}</div></div>'


# ---------------------------------------------------------------- home
SCENES = [
    ("day", "Day", "sun", "Daylight mode", "Blinds open, lights off – the building uses the sun.", {"light": 0, "blinds": 100, "audio": 20, "temp": 21}),
    ("evening", "Evening", "sunset", "Evening scene", "Warm light at 60 %, blinds half down, music on low.", {"light": 60, "blinds": 50, "audio": 35, "temp": 22}),
    ("cinema", "Cinema", "film", "Cinema scene", "Blinds closed, accent light only, sound up.", {"light": 8, "blinds": 0, "audio": 70, "temp": 21}),
    ("away", "Away", "shield", "Away mode", "Everything off, heating lowered, alarm armed.", {"light": 0, "blinds": 100, "audio": 0, "temp": 17}),
]


def scene_section(pre):
    if not all(f"ai/scene-{k}" in IMG for k, *_ in SCENES):
        return ""
    imgs = "".join(f'<img data-scene="{k}" class="{"on" if i == 0 else ""}" src="{pre}{img(f"ai/scene-{k}")}" alt="Living room – {e(label)} scene" loading="lazy" decoding="async">' for i, (k, label, *_r) in enumerate(SCENES))
    btns = "".join(
        f'<button type="button" class="scene-btn" data-scene="{k}" data-title="{e(t)}" data-text="{e(tx)}" data-values=\'{json.dumps(v)}\' aria-pressed="{"true" if i == 0 else "false"}">{icon(ic)}{e(label)}</button>'
        for i, (k, label, ic, t, tx, v) in enumerate(SCENES))
    meters = "".join(f'<div class="meter" data-k="{k}">{icon(ic)}<span class="meter-bar"><i></i></span><output>–</output><span class="sr">{lbl}</span></div>'
                     for k, ic, lbl in (("light", "light", "Light"), ("blinds", "blinds", "Blinds open"), ("audio", "wave", "Audio"), ("temp", "thermo", "Temperature")))
    return f'''<section class="scene" id="scenes">
  <div class="wrap">
    <div class="sec-head row reveal"><div><p class="eyebrow">KNX building automation</p><h2 class="h2">One touch.<br><span class="metal">Every system.</span></h2></div>
      <p class="lead" style="max-width:460px;margin:0">Light, heating, blinds, ventilation and security – centrally controlled, automated and adapted to your life. Try it: tap a scene.</p></div>
    <div class="scene-stage reveal-clip">
      {imgs}
      <div class="scene-caption" aria-live="polite"><b>Daylight mode</b><span>Blinds open, lights off – the building uses the sun.</span></div>
      <div class="panel-ui">
        <div class="panel-top"><b>Living room</b><span class="live">Live demo</span></div>
        <div class="scenes" role="group" aria-label="Lighting scenes">{btns}</div>
        <div class="meters">{meters}</div>
      </div>
    </div>
    <ul class="scene-features">
      <li class="reveal">{icon("light")}<b>Lighting</b><span>Scenes, schedules and presence control</span></li>
      <li class="reveal">{icon("blinds")}<b>Shading</b><span>Blinds and shutters that follow the sun</span></li>
      <li class="reveal">{icon("thermo")}<b>Climate</b><span>Room-by-room heating for real savings</span></li>
      <li class="reveal">{icon("shield")}<b>Security</b><span>Alarm, video and status messages on your phone</span></li>
    </ul>
  </div>
</section>'''


def hero_video(pre):
    if os.path.exists(f"{R}/assets/img/ai/hero-home-video.mp4") and "ai/hero-home" in IMG:
        return (f'<div class="hero-media"><video autoplay muted loop playsinline preload="metadata" poster="{pre}{img("ai/hero-home")}" aria-hidden="true">'
                f'<source src="{pre}assets/img/ai/hero-home-video.mp4" type="video/mp4"></video></div>')
    return media_hero("ai/hero-home" if "ai/hero-home" in IMG else "home/hero", "Modern villa at blue hour", pre)


def build_home():
    pre = ""
    tiles = []
    for i, (old, new, name, tag, ic) in enumerate(SERVICES):
        tiles.append(f'''<a class="tile spot reveal" href="services/{new}.html">
  {picture(tile_key(old), name, pre, "tile-img", "(max-width: 760px) 100vw, 50vw")}
  <span class="tile-top"><span class="idx">{i + 1:02d}</span><span class="tile-arrow">{icon("upright")}</span></span>
  <span><b>{e(name)}</b><small>{e(tag)}</small></span>
</a>''')
    order = ["villa_xxl", "penthouse_xxl", "bayer04_leverkusen", "wdr_studios_koeln", "hotel_im_wasserturm", "townhouse", "stroeer_media_se", "tuev_rheinland", "gerling_ring_karree"]
    hcards = "".join(f'''<a class="hcard" href="projects/{PROJECTS[k][0]}.html">{picture(f"projects/{k}/cover", PROJECTS[k][1], pre, "", "(max-width: 980px) 76vw, 34vw")}
<span class="hcard-body"><span class="idx">{i + 1:02d} — {PROJECTS[k][3]}</span><b>{e(PROJECTS[k][1])}</b><small>{e(PROJECTS[k][2])}</small></span></a>''' for i, k in enumerate(order))
    body = f'''
<section class="hero">
  {hero_video(pre)}
  <div class="wrap hero-content">
    <p class="eyebrow">Paul Neumann Smart Buildings · Cologne &amp; Mallorca</p>
    <h1 class="hero-title" aria-label="Intelligent building technology. Perfectly planned. Precisely implemented.">
      <span class="line" aria-hidden="true"><span><span class="swap"><span class="on">Intelligent</span><span>Secure</span><span>Connected</span><span>Efficient</span></span></span></span>
      <span class="line" aria-hidden="true"><span class="metal">building</span></span>
      <span class="line" aria-hidden="true"><span class="metal">technology.</span></span>
    </h1>
    <div class="hero-sub">
      <p class="lead">Perfectly planned. Precisely implemented. Your partner for electrical installations, smart home, KNX building automation, lighting and security technology – since 1980.</p>
      <div class="actions"><a class="btn btn-light magnetic" href="services.html">Explore services {icon("arrow")}</a><a class="btn btn-glass magnetic" href="#scenes">{icon("play")} Try a scene</a></div>
    </div>
  </div>
  {marquee([n for _, _, n, _, _ in SERVICES])}
</section>

<section class="statement center">
  <div class="wrap narrow">
    <p class="eyebrow reveal">Your partner for</p>
    <p class="lit">Smart solutions for electrical and security technology in Cologne and Mallorca – for high-quality residential and commercial projects, from planning to installation.</p>
    <p class="lead reveal">KNX system integration, smart home, lighting, alarm and video surveillance, and multi-room audio. Since 1980.</p>
  </div>
</section>

{scene_section(pre)}

<section id="services">
  <div class="wrap">
    <div class="sec-head row reveal"><div><p class="eyebrow">Our services</p><h2 class="h2">Every project<br>is unique.</h2></div>
      <a class="btn btn-glass magnetic" href="services.html">All services {icon("arrow")}</a></div>
    <div class="bento">{"".join(tiles)}</div>
  </div>
</section>

<section style="padding-top:0">
  <div class="wrap">
    <ul class="counters reveal">
      <li><b data-count="1980" data-from="1900">1980</b><span>Electricians in Cologne since</span></li>
      <li><b data-count="{len(PROJECTS)}">{len(PROJECTS)}</b><span>Reference projects – villas, stadiums, studios</span></li>
      <li><b data-count="{len(SERVICES)}">{len(SERVICES)}</b><span>Disciplines from a single source</span></li>
      <li><b data-count="2">2</b><span>Locations with own teams – Cologne &amp; Mallorca</span></li>
    </ul>
  </div>
</section>

<section class="hscroll" aria-label="Featured projects">
  <div class="hscroll-pin">
    <div class="wrap hscroll-head reveal"><div><p class="eyebrow">Projects</p><h2 class="h2">Work we’re proud of.</h2></div>
      <a class="btn btn-glass magnetic" href="projects.html">All {len(PROJECTS)} projects {icon("arrow")}</a></div>
    <div class="hscroll-track">{hcards}
      <a class="hcard-end" href="projects.html"><span class="idx">+{len(PROJECTS) - len(order)} more</span><b>Explore all projects</b><span class="round">{icon("arrow")}</span></a>
    </div>
    <div class="wrap"><div class="hbar"><i></i></div></div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="split">
      <div class="reveal-clip" style="border-radius:28px;overflow:hidden">{picture("home/security", "Woman using a wall-mounted smart building touch panel", pre, "", "(max-width: 980px) 100vw, 55vw")}</div>
      <div class="reveal"><p class="eyebrow">Tailor-made solutions – from experts in Cologne</p>
        <h2 class="h2" style="font-size:clamp(32px,4vw,56px)">Security technology for the highest demands.</h2>
        <p class="lead" style="margin-top:24px">Since 1980, we have been offering customized security solutions for your home and industry. From smart home installations to alarm systems – everything from a single source.</p>
        <p class="muted">With high-quality branded products and personal service, we accompany you from the initial consultation to the final installation – whether in your city apartment, holiday home or business.</p>
        <a class="link-more" href="services/alarm-systems.html">Alarm systems {icon("arrow")}</a></div>
    </div>
  </div>
</section>

<section class="light">
  <div class="wrap">
    <div class="sec-head reveal"><p class="eyebrow">How we work</p><h2 class="h2">Idea. Conception.<br>Implementation.</h2></div>
    <ol class="steps">
      <li class="reveal"><span class="idx">01 — Idea</span><h3>We listen.</h3><p>We look at your property on site and understand what you want to achieve.</p></li>
      <li class="reveal"><span class="idx">02 — Conception</span><h3>We plan.</h3><p>System design and a binding quote with a detailed description of the work.</p></li>
      <li class="reveal"><span class="idx">03 — Implementation</span><h3>We deliver.</h3><p>Professional installation, commissioning, handover – and long-term service.</p></li>
    </ol>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="sec-head row reveal"><div><p class="eyebrow">For you</p><h2 class="h2">Two locations.<br><span class="metal">Two teams.</span></h2></div>
      <p class="lead" style="max-width:440px;margin:0">Due to many successful projects in industry and private homes, inquiries from Mallorca followed – today we serve both with our own teams.</p></div>
    <div class="route">
      <article class="loc reveal">
        <video muted loop playsinline preload="none" poster="assets/video/cologne2.webp" data-autoplay aria-hidden="true"><source src="assets/video/cologne2.mp4" type="video/mp4"></video>
        <span class="coords">50.94° N · 6.96° E</span>
        <span class="since">Since 1980</span>
        <h3>Cologne</h3>
        <p>Sophisticated electrical and security technology in the city and the surrounding area – specializing in planning, KNX integration and excellent execution. Managed since 2010 by master electrician Dirk Woronow.</p>
      </article>
      <article class="loc reveal">
        <video muted loop playsinline preload="none" poster="assets/video/palma2.webp" data-autoplay aria-hidden="true"><source src="assets/video/palma2.mp4" type="video/mp4"></video>
        <span class="coords">39.51° N · 2.47° E</span>
        <span class="since">Since 2017</span>
        <h3>Mallorca</h3>
        <p>Active on the island since 2017, with our own office and team since 2022: KNX planning and integration, smart home, video, alarm, multi-room audio and media systems.</p>
      </article>
    </div>
    <div class="route-map" aria-label="Route between Cologne and Mallorca, about 1,320 kilometres">
      <svg viewBox="0 0 1000 220" role="img" aria-hidden="true">
        <defs><pattern id="dots" width="16" height="16" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1.2" class="grid-dots"/></pattern></defs>
        <rect width="1000" height="220" fill="url(#dots)"/>
        <path class="arc" d="M120 170 C 360 -10, 640 -10, 880 70"/>
        <circle class="halo" cx="120" cy="170" r="10"/><circle class="dot" cx="120" cy="170" r="6"/>
        <circle class="halo" cx="880" cy="70" r="10"/><circle class="dot" cx="880" cy="70" r="6"/>
        <text x="120" y="204" text-anchor="middle">SANTA PONÇA</text><text x="120" y="150" text-anchor="middle" class="sub">Mallorca office</text>
        <text x="880" y="44" text-anchor="middle">KÖLN</text><text x="880" y="104" text-anchor="middle" class="sub">Headquarters</text>
        <text x="500" y="70" text-anchor="middle" class="sub">≈ 1,320 km · one team standard</text>
      </svg>
    </div>
    <ol class="timeline">
      <li class="reveal"><b>1980</b><span>Electricians in Cologne</span></li>
      <li class="reveal"><b>2010</b><span>Takeover by master electrician Dirk Woronow</span></li>
      <li class="reveal"><b>2017</b><span>First major projects on Mallorca</span></li>
      <li class="reveal"><b>2022</b><span>Own office and team on Mallorca</span></li>
    </ol>
  </div>
</section>

<section class="brands" aria-label="Branded products we install">
  <div class="wrap"><p class="eyebrow">Branded products we install</p></div>
  {marquee(BRANDS, big=True)}
</section>
{cta(pre)}'''
    page("index.html", SRC["home"]["title"], SRC["home"]["description"], body, "Home",
         f'<script type="application/ld+json">{json.dumps(JSONLD, ensure_ascii=False)}</script>\n')


# ---------------------------------------------------------------- services
def build_services_overview():
    pre = ""
    rows, previews = [], []
    for i, (old, new, name, tag, ic) in enumerate(SERVICES):
        sv = SRC["services"][old]
        rows.append(f'''<a class="svc-row reveal" href="services/{new}.html" data-key="{new}">
  {picture(tile_key(old), name, pre, "svc-thumb", "100vw")}
  <span class="idx">{i + 1:02d}</span>
  <span><h2>{e(name)}</h2><p>{e(tag)} – {e(text(tidy(sv["intro"]))[:150].rsplit(" ", 1)[0])}…</p></span>
  <span class="round">{icon("arrow")}</span>
</a>''')
        previews.append(f'<img data-for="{new}" src="{pre}{img(tile_key(old), "s")}" alt="" loading="lazy">')
    body = f'''
<section class="page-hero">
  <div class="glow-orb"></div>
  <div class="wrap">
    <p class="eyebrow">Services</p>
    <h1 class="display">Everything for intelligent buildings. <span class="metal">From a single source.</span></h1>
    <p class="lead">Planning, installation and maintenance of electrical, KNX, lighting, security and media technology for private homes, businesses and industry.</p>
  </div>
</section>
<section class="svc-list" style="padding-top:0">
  <div class="wrap">{"".join(rows)}</div>
  <div class="cursor-img" aria-hidden="true">{"".join(previews)}</div>
</section>
{cta(pre)}'''
    page("services.html", "Services – Elektro Paul Neumann, Electrician Cologne & Mallorca",
         "KNX system integration, smart home, lighting, alarm systems, video surveillance, video intercoms, multi-room audio and electrical service in Cologne and Mallorca.",
         body, "Services")


def build_service(idx):
    old, new, name, tag, ic = SERVICES[idx]
    sv = SRC["services"][old]
    pre = "../"
    n_img, chapters, toc, extra_head = 0, [], [], ""
    num = 0
    for sec in sv["sections"]:
        title = sec.get("title")
        if title == "additional services":
            continue
        h = tidy(sec["html"])
        keys = []
        for _ in sec["images"]:
            n_img += 1
            keys.append(f"services/{old}/{n_img:02d}")
        if sec.get("faq"):
            num += 1
            items = "".join(f'<details class="faq-item"><summary>{e(q["q"])}<span>{icon("plus")}</span></summary><p>{e(q["a"])}</p></details>' for q in sec["faq"])
            chapters.append(f'<div class="chapter" id="faq"><div class="chapter-head"><span class="idx">{num:02d}</span><h2 class="h2">Frequently asked questions</h2></div><div class="faq-list reveal">{items}</div></div>')
            toc.append(("faq", num, "FAQ"))
            ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
                {"@type": "Question", "name": q["q"], "acceptedAnswer": {"@type": "Answer", "text": q["a"]}} for q in sec["faq"]]}
            extra_head = f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>\n'
            continue
        if len(keys) > 3:
            num += 1
            figs = "".join(f'<a class="g-item reveal" href="{pre}{img(k)}" data-lightbox="svc" data-caption="{e(name)} – reference {i + 1}">{picture(k, f"{name} – reference photo {i + 1}", pre, "", "(max-width: 760px) 50vw, 25vw")}</a>' for i, k in enumerate(keys))
            chapters.append(f'<div class="chapter" id="gallery"><div class="chapter-head"><span class="idx">{num:02d}</span><h2 class="h2">In our projects</h2></div><p class="muted">{len(keys)} photos – click to enlarge.</p><div class="masonry">{figs}</div></div>')
            toc.append(("gallery", num, "Gallery"))
            continue
        if not title and not keys and not sec["videos"]:
            chapters.append(f'''<div class="chapter"><div class="callout reveal"><div class="callout-text">{h}</div>
  <div class="callout-actions"><a class="btn btn-light magnetic" href="{PHONE_HREF}">{icon("phone")} {PHONE}</a><a class="btn btn-glass" href="{pre}contact.html">Contact {icon("arrow")}</a></div></div></div>''')
            continue
        num += 1
        cid = f"c{num}"
        media = ""
        if sec["videos"]:
            media = yt(sec["videos"][0], title or name)
        elif keys:
            media = f'<a class="media-img" href="{pre}{img(keys[0])}" data-lightbox="svc-{n_img}" data-caption="{e(title or name)}">{picture(keys[0], title or name, pre, "", "(max-width: 900px) 100vw, 40vw")}</a>'
        kick = f'<p class="kicker">{e(sec.get("kicker"))}</p>' if sec.get("kicker") else ""
        chapters.append(f'''<div class="chapter" id="{cid}">
  <div class="chapter-head reveal"><span class="idx">{num:02d}</span><div>{kick}<h2 class="h2">{e(title or "")}</h2></div></div>
  <div class="chapter-body{" has-media" if media else ""}"><div class="rich reveal">{h}</div>{f'<div class="chapter-media reveal">{media}</div>' if media else ""}</div>
</div>''')
        toc.append((cid, num, title or ""))
    toc_html = "".join(f'<a href="#{cid}"><span class="idx">{n:02d}</span>{e(t if len(t) < 42 else t[:40] + "…")}</a>' for cid, n, t in toc)
    others = "".join(f'<a class="chip" href="{s}.html">{icon(i2)} {e(n)}</a>' for _, s, n, _, i2 in SERVICES if s != new)
    hero_key = ("ai/hero-knx" if old == "knx-systemintegrator" and "ai/hero-knx" in IMG
                else f"services/{old}/title" if img(f"services/{old}/title") else tile_key(old))
    kicker = sv["kicker"] if sv["kicker"] not in (sv["h1"], "Smart Home") else name
    body = f'''
<section class="page-hero media-hero">
  {media_hero(hero_key, name, pre)}
  <div class="wrap">
    <nav class="crumbs" aria-label="Breadcrumb"><a href="{pre}index.html">Home</a>{icon("chev")}<a href="{pre}services.html">Services</a>{icon("chev")}<span>{e(name)}</span></nav>
    <p class="eyebrow">{e(kicker)}</p>
    <h1 class="display">{e(sv["h1"])}</h1>
    <div class="lead rich">{tidy(sv["intro"])}</div>
    <div class="actions"><a class="btn btn-light magnetic" href="{pre}contact.html">Request consultation {icon("arrow")}</a><a class="btn btn-glass magnetic" href="{PHONE_HREF}">{icon("phone")} {PHONE}</a></div>
  </div>
</section>
<section class="light">
  <div class="wrap chapters-wrap">
    <aside class="chapters"><p>{e(name)}</p>{toc_html}<a class="btn btn-dark btn-sm" href="{pre}contact.html">Get advice {icon("arrow")}</a></aside>
    <div>{"".join(chapters)}</div>
  </div>
</section>
<section>
  <div class="wrap">
    <div class="sec-head reveal"><p class="eyebrow">Additional services</p><h2 class="h2">Everything from a single source.</h2></div>
    <div class="chips reveal">{others}</div>
  </div>
</section>
{cta(pre)}'''
    title = sv["title"] if sv["title"] not in ("Alarm systems", "Smart Home", "Video surveillance", "Video intercom systems", "Multi-room audio") else f"{name} in Cologne & Mallorca – Elektro Paul Neumann"
    page(f"services/{new}.html", title, sv["description"], body, "KNX" if new == "knx-system-integration" else "Services", extra_head)


# ---------------------------------------------------------------- projects
def build_projects():
    pre = ""
    order = list(PROJECTS)
    cards = []
    for i, k in enumerate(order):
        p = SRC["projects"][k]; new, name, sub, cat = PROJECTS[k]; n = len(p["images"])
        cards.append(f'''<a class="pcard spot reveal" href="projects/{new}.html" data-cat="{cat}">
  {picture(f"projects/{k}/cover", f"{name} – {sub}", pre, "pcard-img", "(max-width: 760px) 100vw, 50vw")}
  <span class="pcard-top"><span class="idx">{i + 1:02d} / {len(order)}</span><span class="tag">{cat}</span></span>
  <span class="pcard-body"><b>{e(name)}</b><small><span>{e(sub)}</span><span>{f"{n} photos" if n else ""}</span></small></span>
</a>''')
    body = f'''
<section class="page-hero">
  <div class="glow-orb"></div>
  <div class="wrap">
    <p class="eyebrow">Projects</p>
    <h1 class="display">Villas, stadiums, studios <span class="metal">&amp; headquarters.</span></h1>
    <p class="lead">A selection of our projects around Cologne and Mallorca – electrical engineering, KNX, security, lighting, network and media technology.</p>
    <div class="filters" role="group" aria-label="Filter projects">
      <button type="button" class="filter is-on" data-filter="all" aria-pressed="true">All {len(order)}</button>
      <button type="button" class="filter" data-filter="Residential" aria-pressed="false">Residential</button>
      <button type="button" class="filter" data-filter="Commercial" aria-pressed="false">Commercial</button>
    </div>
  </div>
</section>
<section style="padding-top:0"><div class="wrap"><div class="proj-grid">{"".join(cards)}</div></div></section>
{cta(pre, "Your project next?")}'''
    page("projects.html", "Projects – Elektro Paul Neumann, Electrician Cologne | KNX & Security Technology",
         "A selection of our projects around Cologne and Mallorca: villas, penthouses, Bayer 04 Leverkusen, WDR, TÜV Rheinland, hotels and offices.", body, "Projects")
    for i, k in enumerate(order):
        build_project(k, order[(i + 1) % len(order)], i + 1, len(order))


def build_project(slug, nxt, no, total):
    p = SRC["projects"][slug]
    new, name, sub, cat = PROJECTS[slug]
    pre = "../"
    keys = [f"projects/{slug}/{i:02d}" for i in range(1, len(p["images"]) + 1)]
    figs = "".join(
        f'<a class="g-item reveal" href="{pre}{img(k)}" data-lightbox="p" data-caption="{e(name)} – photo {i + 1}">{picture(k, f"{name} – photo {i + 1}", pre, "", "(max-width: 760px) 50vw, 33vw")}</a>'
        for i, k in enumerate(keys))
    gallery = f'''<section style="padding-top:0"><div class="wrap">
  <div class="sec-head row reveal"><div><p class="eyebrow">Gallery</p><h2 class="h2">{len(keys)} photos</h2></div><p class="muted" style="margin:0">Click a photo – then use the arrows, your keyboard or swipe.</p></div>
  <div class="masonry">{figs}</div></div></section>''' if keys else ""
    nx = PROJECTS[nxt]
    body = f'''
<section class="page-hero media-hero">
  {media_hero(f"projects/{slug}/cover", name, pre)}
  <div class="wrap">
    <nav class="crumbs" aria-label="Breadcrumb"><a href="{pre}index.html">Home</a>{icon("chev")}<a href="{pre}projects.html">Projects</a>{icon("chev")}<span>{e(name)}</span></nav>
    <p class="eyebrow">Project {no:02d} / {total} · {e(cat)}</p>
    <h1 class="display">{e(name)}</h1>
    <p class="lead">{e(sub)}</p>
  </div>
</section>
<section class="proj-intro"><div class="wrap proj-intro-grid">
  <div class="reveal"><p class="eyebrow">Scope of work</p><p class="lead">{e(p["text"]) if p["text"] else "Project details on request."}</p></div>
  <dl class="facts reveal"><div><dt>Project</dt><dd>{e(name)}</dd></div><div><dt>Details</dt><dd>{e(sub)}</dd></div><div><dt>Category</dt><dd>{cat}</dd></div><div><dt>Photos</dt><dd>{len(keys) or "–"}</dd></div></dl>
</div></section>
{gallery}
<a class="next-proj" href="{nx[0]}.html">
  {picture(f"projects/{nxt}/cover", "", pre, "", "100vw")}
  <span class="wrap"><small>Next project</small><b>{e(nx[1])} <span class="round">{icon("arrow")}</span></b></span>
</a>'''
    page(f"projects/{new}.html", f"{name} – Project by Elektro Paul Neumann", p["text"] or f"{name} – a project by Elektro Paul Neumann, {sub}.", body, "Projects")


# ---------------------------------------------------------------- careers
def build_careers():
    pre = ""
    jobs = [("Construction fitter", "Realization and execution of large and small projects, property management, building and office conversions, renovations of practices, villas, houses and apartments.", "karriere/01"),
            ("Service technician", "Service and support for regular customers, video intercom systems, KNX building management systems, alarm systems, video surveillance, smart home.", "karriere/02"),
            ("Trainee (apprentice)", "Training in a future-oriented profession with innovative technology.", "karriere/03"),
            ("Helper (m/f/d)", "We are now looking for energetic helpers for our team!", "karriere/04")]
    bring = ["Completed training in electrical engineering", "Ideally, initial experience in service, project management or on construction sites", "Class B driving license", "Desire for long-term cooperation"]
    offer = ["Permanent position after successful probationary period", "Attractive earning opportunities", "High-quality service vehicle",
             "Thorough training and collegial cooperation", "Regular training – technical and safety-related", "Social security and a modern working environment"]
    li = lambda xs: "".join(f"<li>{e(x)}</li>" for x in xs)
    job_cards = "".join(f'''<article class="job reveal">{picture(k, t, pre, "job-img", "(max-width: 760px) 60vw, 20vw")}
<div><span class="idx">{i + 1:02d}</span><h3>{e(t)}</h3><p>{e(d)}</p><a class="link-more" href="mailto:{MAIL}?subject={e("Application: " + t)}">Apply now {icon("arrow")}</a></div></article>''' for i, (t, d, k) in enumerate(jobs))
    body = f'''
<section class="page-hero media-hero">
  {media_hero("karriere/hero", "Team at work", pre)}
  <div class="wrap">
    <p class="eyebrow">Become part of the team</p>
    <h1 class="display">Build the <span class="metal">smart buildings</span> of tomorrow.</h1>
    <p class="lead">As a specialist company for electrical and security technology with demanding customers in Germany and Mallorca, we rely on team members who think for themselves, take responsibility – and are passionate about what they do.</p>
    <div class="actions"><a class="btn btn-light magnetic" href="#jobs">Open positions {icon("arrow")}</a><a class="btn btn-glass magnetic" href="mailto:{MAIL}">{icon("mail")} Apply by email</a></div>
  </div>
</section>
<section>
  <div class="wrap tc-grid">
    <div class="panel reveal"><p class="eyebrow">You</p><h2 class="h3">What you bring with you</h2><p>You enjoy working in a team, are reliable, flexible, and approach our customers with professionalism and friendliness. Technical understanding and manual dexterity are just as much a given for you as a willingness to develop yourself and think outside the box.</p><ul class="checks">{li(bring)}</ul></div>
    <div class="panel invert reveal"><p class="eyebrow">Us</p><h2 class="h3">What we offer you</h2><p>More than just a job – we offer you prospects. A professional environment with high-quality projects, personal appreciation and genuine future security.</p><ul class="checks">{li(offer)}</ul></div>
  </div>
  <div class="wrap narrow center" style="margin-top:clamp(70px,9vw,120px)"><p class="lit">We also welcome career changers with technical expertise – and we have been training apprentices for years, with numerous successes.</p></div>
</section>
<section class="light" id="jobs"><div class="wrap">
  <div class="sec-head row reveal"><div><p class="eyebrow">Open positions</p><h2 class="h2">Become part of a team<br>that lives quality.</h2></div></div>
  <div class="job-grid">{job_cards}</div>
</div></section>
{cta(pre, "Apply now.", f"Send your detailed application to {MAIL} – we look forward to meeting you.")}'''
    page("careers.html", "Careers – Elektro Paul Neumann, KNX professional from Cologne", SRC["karriere"]["description"], body, "Careers")


# ---------------------------------------------------------------- contact
def build_contact():
    pre = ""
    body = f'''
<section class="page-hero">
  <div class="glow-orb"></div>
  <div class="wrap">
    <p class="eyebrow">For you in Cologne and Mallorca</p>
    <h1 class="display">Let’s build something <span class="metal">smart.</span></h1>
    <p class="lead">Call us, write us an email or visit us. After an on-site appointment you receive a binding quote with a detailed description of the work.</p>
  </div>
</section>
<section style="padding-top:0">
  <div class="wrap">
    <div class="big-links">
      <a class="reveal" href="{PHONE_HREF}"><span><small>Call</small>{PHONE}</span><span class="round">{icon("arrow")}</span></a>
      <a class="reveal" href="mailto:{MAIL}"><span><small>Email</small>{MAIL}</span><span class="round">{icon("arrow")}</span></a>
      <a class="reveal" href="{MAPS}" rel="noopener"><span><small>Visit · Cologne</small>Emil-Hoffmann-Str. 39-43</span><span class="round">{icon("arrow")}</span></a>
    </div>
  </div>
</section>
<section style="padding-top:0"><div class="wrap office-grid">
  <article class="office reveal">
    {picture("kontakt/01", "Cologne office", pre, "office-img", "(max-width: 900px) 100vw, 50vw")}
    <div class="office-body">
      <p class="eyebrow">Germany · Headquarters</p><h2 class="h3">Cologne office</h2>
      <ul class="contact-list">
        <li>{icon("pin")}<a href="{MAPS}" rel="noopener">Elektro Paul Neumann<br>Emil-Hoffmann-Straße 39-43<br>Halle 1 + 2<br>50996 Köln</a></li>
        <li>{icon("phone")}<span><a href="{PHONE_HREF}">{PHONE}</a><br><a href="{PHONE2_HREF}">{PHONE2}</a></span></li>
        <li>{icon("mail")}<a href="mailto:{MAIL}">{MAIL}</a></li>
      </ul>
      <a class="btn btn-glass btn-sm" href="{MAPS}" rel="noopener">Open in Google Maps {icon("upright")}</a>
    </div>
  </article>
  <article class="office reveal">
    {picture("kontakt/02", "Mallorca office", pre, "office-img", "(max-width: 900px) 100vw, 50vw")}
    <div class="office-body">
      <p class="eyebrow">Spain · Since 2022</p><h2 class="h3">Mallorca office</h2>
      <ul class="contact-list">
        <li>{icon("pin")}<span>Elektro Paul Neumann<br>Avinguda del Rei Jaume I, 109<br>07180 Santa Ponça<br>Illes Balears, Spain</span></li>
        <li>{icon("phone")}<a href="{PHONE_HREF}">{PHONE}</a></li>
        <li>{icon("mail")}<a href="mailto:{MAIL}">{MAIL}</a></li>
      </ul>
    </div>
  </article>
</div></section>
<section class="light">
  <div class="wrap">
    <div class="sec-head reveal"><p class="eyebrow">What happens next</p><h2 class="h2">Three steps to your project.</h2></div>
    <ol class="steps">
      <li class="reveal"><span class="idx">01 — Idea</span><h3>You tell us.</h3><p>About your property and your plans – by phone or email.</p></li>
      <li class="reveal"><span class="idx">02 — Conception</span><h3>We plan.</h3><p>On-site appointment, then a binding quote with a detailed description of the work.</p></li>
      <li class="reveal"><span class="idx">03 — Implementation</span><h3>We deliver.</h3><p>Installation, commissioning, handover – and service and maintenance afterwards.</p></li>
    </ol>
  </div>
</section>'''
    page("contact.html", SRC["kontakt"]["title"], SRC["kontakt"]["description"], body, "Contact")


# ---------------------------------------------------------------- imprint
def build_imprint():
    h = tidy(SRC["impressum"]["html"])
    h = h.replace("<h3>Dirk Woronow</h3>", "<p><strong>Dirk Woronow</strong></p>")
    h = re.sub(r"phone:\s*\+49 \(0\) 221 - 431 351\s*Email:\s*info@elektro-paul-neumann.de\s*Web:\s*elektro-paul-neumann.de\s*VAT ID No.:\s*DE251151581",
               f'<p>Phone: <a href="{PHONE_HREF}">{PHONE}</a><br>Email: <a href="mailto:{MAIL}">{MAIL}</a><br>Web: elektro-paul-neumann.de<br>VAT ID No.: DE251151581</p>', h)
    h = h.replace("<h3>Privacy Policy</h3>", '<h2 class="h2" id="privacy">Privacy policy</h2>')
    h = re.sub(r"<h3>([a-z])", lambda m: "<h3>" + m.group(1).upper(), h)
    body = f'''
<section class="page-hero"><div class="glow-orb"></div><div class="wrap"><p class="eyebrow">Legal</p><h1 class="display">Imprint &amp; <span class="metal">privacy.</span></h1></div></section>
<section class="legal light"><div class="wrap narrow rich">{h}</div></section>'''
    page("imprint.html", "Imprint & privacy policy – Elektro Paul Neumann", SRC["impressum"]["description"], body)


if __name__ == "__main__":
    build_home()
    build_services_overview()
    for i in range(len(SERVICES)):
        build_service(i)
    build_projects()
    build_careers()
    build_contact()
    build_imprint()
    print("built")
