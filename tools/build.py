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


# ---------------------------------------------------------------- layout
NAV = [("index.html", "Home"), ("services.html", "Services"), ("services/knx-system-integration.html", "KNX"),
       ("projects.html", "Projects"), ("careers.html", "Careers"), ("contact.html", "Contact")]


def header(pre, active):
    links = []
    for href, label in NAV:
        cur = ' aria-current="page"' if active == label else ""
        if label == "Services":
            items = "".join(
                f'<a class="mega-item" href="{pre}services/{s}.html">{icon(ic)}<span><b>{e(n)}</b><small>{e(t)}</small></span></a>'
                for _, s, n, t, ic in SERVICES)
            links.append(
                f'<div class="has-mega"><a href="{pre}{href}"{cur} class="nav-link">Services {icon("down", "i caret")}</a>'
                f'<div class="mega"><div class="mega-inner"><div class="mega-grid">{items}</div>'
                f'<a class="mega-all" href="{pre}services.html">{icon("grid")} All services</a></div></div></div>')
        elif label != "Home":
            links.append(f'<a href="{pre}{href}"{cur} class="nav-link">{label}</a>')
    mob = "".join(f'<a href="{pre}{h}">{l}</a>' for h, l in NAV)
    mob_s = "".join(f'<a class="sub" href="{pre}services/{s}.html">{e(n)}</a>' for _, s, n, _, _ in SERVICES)
    return f'''<a class="skip" href="#main">Skip to content</a>
<header class="site-header" id="top">
  <div class="bar">
    <a class="brand" href="{pre}index.html" aria-label="Elektro Paul Neumann – Smart Buildings, home"><img src="{pre}assets/brand/logo.svg" alt="Paul Neumann Smart Buildings" width="186" height="37"></a>
    <nav class="nav" aria-label="Main">{"".join(links)}</nav>
    <div class="bar-cta">
      <a class="phone-link" href="{PHONE_HREF}">{icon("phone")}<span>{PHONE}</span></a>
      <a class="btn btn-light btn-sm" href="{pre}contact.html">Request consultation</a>
      <button class="menu-btn" type="button" aria-expanded="false" aria-controls="mobile-menu"><span></span><span></span><span class="sr">Menu</span></button>
    </div>
  </div>
  <div class="mobile-menu" id="mobile-menu" hidden>
    <nav aria-label="Mobile">{mob}<p class="mm-label">Services</p>{mob_s}</nav>
    <div class="mm-foot"><a class="btn btn-light" href="{PHONE_HREF}">{icon("phone")} Call {PHONE}</a><a class="btn btn-ghost" href="mailto:{MAIL}">{icon("mail")} {MAIL}</a></div>
  </div>
</header>'''


def footer(pre):
    svc = "".join(f'<li><a href="{pre}services/{s}.html">{e(n)}</a></li>' for _, s, n, _, _ in SERVICES)
    return f'''<footer class="site-footer">
  <div class="wrap">
    <div class="foot-top">
      <img src="{pre}assets/brand/logo.svg" alt="Paul Neumann Smart Buildings" width="220" height="44" loading="lazy">
      <p>Electrical, KNX and security technology in Cologne and on Mallorca. Since 1980.</p>
    </div>
    <div class="foot-grid">
      <div><h3>Services</h3><ul>{svc}</ul></div>
      <div><h3>Company</h3><ul>
        <li><a href="{pre}projects.html">Projects</a></li><li><a href="{pre}careers.html">Careers</a></li>
        <li><a href="{pre}contact.html">Contact</a></li><li><a href="{pre}imprint.html">Imprint</a></li><li><a href="{pre}imprint.html#privacy">Privacy policy</a></li></ul></div>
      <div><h3>Cologne office</h3><address><a href="{MAPS}" rel="noopener">Emil-Hoffmann-Straße 39-43<br>Halle 1 + 2<br>50996 Köln</a><br><a href="{PHONE_HREF}">{PHONE}</a><br><a href="{PHONE2_HREF}">{PHONE2}</a><br><a href="mailto:{MAIL}">{MAIL}</a></address></div>
      <div><h3>Mallorca office</h3><address>Avinguda del Rei Jaume I, 109<br>07180 Santa Ponça<br>Illes Balears, Spain<br><a href="{PHONE_HREF}">{PHONE}</a><br><a href="mailto:{MAIL}">{MAIL}</a></address></div>
    </div>
    <div class="foot-bottom"><span>© Elektro Paul Neumann · Dirk Woronow</span><span><a href="{pre}imprint.html">Imprint</a> · <a href="{pre}imprint.html#privacy">Privacy</a></span></div>
  </div>
</footer>'''


JSONLD = {
    "@context": "https://schema.org", "@type": "Electrician", "name": "Elektro Paul Neumann",
    "alternateName": "Paul Neumann Smart Buildings", "url": "https://elektro-paul-neumann.de/",
    "email": MAIL, "telephone": "+49221431351", "foundingDate": "1980", "founder": None,
    "areaServed": ["Köln", "Deutschland", "Mallorca"],
    "address": {"@type": "PostalAddress", "streetAddress": "Emil-Hoffmann-Straße 39-43, Halle 1 + 2",
                "postalCode": "50996", "addressLocality": "Köln", "addressCountry": "DE"},
    "department": [{"@type": "Electrician", "name": "Elektro Paul Neumann – Mallorca",
                    "address": {"@type": "PostalAddress", "streetAddress": "Avinguda del Rei Jaume I, 109",
                                "postalCode": "07180", "addressLocality": "Santa Ponça", "addressRegion": "Illes Balears", "addressCountry": "ES"}}],
}
JSONLD.pop("founder")


def page(path, title, desc, body, active="", extra_head=""):
    depth = path.count("/")
    pre = "../" * depth
    doc = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta name="theme-color" content="#131313">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:image" content="{pre}{img('ai/hero-home') or img('home/hero')}">
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
  <button class="lb-next" type="button" aria-label="Next image">{icon("chev")}</button>
</div>
<script src="{pre}assets/js/site.js" defer></script>
</body>
</html>
'''
    out = f"{R}/{path}"
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, "w", encoding="utf-8").write(doc)


def cta_band(pre, title="Let’s plan your project.", sub="From the first consultation to the final installation – in Cologne, throughout Germany and on Mallorca."):
    return f'''<section class="cta-band dark">
  <div class="wrap narrow center reveal">
    {eyebrow("Get in touch")}
    <h2 class="display">{e(title)}</h2>
    <p class="lead">{e(sub)}</p>
    <div class="actions center"><a class="btn btn-light" href="{PHONE_HREF}">{icon("phone")} {PHONE}</a><a class="btn btn-ghost" href="mailto:{MAIL}">{icon("mail")} Write an email</a></div>
  </div>
</section>'''


def project_card(slug, pre, size=""):
    p = SRC["projects"][slug]
    new, name, sub, cat = PROJECTS[slug]
    n = len(p["images"])
    count = f'<span class="count">{n} photos</span>' if n else ""
    return f'''<a class="pcard {size} reveal" href="{pre}projects/{new}.html" data-cat="{cat}">
  {picture(f"projects/{slug}/cover", f"{name} – {sub}", pre, "pcard-img", "(max-width: 760px) 100vw, 50vw")}
  <span class="pcard-body"><span class="tag">{cat}</span><b>{e(name)}</b><small>{e(sub)}</small>{count}</span>
</a>'''


# ---------------------------------------------------------------- home
def hero_media(pre):
    if "ai/hero-home" not in IMG:
        return picture("home/hero", "Modern office building in Cologne with Cologne Cathedral in the background", pre, "hero-img", "100vw", eager=True)
    pic = picture("ai/hero-home", "Modern villa on Mallorca at blue hour with architectural lighting", pre, "hero-img", "100vw", eager=True)
    if os.path.exists(f"{R}/assets/img/ai/hero-home-video.mp4"):
        return (f'<video class="hero-img hero-video" autoplay muted loop playsinline preload="metadata" poster="{pre}{img("ai/hero-home")}" '
                f'aria-hidden="true"><source src="{pre}assets/img/ai/hero-home-video.mp4" type="video/mp4"></video>')
    return pic


def build_home():
    pre = ""
    s = SRC
    svc_tiles = []
    for i, (old, new, name, tag, ic) in enumerate(SERVICES):
        big = " tile-lg" if i in (0, 1) else ""
        svc_tiles.append(f'''<a class="tile{big} reveal" href="services/{new}.html">
  {picture(tile_key(old), name, pre, "tile-img", "(max-width: 760px) 100vw, 50vw")}
  <span class="tile-body">{icon(ic, "i tile-ic")}<b>{e(name)}</b><small>{e(tag)}</small><span class="more">Learn more {icon("chev")}</span></span>
</a>''')
    featured = ["villa_xxl", "penthouse_xxl", "bayer04_leverkusen", "hotel_im_wasserturm", "townhouse", "stroeer_media_se", "wdr_studios_koeln", "tuev_rheinland"]
    rail = "".join(f'''<a class="rail-card" href="projects/{PROJECTS[k][0]}.html">{picture(f"projects/{k}/cover", PROJECTS[k][1], pre, "", "(max-width: 760px) 85vw, 40vw")}
<span><b>{e(PROJECTS[k][1])}</b><small>{e(PROJECTS[k][2])}</small></span></a>''' for k in featured)
    brands = "".join(f"<li>{b}</li>" for b in BRANDS)
    body = f'''
<section class="hero dark">
  {hero_media(pre)}
  <div class="hero-shade"></div>
  <div class="wrap hero-content">
    {eyebrow("Building technology at the highest level")}
    <h1 class="hero-title"><span>Intelligent building technology.</span><span>Perfectly planned.</span><span>Precisely implemented.</span></h1>
    <p class="lead">Your partner for electrical installations, smart home technology, KNX building automation, lighting and security technology in Cologne and Mallorca.</p>
    <div class="actions"><a class="btn btn-light" href="services.html">Explore services</a><a class="btn btn-ghost" href="contact.html">Request consultation {icon("chev")}</a></div>
  </div>
  <div class="wrap"><ul class="stats">
    <li><b>1980</b><span>Electricians in Cologne since</span></li>
    <li><b>2</b><span>Locations – Cologne &amp; Mallorca</span></li>
    <li><b>KNX</b><span>Certified KNX partner</span></li>
    <li><b>{len(PROJECTS)}</b><span>Reference projects online</span></li>
  </ul></div>
</section>

<section class="statement">
  <div class="wrap narrow center reveal">
    {eyebrow("Your partner for")}
    <h2 class="display">Smart solutions for electrical and security technology in Cologne and Mallorca.</h2>
    <p class="lead muted">Your electrician in Cologne for high-quality residential and commercial projects: KNX system integration, smart home, lighting, alarm and video surveillance, and multi-room audio – from planning to installation. Since 1980.</p>
  </div>
</section>

<section class="services-bento light" id="services">
  <div class="wrap">
    <div class="sec-head reveal">
      {eyebrow("Our services")}
      <h2 class="h2">Every project is unique.</h2>
      <p class="lead muted">We implement your projects – successfully, individually and professionally. We guarantee this through our broad range of services.</p>
    </div>
    <div class="bento">{"".join(svc_tiles)}</div>
  </div>
</section>

<section class="split dark">
  <div class="wrap split-grid">
    <div class="split-media reveal">{picture("home/security", "Woman using a wall-mounted smart building touch panel", pre, "", "(max-width: 900px) 100vw, 55vw")}</div>
    <div class="split-text reveal">
      {eyebrow("Tailor-made solutions – from experts in Cologne")}
      <h2 class="h2">Security technology from Cologne for the highest demands.</h2>
      <p>Since 1980, we have been offering customized security solutions for your home and industry. From smart home installations to alarm systems – everything from a single source.</p>
      <p>With high-quality branded products and personal service, we accompany you from the initial consultation to the final installation.</p>
      <p class="muted">Our experts guarantee innovative and reliable technology to maximize your security, whether in your city apartment, holiday home or business.</p>
    </div>
  </div>
</section>

<section class="process">
  <div class="wrap">
    <div class="sec-head center reveal">{eyebrow("How we work")}<h2 class="h2">From the first idea to the finished installation.</h2></div>
    <ol class="steps">
      <li class="reveal"><span class="step-no">01</span><h3>Idea</h3><p>We listen, look at your property on site and understand what you want to achieve.</p></li>
      <li class="reveal"><span class="step-no">02</span><h3>Conception</h3><p>Planning, system design and a binding quote with a detailed description of the work.</p></li>
      <li class="reveal"><span class="step-no">03</span><h3>Implementation</h3><p>Professional installation, commissioning, handover – and long-term service.</p></li>
    </ol>
  </div>
</section>

<section class="locations dark">
  <div class="wrap">
    <div class="sec-head reveal">{eyebrow("For you")}<h2 class="h2">Two locations. Two teams.</h2></div>
    <div class="loc-grid">
      <article class="loc reveal">
        <video class="loc-video" muted loop playsinline preload="none" poster="assets/video/cologne2.webp" data-autoplay><source src="assets/video/cologne2.mp4" type="video/mp4"></video>
        <div class="loc-body">
          <p class="eyebrow">Cologne, Germany</p>
          <h3>Your electrician in Cologne since 1980.</h3>
          <p>We implement sophisticated electrical and security technology in the city and the surrounding area – specializing in planning, KNX integration and excellent execution.</p>
          <p class="muted">Since the takeover in 2010, the company has been managed by Dirk Woronow, master electrician and managing director.</p>
        </div>
      </article>
      <article class="loc reveal">
        <video class="loc-video" muted loop playsinline preload="none" poster="assets/video/palma2.webp" data-autoplay><source src="assets/video/palma2.mp4" type="video/mp4"></video>
        <div class="loc-body">
          <p class="eyebrow">Palma de Mallorca</p>
          <h3>On the island since 2017.</h3>
          <p>After completing major projects on Mallorca, we founded our own office with our own team in 2022 – a specialist for KNX planning and integration, smart home, video, alarm, multi-room audio and media systems.</p>
        </div>
      </article>
    </div>
    <ol class="timeline reveal">
      <li><b>1980</b><span>Electricians in Cologne since 1980</span></li>
      <li><b>2010</b><span>Takeover by master electrician Dirk Woronow</span></li>
      <li><b>2017</b><span>First major projects on Mallorca</span></li>
      <li><b>2022</b><span>Own office and team on Mallorca</span></li>
    </ol>
  </div>
</section>

<section class="projects-rail light">
  <div class="wrap">
    <div class="sec-head row reveal"><div>{eyebrow("Projects")}<h2 class="h2">Work we’re proud of.</h2></div>
      <div class="rail-ctrl"><button type="button" class="round" data-rail="-1" aria-label="Scroll back">{icon("left")}</button><button type="button" class="round" data-rail="1" aria-label="Scroll forward">{icon("chev")}</button></div></div>
  </div>
  <div class="rail" tabindex="0" aria-label="Featured projects">{rail}</div>
  <div class="wrap"><a class="link-more" href="projects.html">View all {len(PROJECTS)} projects {icon("chev")}</a></div>
</section>

<section class="brands">
  <div class="wrap center reveal">{eyebrow("Branded products we install")}<ul class="brand-list">{brands}</ul></div>
</section>
{cta_band(pre)}'''
    page("index.html", s["home"]["title"], s["home"]["description"], body, "Home",
         f'<script type="application/ld+json">{json.dumps(JSONLD, ensure_ascii=False)}</script>\n')


# ---------------------------------------------------------------- services
def build_services_overview():
    pre = ""
    rows = []
    for i, (old, new, name, tag, ic) in enumerate(SERVICES):
        sv = SRC["services"][old]
        rows.append(f'''<a class="svc-row reveal" href="services/{new}.html">
  <span class="svc-no">{i + 1:02d}</span>
  {picture(tile_key(old), name, pre, "svc-img", "(max-width: 760px) 100vw, 40vw")}
  <span class="svc-text">{icon(ic, "i tile-ic")}<b>{e(name)}</b><span>{e(tag)}</span><small>{e(text(tidy(sv["intro"]))[:210].rsplit(" ", 1)[0])}…</small></span>
  <span class="round">{icon("arrow")}</span>
</a>''')
    body = f'''
<section class="page-hero dark compact">
  <div class="wrap">
    {eyebrow("Services")}
    <h1 class="display">Everything for intelligent buildings – from a single source.</h1>
    <p class="lead muted">Planning, installation and maintenance of electrical, KNX, lighting, security and media technology for private homes, businesses and industry.</p>
  </div>
</section>
<section class="svc-list">
  <div class="wrap">{"".join(rows)}</div>
</section>
{cta_band(pre)}'''
    page("services.html", "Services – Elektro Paul Neumann, Electrician Cologne & Mallorca",
         "KNX system integration, smart home, lighting, alarm systems, video surveillance, video intercoms, multi-room audio and electrical service in Cologne and Mallorca.",
         body, "Services")


def build_service(idx):
    old, new, name, tag, ic = SERVICES[idx]
    sv = SRC["services"][old]
    pre = "../"
    n_img = 0
    blocks = []
    flip = False
    extra_head = ""
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
            items = "".join(f'<details class="faq-item"><summary>{e(q["q"])}<span>{icon("plus")}</span></summary><p>{e(q["a"])}</p></details>' for q in sec["faq"])
            blocks.append(f'''<section class="faq light" id="faq"><div class="wrap narrow">
  <div class="sec-head reveal">{eyebrow("FAQ")}<h2 class="h2">Frequently asked questions</h2></div>
  <div class="faq-list reveal">{items}</div></div></section>''')
            ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
                {"@type": "Question", "name": q["q"], "acceptedAnswer": {"@type": "Answer", "text": q["a"]}} for q in sec["faq"]]}
            extra_head = f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>\n'
            continue
        if len(keys) > 3:  # gallery
            figs = "".join(f'<a class="g-item reveal" href="{pre}{img(k)}" data-lightbox="svc" data-caption="{e(name)} – reference {i + 1}">{picture(k, f"{name} – reference photo {i + 1}", pre, "", "(max-width: 760px) 50vw, 25vw")}</a>' for i, k in enumerate(keys))
            blocks.append(f'''<section class="gallery-sec light"><div class="wrap">
  <div class="sec-head reveal">{eyebrow("Gallery")}<h2 class="h2">{e(name)} in our projects</h2><p class="muted">{len(keys)} photos – click to enlarge.</p></div>
  <div class="masonry">{figs}</div></div></section>''')
            continue
        if not title and not keys and not sec["videos"]:  # callout
            blocks.append(f'''<section class="callout-sec"><div class="wrap"><div class="callout reveal">
  <div class="callout-text">{h}</div>
  <div class="callout-actions"><a class="btn btn-light" href="{PHONE_HREF}">{icon("phone")} {PHONE}</a><a class="btn btn-ghost" href="{pre}contact.html">Contact {icon("chev")}</a></div>
</div></div></section>''')
            continue
        media = ""
        if sec["videos"]:
            media = yt(sec["videos"][0], title or name)
        elif keys:
            media = f'<a class="media-img" href="{pre}{img(keys[0])}" data-lightbox="svc-{n_img}" data-caption="{e(title or name)}">{picture(keys[0], title or name, pre, "", "(max-width: 900px) 100vw, 50vw")}</a>'
        tone = "light" if flip else ""
        cls = "feature-sec " + tone + (" flip" if flip else "") + ("" if media else " solo")
        blocks.append(f'''<section class="{cls}"><div class="wrap fs-grid">
  <div class="fs-text reveal">{eyebrow(sec.get("kicker"))}<h2 class="h2">{e(title or "")}</h2><div class="rich">{h}</div></div>
  {f'<div class="fs-media reveal">{media}</div>' if media else ""}
</div></section>''')
        flip = not flip
    others = "".join(f'<a class="chip" href="{s}.html">{icon(i2)} {e(n)}</a>' for _, s, n, _, i2 in SERVICES if s != new)
    hero_key = f"services/{old}/title" if img(f"services/{old}/title") else ("ai/hero-knx" if old == "knx-systemintegrator" and "ai/hero-knx" in IMG else f"services/{old}/card")
    body = f'''
<section class="page-hero dark media-hero">
  {picture(hero_key, name, pre, "hero-img", "100vw", eager=True)}
  <div class="hero-shade"></div>
  <div class="wrap">
    <nav class="crumbs" aria-label="Breadcrumb"><a href="{pre}index.html">Home</a>{icon("chev")}<a href="{pre}services.html">Services</a>{icon("chev")}<span>{e(name)}</span></nav>
    {eyebrow(sv["kicker"] if sv["kicker"] != sv["h1"] and sv["kicker"] != "Smart Home" else name)}
    <h1 class="display">{e(sv["h1"])}</h1>
    <div class="lead rich">{tidy(sv["intro"])}</div>
    <div class="actions"><a class="btn btn-light" href="{pre}contact.html">Request consultation</a><a class="btn btn-ghost" href="{PHONE_HREF}">{icon("phone")} {PHONE}</a></div>
  </div>
</section>
<div class="subnav"><div class="wrap subnav-in"><b>{icon(ic)} {e(name)}</b><a class="btn btn-dark btn-sm" href="{pre}contact.html">Get advice</a></div></div>
{"".join(blocks)}
<section class="more-svc"><div class="wrap">
  <div class="sec-head reveal">{eyebrow("Additional services")}<h2 class="h2">Everything from a single source.</h2></div>
  <div class="chips reveal">{others}</div>
</div></section>
{cta_band(pre)}'''
    page(f"services/{new}.html", sv["title"] if sv["title"] not in ("Alarm systems", "Smart Home", "Video surveillance", "Video intercom systems", "Multi-room audio") else f"{name} in Cologne & Mallorca – Elektro Paul Neumann",
         sv["description"], body, "KNX" if new == "knx-system-integration" else "Services", extra_head)


# ---------------------------------------------------------------- projects
def build_projects():
    pre = ""
    order = list(PROJECTS)
    cards = "".join(project_card(k, pre, "pcard-lg" if i < 2 else "") for i, k in enumerate(order))
    body = f'''
<section class="page-hero dark compact">
  <div class="wrap">
    {eyebrow("Projects")}
    <h1 class="display">A selection of our projects around Cologne and Mallorca.</h1>
    <p class="lead muted">From exclusive villas and penthouses to stadiums, studios, hotels and headquarters – electrical engineering, KNX, security, lighting, network and media technology.</p>
    <div class="filters" role="group" aria-label="Filter projects">
      <button type="button" class="filter is-on" data-filter="all">All</button>
      <button type="button" class="filter" data-filter="Residential">Residential</button>
      <button type="button" class="filter" data-filter="Commercial">Commercial</button>
    </div>
  </div>
</section>
<section class="proj-grid-sec light"><div class="wrap"><div class="proj-grid">{cards}</div></div></section>
{cta_band(pre, "Your project could be next.")}'''
    page("projects.html", "Projects – Elektro Paul Neumann, Electrician Cologne | KNX & Security Technology",
         SRC["projekt"]["description"] if "projekt" in SRC else "A selection of our projects around Cologne and Mallorca.", body, "Projects")
    for i, k in enumerate(order):
        build_project(k, order[(i - 1) % len(order)], order[(i + 1) % len(order)])


def build_project(slug, prev, nxt):
    p = SRC["projects"][slug]
    new, name, sub, cat = PROJECTS[slug]
    pre = "../"
    keys = [f"projects/{slug}/{i:02d}" for i in range(1, len(p["images"]) + 1)]
    scope_src = re.sub(r"^.*?(Implementation of|management:|Realization of)\s*", "", p["text"]) if p["text"] else ""
    figs = "".join(
        f'<a class="g-item reveal" href="{pre}{img(k)}" data-lightbox="p" data-caption="{e(name)} – photo {i + 1} of {len(keys)}">{picture(k, f"{name} – photo {i + 1}", pre, "", "(max-width: 760px) 50vw, 33vw")}</a>'
        for i, k in enumerate(keys))
    gallery = f'''<section class="gallery-sec light"><div class="wrap">
  <div class="sec-head row reveal"><div>{eyebrow("Gallery")}<h2 class="h2">{len(keys)} photos</h2></div><p class="muted">Click a photo to view it full screen.</p></div>
  <div class="masonry">{figs}</div></div></section>''' if keys else ""
    desc = p["text"] or f"{name} – a project by Elektro Paul Neumann, {sub}."
    pv, nx = PROJECTS[prev], PROJECTS[nxt]
    body = f'''
<section class="page-hero dark media-hero tall">
  {picture(f"projects/{slug}/cover", name, pre, "hero-img", "100vw", eager=True)}
  <div class="hero-shade"></div>
  <div class="wrap">
    <nav class="crumbs" aria-label="Breadcrumb"><a href="{pre}index.html">Home</a>{icon("chev")}<a href="{pre}projects.html">Projects</a>{icon("chev")}<span>{e(name)}</span></nav>
    <p class="eyebrow">{e(cat)} · {e(sub)}</p>
    <h1 class="display">{e(name)}</h1>
  </div>
</section>
<section class="proj-intro"><div class="wrap proj-intro-grid">
  <div class="reveal">{eyebrow("Scope of work")}<p class="lead">{e(p["text"]) if p["text"] else "Project details on request."}</p></div>
  <dl class="facts reveal"><div><dt>Client / project</dt><dd>{e(name)}</dd></div><div><dt>Details</dt><dd>{e(sub)}</dd></div><div><dt>Category</dt><dd>{cat}</dd></div><div><dt>Photos</dt><dd>{len(keys) or "–"}</dd></div></dl>
</div></section>
{gallery}
<section class="pager"><div class="wrap pager-grid">
  <a href="{pv[0]}.html" class="pager-link">{icon("left")}<span><small>Previous project</small><b>{e(pv[1])}</b></span></a>
  <a href="{pre}projects.html" class="pager-all">{icon("grid")}<span>All projects</span></a>
  <a href="{nx[0]}.html" class="pager-link right"><span><small>Next project</small><b>{e(nx[1])}</b></span>{icon("chev")}</a>
</div></section>
{cta_band(pre, "Planning something similar?")}'''
    page(f"projects/{new}.html", f"{name} – Project by Elektro Paul Neumann", desc, body, "Projects")


# ---------------------------------------------------------------- careers
def build_careers():
    pre = ""
    jobs = [("Construction fitter", "Realization and execution of large and small projects, property management, building and office conversions, renovations of practices, villas, houses and apartments.", "karriere/01"),
            ("Service technician", "Service and support for regular customers, video intercom systems, KNX building management systems, alarm systems, video surveillance, smart home.", "karriere/02"),
            ("Trainee (apprentice)", "Training in a future-oriented profession with innovative technology.", "karriere/03"),
            ("Helper (m/f/d)", "We are now looking for energetic helpers for our team!", "karriere/04")]
    bring = ["Completed training in electrical engineering", "Ideally, initial experience in service, project management or on construction sites",
             "Class B driving license", "Desire for long-term cooperation"]
    offer = ["Permanent position after successful probationary period", "Attractive earning opportunities", "High-quality service vehicle",
             "Thorough training and collegial cooperation", "Regular training – technical and safety-related", "Social security and a modern working environment"]
    li = lambda xs: "".join(f"<li>{e(x)}</li>" for x in xs)
    job_cards = "".join(f'''<article class="job reveal">{picture(k, t, pre, "job-img", "(max-width: 760px) 60vw, 20vw")}
<div><h3>{e(t)}</h3><p>{e(d)}</p><a class="link-more" href="mailto:{MAIL}?subject={e("Application: " + t)}">Apply now {icon("chev")}</a></div></article>''' for t, d, k in jobs)
    body = f'''
<section class="page-hero dark media-hero">
  {picture("karriere/hero", "Team at work", pre, "hero-img", "100vw", eager=True)}
  <div class="hero-shade"></div>
  <div class="wrap">
    {eyebrow("Become part of the team")}
    <h1 class="display">Career at Elektro Paul Neumann.</h1>
    <p class="lead">As a specialist company for electrical and security technology with demanding customers in Germany and Mallorca, we rely on team members who think for themselves, take responsibility – and are passionate about what they do.</p>
    <div class="actions"><a class="btn btn-light" href="#jobs">Open positions</a><a class="btn btn-ghost" href="mailto:{MAIL}">{icon("mail")} Apply by email</a></div>
  </div>
</section>
<section class="two-col">
  <div class="wrap tc-grid">
    <div class="panel reveal"><h2 class="h3">What you bring with you</h2><p class="muted">You enjoy working in a team, are reliable, flexible, and approach our customers with professionalism and friendliness. Technical understanding and manual dexterity are just as much a given for you as a willingness to develop yourself and think outside the box.</p><ul class="checks">{li(bring)}</ul></div>
    <div class="panel dark reveal"><h2 class="h3">What we offer you</h2><p class="muted">We offer you more than just a job – we offer you prospects. Look forward to a professional environment with high-quality projects, personal appreciation, and genuine future security.</p><ul class="checks">{li(offer)}</ul></div>
  </div>
  <div class="wrap narrow center reveal"><p class="lead">We also welcome career changers with technical expertise. We have been committed to training for years and can proudly look back on numerous successes.</p></div>
</section>
<section class="jobs light" id="jobs"><div class="wrap">
  <div class="sec-head reveal">{eyebrow("Open positions")}<h2 class="h2">Become part of a team that lives quality.</h2></div>
  <div class="job-grid">{job_cards}</div>
</div></section>
{cta_band(pre, "Apply now.", f"If you are interested, please send your detailed application to {MAIL}.")}'''
    page("careers.html", "Careers – Elektro Paul Neumann, KNX professional from Cologne", SRC["karriere"]["description"], body, "Careers")


# ---------------------------------------------------------------- contact
def build_contact():
    pre = ""
    body = f'''
<section class="page-hero dark compact">
  <div class="wrap">
    {eyebrow("For you in Cologne and Mallorca")}
    <h1 class="display">Contact.</h1>
    <p class="lead muted">Call us, write us an email or visit us. We look forward to your project.</p>
    <div class="actions"><a class="btn btn-light" href="{PHONE_HREF}">{icon("phone")} {PHONE}</a><a class="btn btn-ghost" href="mailto:{MAIL}">{icon("mail")} {MAIL}</a></div>
  </div>
</section>
<section class="offices light"><div class="wrap office-grid">
  <article class="office reveal">
    {picture("kontakt/01", "Cologne office", pre, "office-img", "(max-width: 900px) 100vw, 50vw")}
    <div class="office-body">
      <p class="eyebrow">Germany</p><h2 class="h3">Cologne office</h2>
      <ul class="contact-list">
        <li>{icon("pin")}<a href="{MAPS}" rel="noopener">Elektro Paul Neumann<br>Emil-Hoffmann-Straße 39-43<br>Halle 1 + 2<br>50996 Köln</a></li>
        <li>{icon("phone")}<span><a href="{PHONE_HREF}">{PHONE}</a><br><a href="{PHONE2_HREF}">{PHONE2}</a></span></li>
        <li>{icon("mail")}<a href="mailto:{MAIL}">{MAIL}</a></li>
      </ul>
      <a class="btn btn-dark btn-sm" href="{MAPS}" rel="noopener">Open in Google Maps {icon("chev")}</a>
    </div>
  </article>
  <article class="office reveal">
    {picture("kontakt/02", "Mallorca office", pre, "office-img", "(max-width: 900px) 100vw, 50vw")}
    <div class="office-body">
      <p class="eyebrow">Spain</p><h2 class="h3">Mallorca office</h2>
      <ul class="contact-list">
        <li>{icon("pin")}<span>Elektro Paul Neumann<br>Avinguda del Rei Jaume I, 109<br>07180 Santa Ponça<br>Illes Balears, Spain</span></li>
        <li>{icon("phone")}<a href="{PHONE_HREF}">{PHONE}</a></li>
        <li>{icon("mail")}<a href="mailto:{MAIL}">{MAIL}</a></li>
      </ul>
    </div>
  </article>
</div></section>
<section class="process">
  <div class="wrap">
    <div class="sec-head center reveal">{eyebrow("What happens next")}<h2 class="h2">Three steps to your project.</h2></div>
    <ol class="steps">
      <li class="reveal"><span class="step-no">01</span><h3>Idea</h3><p>Tell us about your property and your plans – by phone or email.</p></li>
      <li class="reveal"><span class="step-no">02</span><h3>Conception</h3><p>After an on-site appointment you receive a binding quote with a detailed description of the work.</p></li>
      <li class="reveal"><span class="step-no">03</span><h3>Implementation</h3><p>We install, commission and hand over – and remain your partner for service and maintenance.</p></li>
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
<section class="page-hero dark compact"><div class="wrap">{eyebrow("Legal")}<h1 class="display">Imprint &amp; privacy.</h1></div></section>
<section class="legal"><div class="wrap narrow rich">{h}</div></section>'''
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
