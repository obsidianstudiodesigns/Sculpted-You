"""Writes every page of the Sculpted You site, plus products.js, sitemap.xml, robots.txt and the web manifest.
Run: python tools/build.py   (run tools/make-images.py first when images change)
"""
import json
import sys
from datetime import date
from html import escape
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from catalog import CATEGORIES, GENERAL_AVOID, PRODUCTS, by_slug, label  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
ICONS = Path(__file__).parent / "icons"

NAME = "Sculpted You"
TAGLINE = "Science. Beauty. You."
BASE = "https://obsidianstudiodesigns.github.io/Sculpted-You/"
CREDIT = "https://obsidianstudiodesigns.co.za/"
SHIPPING = 100
TERMS_VERSION = "2026-11-17"
UPDATED = "17 November 2026"
# Contact details: fill these in when the client confirms them. Empty values are hidden on the site.
WHATSAPP = ""   # international format, digits only, e.g. "27821234567"
EMAIL = ""      # e.g. "orders@sculptedyou.co.za"
INSTAGRAM = ""  # full URL
FACEBOOK = ""   # full URL

P = by_slug()
CAT = {c["slug"]: c for c in CATEGORIES}
e = lambda s: escape(str(s), quote=True)
pages = []  # (path, priority) for the sitemap


def rand(n):
    return "R " + f"{n:,}".replace(",", " ")


def icon(name, cls="ic"):
    svg = (ICONS / f"{name}.svg").read_text(encoding="utf8")
    return svg.replace("<svg ", f'<svg class="{cls}" aria-hidden="true" focusable="false" ', 1)


def srcset(folder, stem, widths):
    return ", ".join(f"{{R}}assets/img/{folder}/{stem}-{w}.webp {w}w" for w in widths)


def img(folder, stem, widths, alt, sizes, cls="", eager=False, w=None, h=None):
    first = widths[-1] if eager else widths[0]
    dims = f' width="{w}" height="{h}"' if w else ""
    load = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    c = f' class="{cls}"' if cls else ""
    return (f'<img{c} src="{{R}}assets/img/{folder}/{stem}-{first}.webp" srcset="{srcset(folder, stem, widths)}" '
            f'sizes="{sizes}" alt="{e(alt)}"{dims} {load}>')


# ---------------------------------------------------------------------------------------------- layout
def head(path, title, desc, og="home", og_alt=None, ld=None, robots="index,follow,max-image-preview:large", extra=""):
    url = BASE + path
    full = title if title.endswith(NAME) or title == NAME else f"{title} | {NAME}"
    og_img = f"{BASE}assets/og/{og}.jpg"
    data = "".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>\n' for x in (ld or []))
    return f"""<!doctype html>
<html lang="en-ZA">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(full)}</title>
<meta name="description" content="{e(desc)}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{url}">
<meta name="theme-color" content="#13110f">
<meta name="color-scheme" content="dark">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{NAME}">
<meta property="og:locale" content="en_ZA">
<meta property="og:title" content="{e(full)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{og_img}">
<meta property="og:image:secure_url" content="{og_img}">
<meta property="og:image:type" content="image/jpeg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{e(og_alt or full)}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(full)}">
<meta name="twitter:description" content="{e(desc)}">
<meta name="twitter:image" content="{og_img}">
<link rel="icon" href="{{R}}favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="{{R}}favicon-32.png">
<link rel="icon" type="image/png" sizes="96x96" href="{{R}}favicon-96.png">
<link rel="apple-touch-icon" href="{{R}}apple-touch-icon.png">
<link rel="manifest" href="{{R}}site.webmanifest">
<link rel="preload" href="{{R}}assets/fonts/cormorant-garamond-500.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{{R}}assets/fonts/manrope-var.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{{R}}assets/css/site.css?v={VERSION}">
{extra}{data}</head>
"""


NAV = [("shop/", "Shop"), ("compare/glp-1/", "Compare GLP-1"), ("bmi/", "BMI check"),
       ("bloodwork/", "Bloodwork"), ("guides/", "Guides"), ("about/", "About")]


def header(path):
    links = "".join(
        f'<a href="{{R}}{h}"{" aria-current=\"page\"" if path.startswith(h) else ""}>{t}</a>' for h, t in NAV)
    cats = "".join(f'<a href="{{R}}shop/{c["slug"]}/">{c["name"]}</a>' for c in CATEGORIES)
    return f"""<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-head" data-head>
  <div class="wrap head-row">
    <a class="brand" href="{{R}}" aria-label="{NAME} home">
      <img src="{{R}}assets/img/brand/emblem-96.png" alt="" width="40" height="40">
      <span class="wordmark">Sculpted You</span>
    </a>
    <nav class="nav" aria-label="Main">{links}</nav>
    <div class="head-actions">
      <button class="icon-btn cart-btn" type="button" data-cart-open aria-label="Open cart">
        {icon("bag-simple")}<span class="cart-count" data-cart-count hidden>0</span>
      </button>
      <button class="icon-btn menu-btn" type="button" data-menu-open aria-label="Open menu" aria-expanded="false" aria-controls="menu">
        {icon("list")}
      </button>
    </div>
  </div>
</header>
<div class="menu" id="menu" data-menu hidden>
  <div class="menu-top wrap">
    <span class="wordmark">Sculpted You</span>
    <button class="icon-btn" type="button" data-menu-close aria-label="Close menu">{icon("x")}</button>
  </div>
  <nav class="menu-body wrap" aria-label="Mobile">
    <div class="menu-main">{links}</div>
    <p class="menu-label">Shop by goal</p>
    <div class="menu-cats">{cats}</div>
  </nav>
</div>
"""


def contact_links():
    out = []
    if WHATSAPP:
        out.append(f'<a href="https://wa.me/{WHATSAPP}" target="_blank" rel="noopener">{icon("whatsapp-logo")} WhatsApp</a>')
    if EMAIL:
        out.append(f'<a href="mailto:{EMAIL}">{icon("envelope-simple")} {EMAIL}</a>')
    if INSTAGRAM:
        out.append(f'<a href="{INSTAGRAM}" target="_blank" rel="noopener">{icon("instagram-logo")} Instagram</a>')
    if FACEBOOK:
        out.append(f'<a href="{FACEBOOK}" target="_blank" rel="noopener">{icon("facebook-logo")} Facebook</a>')
    return out


def footer(scripts=""):
    shop = "".join(f'<li><a href="{{R}}shop/{c["slug"]}/">{c["name"]}</a></li>' for c in CATEGORIES)
    social = "".join(f"<li>{x}</li>" for x in contact_links())
    return f"""<footer class="site-foot">
  <div class="wrap foot-grid">
    <div class="foot-brand">
      <a class="brand" href="{{R}}"><img src="{{R}}assets/img/brand/emblem-96.png" alt="" width="48" height="48" loading="lazy"><span class="wordmark">Sculpted You</span></a>
      <p class="foot-tag">{TAGLINE}</p>
      <p class="foot-note">Information on this site is general and educational. It is not medical advice and does not replace a consultation with a qualified healthcare professional. Products are sold to adults 18 and over.</p>
    </div>
    <div>
      <h2 class="foot-h">Shop</h2>
      <ul class="foot-list"><li><a href="{{R}}shop/">All peptides</a></li>{shop}</ul>
    </div>
    <div>
      <h2 class="foot-h">Help</h2>
      <ul class="foot-list">
        <li><a href="{{R}}faq/">FAQ</a></li>
        <li><a href="{{R}}shipping-returns/">Shipping and returns</a></li>
        <li><a href="{{R}}bmi/">BMI check</a></li>
        <li><a href="{{R}}bloodwork/">Bloodwork</a></li>
        <li><a href="{{R}}guides/">Guides</a></li>
        <li><a href="{{R}}contact/">Contact</a></li>
        {social}
      </ul>
    </div>
    <div>
      <h2 class="foot-h">Policies</h2>
      <ul class="foot-list">
        <li><a href="{{R}}terms/">Terms and conditions</a></li>
        <li><a href="{{R}}privacy/">Privacy policy</a></li>
        <li><a href="{{R}}disclaimer/">Health disclaimer</a></li>
        <li><a href="{{R}}cookies/">Cookie policy</a></li>
        <li><a href="{{R}}shipping-returns/">Returns policy</a></li>
      </ul>
    </div>
  </div>
  <div class="wrap foot-base">
    <p>&copy; {date.today().year} {NAME}. Prices in South African rand. Secure payments by PayFast.</p>
    <p class="credit">Designed by <a href="{CREDIT}" target="_blank" rel="noopener">Obsidian Studio Designs</a></p>
  </div>
</footer>
<aside class="drawer" data-drawer aria-label="Cart" hidden>
  <div class="drawer-scrim" data-cart-close></div>
  <div class="drawer-panel" role="dialog" aria-modal="true" aria-labelledby="cart-title">
    <div class="drawer-head">
      <h2 id="cart-title">Your cart</h2>
      <button class="icon-btn" type="button" data-cart-close aria-label="Close cart">{icon("x")}</button>
    </div>
    <div class="drawer-body" data-cart-items></div>
    <div class="drawer-foot" data-cart-foot>
      <dl class="totals">
        <div><dt>Subtotal</dt><dd data-cart-subtotal>R 0</dd></div>
        <div><dt>Courier, anywhere in South Africa</dt><dd>{rand(SHIPPING)}</dd></div>
        <div class="grand"><dt>Total</dt><dd data-cart-total>R 0</dd></div>
      </dl>
      <a class="btn btn-gold btn-block" href="{{R}}checkout/">Go to checkout</a>
      <p class="drawer-note">You'll sign a short declaration before paying.</p>
    </div>
  </div>
</aside>
<dialog class="age" data-age aria-labelledby="age-title">
  <img src="{{R}}assets/img/brand/emblem-96.png" alt="" width="64" height="64">
  <h2 id="age-title">Are you 18 or older?</h2>
  <p>This site sells peptides to adults only. Please confirm your age to continue.</p>
  <div class="age-actions">
    <button class="btn btn-gold" type="button" data-age-yes>Yes, I'm 18 or older</button>
    <a class="btn btn-ghost" href="https://www.google.com/">No, leave</a>
  </div>
</dialog>
<div class="toast" data-toast role="status" aria-live="polite"></div>
<script src="{{R}}assets/js/config.js?v={VERSION}"></script>
<script src="{{R}}assets/js/products.js?v={VERSION}"></script>
<script src="{{R}}assets/js/site.js?v={VERSION}" defer></script>
{scripts}</body>
</html>
"""


def write(path, html, priority="0.6", sitemap=True):
    depth = path.count("/")
    R = "../" * depth
    html = html.replace("{R}", R)
    assert "—" not in html and "–" not in html, f"dash in {path}"
    out = ROOT / path / "index.html" if path else ROOT / "index.html"
    if path.endswith(".html"):
        out = ROOT / path
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf8", newline="\n")
    if sitemap:
        pages.append((path, priority))


def page(path, title, desc, body, og="home", og_alt=None, ld=None, priority="0.6", scripts="", robots=None, sitemap=True):
    kw = {"robots": robots} if robots else {}
    crumbs = breadcrumb_ld(path, title)
    write(path, head(path, title, desc, og, og_alt, (ld or []) + ([crumbs] if crumbs else []), **kw) + header(path)
          + f'<main id="main">{body}</main>\n' + footer(scripts), priority, sitemap)


def breadcrumb_ld(path, title):
    if not path:
        return None
    items = [{"@type": "ListItem", "position": 1, "name": "Home", "item": BASE}]
    parts = path.strip("/").split("/")
    if parts[0] in ("shop", "product") and len(parts) > 1:
        items.append({"@type": "ListItem", "position": 2, "name": "Shop", "item": BASE + "shop/"})
    items.append({"@type": "ListItem", "position": len(items) + 1, "name": title, "item": BASE + path})
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": items}


def crumbs(*trail):
    links = [f'<a href="{{R}}">Home</a>']
    for href, text in trail[:-1]:
        links.append(f'<a href="{{R}}{href}">{e(text)}</a>')
    links.append(f'<span aria-current="page">{e(trail[-1][1])}</span>')
    return '<nav class="crumbs wrap" aria-label="Breadcrumb">' + f' {icon("caret-right", "ic sep")} '.join(links) + "</nav>"


def page_head(title, lead="", cls=""):
    lead_html = f'<p class="lead">{lead}</p>' if lead else ""
    return f'<header class="page-head wrap {cls}"><h1>{title}</h1>{lead_html}</header>'


# ---------------------------------------------------------------------------------------------- components
def product_card(p, lazy=True):
    c = CAT[p["cat"]]
    alt = f'{label(p)} vial'
    return f"""<article class="pcard" data-cat="{p['cat']}">
  <a class="pcard-media" href="{{R}}product/{p['slug']}/" tabindex="-1" aria-hidden="true">
    {img("products", p["slug"], [400, 800], alt, "(min-width: 1100px) 280px, (min-width: 700px) 30vw, 46vw", w=400, h=500)}
  </a>
  <div class="pcard-body">
    <p class="pcard-cat">{c['name']}</p>
    <h3 class="pcard-name"><a href="{{R}}product/{p['slug']}/">{e(p['name'])}</a></h3>
    <p class="pcard-strength">{e(p['strength']) or "&nbsp;"}</p>
    <div class="pcard-foot">
      <span class="price">{rand(p['price'])}</span>
      <button class="btn-add" type="button" data-add="{p['slug']}" aria-label="Add {e(label(p))} to cart">{icon("plus")}<span>Add</span></button>
    </div>
  </div>
</article>"""


def bullet_list(items, ic="check", cls="ticks"):
    return f'<ul class="{cls}">' + "".join(f"<li>{icon(ic)}<span>{e(i)}</span></li>" for i in items) + "</ul>"


def bloodwork_note(compact=False):
    return f"""<aside class="note">
  {icon("drop")}
  <div><strong>We recommend bloodwork first.</strong> A basic blood panel shows what your body is short of and gives your doctor a baseline. <a href="{{R}}bloodwork/">What to test</a></div>
</aside>"""


# ---------------------------------------------------------------------------------------------- pages
def home():
    cats = []
    for c in CATEGORIES:
        n = sum(1 for p in PRODUCTS if p["cat"] == c["slug"])
        cats.append(f"""<a class="panel" href="{{R}}shop/{c['slug']}/" data-panel>
  {img("photo", c["image"], [480, 900], "", "(min-width: 900px) 40vw, 80vw", "panel-img")}
  <span class="panel-shade"></span>
  <span class="panel-text">
    <span class="panel-name">{c['name']}</span>
    <span class="panel-tag">{c['tagline']}</span>
    <span class="panel-count">{n} peptide{'s' if n != 1 else ''}</span>
  </span>
</a>""")
    featured = [p for p in PRODUCTS if p["feature"]]
    cards = "".join(product_card(p) for p in featured)
    guides = guide_items()
    faq = faq_items(HOME_FAQ)
    org = {
        "@context": "https://schema.org", "@type": "OnlineStore", "name": NAME, "slogan": TAGLINE, "url": BASE,
        "logo": BASE + "icon-512.png", "image": BASE + "assets/og/home.jpg",
        "description": "Premium peptides for weight loss, recovery, hormones, skin and focus, couriered across South Africa.",
        "areaServed": "ZA", "currenciesAccepted": "ZAR", "paymentAccepted": "Credit card, Instant EFT (PayFast)",
    }
    site = {"@context": "https://schema.org", "@type": "WebSite", "name": NAME, "url": BASE}
    body = f"""
<section class="hero" aria-labelledby="hero-title">
  <picture class="hero-media">
    <source media="(min-width: 760px)" srcset="{srcset('photo', 'hero-wide', [960, 1600, 2400])}" sizes="100vw">
    <img src="{{R}}assets/img/photo/hero-tall-900.webp" srcset="{srcset('photo', 'hero-tall', [600, 900, 1200])}" sizes="100vw" alt="A Sculpted You peptide vial with a gold cap on black and gold marble" width="1200" height="2133" fetchpriority="high">
  </picture>
  <div class="wrap hero-inner">
    <div class="hero-copy" data-hero>
      <p class="hero-brand">{TAGLINE}</p>
      <h1 id="hero-title">Small peptides.<br>Big results.</h1>
      <p class="hero-sub">Premium peptides for weight loss, recovery, hormones, skin and focus. Every order couriered across South Africa for R100.</p>
      <div class="hero-cta">
        <a class="btn btn-gold" href="{{R}}shop/">Shop peptides</a>
        <a class="btn btn-ghost" href="{{R}}bmi/">Check your BMI</a>
      </div>
    </div>
  </div>
</section>

<section class="facts" aria-label="Why order from Sculpted You">
  <ul class="wrap facts-row">
    <li>{icon("truck")}<span>R100 courier, anywhere in South Africa</span></li>
    <li>{icon("lock-simple")}<span>Secure checkout with PayFast</span></li>
    <li>{icon("file-pdf")}<span>An info sheet for every peptide</span></li>
    <li>{icon("package")}<span>Discreet, sealed packaging</span></li>
  </ul>
</section>

<section class="section goals" aria-labelledby="goals-title">
  <div class="wrap">
    <h2 id="goals-title" class="h2">Shop by goal</h2>
    <div class="panels">{''.join(cats)}</div>
  </div>
</section>

<section class="section siblings" aria-labelledby="sib-title">
  <div class="wrap sib-grid">
    <div class="sib-copy">
      <h2 id="sib-title" class="h2">Three siblings, three strengths</h2>
      <p>Semaglutide, tirzepatide and retatrutide all act on GLP-1, the fullness hormone. Each newer sibling adds a hormone target, and with it more appetite control and fat loss.</p>
      <a class="btn btn-ghost" href="{{R}}compare/glp-1/">Compare the three</a>
    </div>
    {glp1_matrix(compact=True)}
  </div>
</section>

<section class="section featured" aria-labelledby="feat-title">
  <div class="wrap feat-head">
    <h2 id="feat-title" class="h2">Most asked for</h2>
    <div class="rail-btns">
      <button class="icon-btn" type="button" data-rail-prev aria-label="Previous products">{icon("arrow-left")}</button>
      <button class="icon-btn" type="button" data-rail-next aria-label="Next products">{icon("arrow-right")}</button>
    </div>
  </div>
  <div class="rail" data-rail tabindex="0" aria-label="Featured products">{cards}</div>
  <div class="wrap"><a class="text-link" href="{{R}}shop/">See all {len(PRODUCTS)} peptides</a></div>
</section>

<section class="band" aria-labelledby="blood-title">
  {img("photo", "bloodwork", [800, 1400], "Blood test tubes and a stethoscope on a marble counter", "100vw", "band-img")}
  <div class="wrap band-inner">
    <div class="band-card">
      <h2 id="blood-title" class="h2">Start with your bloodwork</h2>
      <p>We recommend a simple blood panel before any peptide. It shows what your body is short of and gives your doctor a baseline to measure progress against.</p>
      <a class="btn btn-gold" href="{{R}}bloodwork/">What to test</a>
    </div>
  </div>
</section>

<section class="section steps-sec" aria-labelledby="steps-title">
  <div class="wrap">
    <h2 id="steps-title" class="h2">How ordering works</h2>
    <ol class="steps">
      <li><span class="step-n">1</span><h3>Choose your peptides</h3><p>Read the info sheet, compare options and add to your cart.</p></li>
      <li><span class="step-n">2</span><h3>Sign the declaration</h3><p>Confirm you're 18 or older, accept the terms and sign before you pay.</p></li>
      <li><span class="step-n">3</span><h3>Pay with PayFast</h3><p>Card, Instant EFT and more through PayFast's secure checkout.</p></li>
      <li><span class="step-n">4</span><h3>Courier to your door</h3><p>Packed and couriered for a flat R100. We don't do collections.</p></li>
    </ol>
  </div>
</section>

<section class="section manifesto" aria-labelledby="man-title">
  <div class="wrap man-grid">
    {img("photo", "torso", [540], "A sculpted, toned body in warm light", "(min-width: 900px) 34vw, 90vw", "man-img", w=540, h=675)}
    <div class="man-copy">
      <h2 id="man-title" class="display">Science.<br>Beauty.<br>You.</h2>
      <p>Sculpted You started with one-on-one clients who wanted honest answers about peptides. The shop keeps that approach: clear information, the downsides as well as the benefits, and a strong nudge to see a doctor first.</p>
      <a class="text-link" href="{{R}}about/">Our story</a>
    </div>
  </div>
</section>

<section class="section guides-sec" aria-labelledby="guides-title">
  <div class="wrap guides-grid">
    <div>
      <h2 id="guides-title" class="h2">Free guides</h2>
      <p class="muted">Download the full info sheets, or see how to mix a vial with our step-by-step reconstitution guide.</p>
      <a class="btn btn-ghost" href="{{R}}guides/">All guides</a>
    </div>
    <ul class="guide-list">{guides}</ul>
  </div>
</section>

<section class="section faq-sec" aria-labelledby="faq-title">
  <div class="wrap faq-wrap">
    <h2 id="faq-title" class="h2">Questions, answered</h2>
    <div class="faq">{faq}</div>
    <a class="text-link" href="{{R}}faq/">More questions</a>
  </div>
</section>
"""
    page("", NAME + ": premium peptides in South Africa",
         "Premium peptides for weight loss, recovery, hormones, skin and focus. Clear info sheets, secure PayFast checkout and R100 courier anywhere in South Africa.",
         body, og="home", og_alt="Sculpted You: small peptides, big results", ld=[org, site], priority="1.0")


def glp1_matrix(compact=False):
    rows = [
        ("semaglutide-10mg", ["GLP-1"], "About 15%", "STEP 1, 68 weeks"),
        ("tirzepatide-30mg", ["GLP-1", "GIP"], "About 21%", "SURMOUNT-1, 72 weeks"),
        ("retatrutide-30mg", ["GLP-1", "GIP", "Glucagon"], "About 24%", "Phase 2, 48 weeks"),
    ]
    targets = ["GLP-1", "GIP", "Glucagon"]
    head_cells = "".join(f'<th scope="col">{t}</th>' for t in targets)
    body = ""
    for slug, has, loss, study in rows:
        p = P[slug]
        cells = "".join(
            f'<td>{icon("check", "ic yes") + "<span class=sr>Yes</span>" if t in has else "<span class=no aria-hidden=true></span><span class=sr>No</span>"}</td>'
            for t in targets)
        body += (f'<tr><th scope="row"><a href="{{R}}product/{slug}/">{p["name"]}</a></th>{cells}'
                 f'<td class="loss"><strong>{loss}</strong><small>{study}</small></td></tr>')
    note = '<p class="matrix-note">Average weight loss at the highest dose in published trials of the pharmaceutical versions. Your results will differ.</p>'
    return f"""<div class="matrix-wrap"><table class="matrix">
  <caption class="sr">Which hormone receptors each GLP-1 peptide acts on, and average trial weight loss</caption>
  <thead><tr><th scope="col">Peptide</th>{head_cells}<th scope="col">Trial weight loss</th></tr></thead>
  <tbody>{body}</tbody>
</table>{note}</div>"""


def guide_items():
    out = []
    seen = set()
    for p in PRODUCTS:
        if p.get("guide") and p["slug"] not in seen:
            seen.add(p["slug"])
            out.append((f"assets/guides/{p['slug']}-guide.pdf", f"{p['name']} guide"))
    out.append(("assets/guides/weight-loss-plateau-guide.pdf", "Weight-loss plateau guide"))
    return "".join(
        f'<li><a href="{{R}}{href}" download>{icon("file-pdf")}<span>{e(t)}</span>{icon("download-simple", "ic dl")}</a></li>'
        for href, t in out)


HOME_FAQ = [
    ("How much is delivery?", "A flat R100 courier fee on every order, anywhere in South Africa. We don't offer collections."),
    ("Why do I sign a declaration?", "Before paying, you confirm you're 18 or older, that you've read the information and terms, and that you buy at your own risk. A copy of the declaration is kept with your order."),
    ("How do I pay?", "Checkout runs through PayFast, South Africa's secure payment gateway. You can pay by card, Instant EFT and other methods PayFast offers."),
    ("Do I need to see a doctor?", "We strongly recommend it. Start with bloodwork, and discuss any peptide with a qualified healthcare professional, especially if you have a medical condition or take medication."),
    ("How should I store peptides?", "Keep unmixed vials in the fridge, away from light. Once mixed with bacteriostatic water, keep the vial refrigerated and follow the storage guidance in your info sheet."),
]

FULL_FAQ = HOME_FAQ + [
    ("What comes in my package?", "Each peptide order ships with what you need to mix it: insulin syringes, alcohol swabs, a 3 mL mixing syringe with needle, the peptide vial and a vial of bacteriostatic water. See the reconstitution guide for the full list."),
    ("How long does delivery take?", "Orders are packed after payment is confirmed and couriered to your door. Most main centres receive parcels within 2 to 4 working days. Outlying areas can take longer."),
    ("Is my order discreet?", "Yes. Parcels are sealed and plainly packed."),
    ("Can I return a product?", "Because of their nature, opened or used products can't be returned. If your order arrives damaged or incorrect, contact us within 48 hours. See the returns policy for details."),
    ("Which GLP-1 should I start with?", "Most people start with semaglutide, the gentlest and most studied. Tirzepatide and retatrutide are stronger. Compare them on our GLP-1 page and talk to your doctor."),
    ("Is my information safe?", "We collect only what we need to process your order and declaration, and we handle it under South Africa's Protection of Personal Information Act. See our privacy policy."),
]


def faq_items(items):
    return "".join(
        f'<details class="qa"><summary><span>{e(q)}</span>{icon("plus", "ic qa-ic")}</summary><p>{e(a)}</p></details>' for q, a in items)


def faq_page():
    ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FULL_FAQ]}
    body = crumbs(("faq/", "FAQ")) + page_head("Questions, answered", "Delivery, payment, storage and how ordering works.") + \
        f'<section class="section-tight"><div class="wrap narrow"><div class="faq">{faq_items(FULL_FAQ)}</div></div></section>'
    page("faq/", "FAQ", "Answers about delivery, PayFast payment, the order declaration, storage and returns at Sculpted You.", body, ld=[ld])


def shop():
    chips = '<button class="chip" type="button" data-filter="all" aria-pressed="true">All</button>' + "".join(
        f'<button class="chip" type="button" data-filter="{c["slug"]}" aria-pressed="false">{c["name"]}</button>' for c in CATEGORIES)
    cards = "".join(product_card(p) for p in PRODUCTS)
    body = crumbs(("shop/", "Shop")) + page_head("All peptides", f"{len(PRODUCTS)} peptides across five goals. Every product has a full information sheet.") + f"""
<section class="section-tight">
  <div class="wrap">
    <div class="chips" role="group" aria-label="Filter by goal">{chips}</div>
    <div class="grid" data-grid>{cards}</div>
  </div>
</section>"""
    items = {"@context": "https://schema.org", "@type": "ItemList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "url": f"{BASE}product/{p['slug']}/", "name": label(p)} for i, p in enumerate(PRODUCTS)]}
    page("shop/", "Shop all peptides", "Shop weight loss, recovery, hormone, aesthetic and brain health peptides. Prices in rand, R100 courier across South Africa.", body, ld=[items], priority="0.9")


def category(c):
    prods = [p for p in PRODUCTS if p["cat"] == c["slug"]]
    cards = "".join(product_card(p) for p in prods)
    others = "".join(f'<a class="chip" href="{{R}}shop/{o["slug"]}/">{o["name"]}</a>' for o in CATEGORIES if o is not c)
    extra = ""
    if c["slug"] == "weight-loss":
        extra = f"""<div class="callouts">
  <a class="callout" href="{{R}}compare/glp-1/">{icon("scales")}<span><strong>Semaglutide, tirzepatide or retatrutide?</strong> See how the three GLP-1 siblings compare.</span></a>
  <a class="callout" href="{{R}}bmi/">{icon("calculator")}<span><strong>Check your BMI</strong> and see which products people in your range ask about.</span></a>
</div>"""
    body = crumbs(("shop/", "Shop"), (f"shop/{c['slug']}/", c["name"])) + f"""
<header class="cat-hero wrap">
  <div class="cat-copy">
    <h1>{c['name']}</h1>
    <p class="cat-tag">{c['tagline']}</p>
    <p class="lead">{c['blurb']}</p>
  </div>
  {img("photo", c["image"], [480, 900], "", "(min-width: 900px) 34vw, 100vw", "cat-img", eager=True, w=900, h=1125)}
</header>
<section class="section-tight">
  <div class="wrap">
    {extra}
    <div class="grid">{cards}</div>
    {bloodwork_note()}
    <div class="other-cats"><span class="muted">Other goals</span><div class="chips">{others}</div></div>
  </div>
</section>"""
    items = {"@context": "https://schema.org", "@type": "ItemList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "url": f"{BASE}product/{p['slug']}/", "name": label(p)} for i, p in enumerate(prods)]}
    page(f"shop/{c['slug']}/", f"{c['name']} peptides", f"{c['title'].capitalize()} peptides: {', '.join(p['name'] for p in prods)}. Full info sheets and R100 courier across South Africa.",
         body, og=f"cat-{c['slug']}", og_alt=f"Sculpted You {c['name']} peptides", ld=[items], priority="0.8")


def product(p):
    c = CAT[p["cat"]]
    related = "".join(product_card(P[s]) for s in p["related"] if s in P)
    what = "".join(f"<p>{e(x)}</p>" for x in p["what"])
    avoid = p["avoid"] + GENERAL_AVOID
    glp = p["slug"] in ("semaglutide-10mg", "tirzepatide-30mg", "retatrutide-30mg")
    links = []
    if glp:
        links.append(f'<a class="callout" href="{{R}}compare/glp-1/">{icon("scales")}<span><strong>How does {e(p["name"])} compare?</strong> Semaglutide, tirzepatide and retatrutide side by side.</span></a>')
    if p["cat"] == "weight-loss":
        links.append(f'<a class="callout" href="{{R}}bmi/">{icon("calculator")}<span><strong>Check your BMI</strong> before choosing a weight-loss peptide.</span></a>')
    if p.get("guide"):
        links.append(f'<a class="callout" href="{{R}}assets/guides/{p["slug"]}-guide.pdf" download>{icon("file-pdf")}<span><strong>Download the full {e(p["name"])} guide</strong> PDF info sheet.</span></a>')
    links_html = f'<div class="callouts">{"".join(links)}</div>' if links else ""
    ld = {
        "@context": "https://schema.org", "@type": "Product", "name": label(p), "sku": p["slug"],
        "image": [f"{BASE}assets/img/products/{p['slug']}-800.webp"], "description": p["short"],
        "brand": {"@type": "Brand", "name": NAME}, "category": c["title"],
        "offers": {"@type": "Offer", "url": f"{BASE}product/{p['slug']}/", "priceCurrency": "ZAR", "price": f"{p['price']:.2f}",
                   "availability": "https://schema.org/InStock", "itemCondition": "https://schema.org/NewCondition",
                   "shippingDetails": {"@type": "OfferShippingDetails", "shippingRate": {"@type": "MonetaryAmount", "value": "100.00", "currency": "ZAR"},
                                       "shippingDestination": {"@type": "DefinedRegion", "addressCountry": "ZA"}}},
    }
    body = crumbs(("shop/", "Shop"), (f"shop/{c['slug']}/", c["name"]), (f"product/{p['slug']}/", p["name"])) + f"""
<section class="pdp wrap">
  <div class="pdp-media">
    {img("products", p["slug"], [400, 800], f"{label(p)} vial", "(min-width: 900px) 44vw, 100vw", eager=True, w=800, h=1000)}
  </div>
  <div class="pdp-info">
    <a class="pdp-cat" href="{{R}}shop/{c['slug']}/">{c['name']}</a>
    <h1>{e(p['name'])}</h1>
    {f'<p class="pdp-strength">{e(p["strength"])}</p>' if p['strength'] else ''}
    <p class="pdp-price">{rand(p['price'])}</p>
    <p class="pdp-short">{e(p['short'])}</p>
    <div class="buy">
      <div class="qty" data-qty>
        <button type="button" data-qty-dec aria-label="Decrease quantity">{icon("minus")}</button>
        <input type="number" min="1" max="20" value="1" inputmode="numeric" aria-label="Quantity" data-qty-input>
        <button type="button" data-qty-inc aria-label="Increase quantity">{icon("plus")}</button>
      </div>
      <button class="btn btn-gold buy-btn" type="button" data-add="{p['slug']}" data-add-qty>Add to cart</button>
    </div>
    <ul class="pdp-points">
      <li>{icon("truck")}<span>R100 courier anywhere in South Africa</span></li>
      <li>{icon("package")}<span>Ships with syringes, swabs and bacteriostatic water</span></li>
      <li>{icon("drop")}<span>We recommend <a href="{{R}}bloodwork/">bloodwork</a> before you start</span></li>
    </ul>
  </div>
</section>

<section class="section-tight">
  <div class="wrap pdp-body">
    <div class="pdp-main">
      <section class="block" aria-labelledby="what">
        <h2 id="what" class="h3">What is {e(p['name'])}?</h2>
        {what}
      </section>
      <section class="block" aria-labelledby="benefits">
        <h2 id="benefits" class="h3">Benefits</h2>
        {bullet_list(p['benefits'], 'check', 'ticks two')}
      </section>
      <section class="block" aria-labelledby="side">
        <h2 id="side" class="h3">Possible side effects</h2>
        {bullet_list(p['side'], 'warning', 'ticks warn')}
      </section>
      <div class="fit">
        <section class="fit-card" aria-labelledby="who">
          <h2 id="who" class="h4">{icon("seal-check")} Who it may suit</h2>
          <p>{e(p['who'])}</p>
        </section>
        <section class="fit-card avoid" aria-labelledby="avoid">
          <h2 id="avoid" class="h4">{icon("shield-check")} Avoid, or speak to a doctor first, if you have</h2>
          <ul>{''.join(f'<li>{e(a)}</li>' for a in avoid)}</ul>
        </section>
      </div>
      {links_html}
      {bloodwork_note()}
      <p class="fine">This information is general and educational, not medical advice. Effects differ between people. Always follow the guidance of a qualified healthcare professional. By buying you confirm you're 18 or older and accept our <a href="{{R}}terms/">terms</a>.</p>
    </div>
  </div>
</section>

<section class="section related" aria-labelledby="rel-title">
  <div class="wrap">
    <h2 id="rel-title" class="h2">Compare with</h2>
    <div class="grid grid-3">{related}</div>
  </div>
</section>
<div class="sticky-buy" data-sticky-buy hidden>
  <div><strong>{e(p['name'])}</strong><span>{rand(p['price'])}</span></div>
  <button class="btn btn-gold" type="button" data-add="{p['slug']}">Add to cart</button>
</div>
"""
    desc = f"{label(p)}: {p['short']} {rand(p['price'])}, R100 courier across South Africa."
    page(f"product/{p['slug']}/", f"{label(p)}", desc[:300], body, og=p["slug"], og_alt=f"{label(p)} by Sculpted You", ld=[ld], priority="0.8")


def compare():
    sema, tirz, reta = P["semaglutide-10mg"], P["tirzepatide-30mg"], P["retatrutide-30mg"]
    rows = [
        ("Hormone targets", "GLP-1", "GLP-1 and GIP", "GLP-1, GIP and glucagon"),
        ("How it works", "Fullness signal, slower digestion, better insulin response", "Adds GIP for stronger appetite and blood sugar control", "Adds glucagon to raise energy burn and liver fat loss"),
        ("Average trial weight loss", "About 15% (STEP 1, 68 weeks)", "About 21% (SURMOUNT-1, 72 weeks)", "About 24% (phase 2, 48 weeks)"),
        ("Status", "Approved medicine (Ozempic, Wegovy)", "Approved medicine (Mounjaro, Zepbound)", "Still in clinical trials"),
        ("Track record", "Longest, millions of users", "Several years, large trials", "Newest, least long-term data"),
        ("Stomach side effects", "Common at the start", "Common, often milder at the same stage", "Common, plus a faster heart rate"),
        ("Often chosen for", "A first GLP-1, BMI 27 to 35", "Insulin resistance, BMI 30+, or a stall on semaglutide", "BMI 35+, or a plateau on tirzepatide"),
        ("Price", rand(sema["price"]) + " (10mg)", rand(tirz["price"]) + " (30mg)", rand(reta["price"]) + " (30mg)"),
    ]
    trs = "".join(f'<tr><th scope="row">{r[0]}</th><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td></tr>' for r in rows)
    qas = [
        ("Why choose retatrutide instead of tirzepatide?",
         "Retatrutide adds a third target, glucagon, which raises the energy your body burns and helps clear liver fat. In trials it produced the largest average weight loss of the three. "
         "It's the newest, though, with the least long-term safety data, and it can raise your heart rate. People usually consider it with a high BMI or after a plateau on tirzepatide."),
        ("Why choose semaglutide instead of tirzepatide or retatrutide?",
         "Semaglutide has the longest track record and the most real-world experience. It works on one target, so it's the gentlest place to start and the most affordable. "
         "Many people reach their goal on semaglutide alone and never need to step up."),
        ("Why choose tirzepatide instead of semaglutide?",
         "Tirzepatide adds GIP to GLP-1. In head-to-head trials it gave more weight loss than semaglutide, and many people find the stomach side effects easier at the same stage. "
         "It's a common next step for anyone who stalls on semaglutide or has insulin resistance."),
        ("Can I switch between them?",
         "People do move from one to another, usually upward when results slow. A switch should be planned with your doctor, because the starting amount on the new peptide matters."),
    ]
    qa_html = "".join(f'<section class="qa-block"><h3 class="h4">{q}</h3><p>{a}</p></section>' for q, a in qas)
    cards = "".join(product_card(x) for x in (sema, tirz, reta))
    body = crumbs(("compare/glp-1/", "Compare GLP-1")) + page_head(
        "Semaglutide, tirzepatide or retatrutide?",
        "They're siblings: all three act on GLP-1, the fullness hormone. Each newer one adds a target. Here's how they differ, and why you might choose one over another.") + f"""
<section class="section-tight">
  <div class="wrap">
    {glp1_matrix()}
    <div class="table-scroll" tabindex="0" role="region" aria-label="Detailed comparison">
      <table class="compare">
        <thead><tr><th scope="col"><span class="sr">Feature</span></th><th scope="col"><a href="{{R}}product/semaglutide-10mg/">Semaglutide</a></th><th scope="col"><a href="{{R}}product/tirzepatide-30mg/">Tirzepatide</a></th><th scope="col"><a href="{{R}}product/retatrutide-30mg/">Retatrutide</a></th></tr></thead>
        <tbody>{trs}</tbody>
      </table>
    </div>
  </div>
</section>
<section class="section">
  <div class="wrap narrow">
    <h2 class="h2">Which one, and why</h2>
    {qa_html}
    <h3 class="h4 side-h">Side effects all three share</h3>
    {bullet_list(P['semaglutide-10mg']['side'], 'warning', 'ticks warn')}
    {bloodwork_note()}
    <p class="fine">Trial figures come from published studies of the pharmaceutical products (NEJM: STEP 1, 2021; SURMOUNT-1, 2022; retatrutide phase 2, 2023). They are averages at the highest studied dose and don't predict your result. This page is educational, not medical advice.</p>
  </div>
</section>
<section class="section related">
  <div class="wrap">
    <h2 class="h2">Shop the GLP-1 family</h2>
    <div class="grid grid-3">{cards}</div>
  </div>
</section>"""
    page("compare/glp-1/", "Semaglutide vs tirzepatide vs retatrutide", "How semaglutide, tirzepatide and retatrutide compare: hormone targets, trial weight loss, side effects and who each one suits.",
         body, og="cat-weight-loss", priority="0.8")


def bmi():
    body = crumbs(("bmi/", "BMI check")) + page_head("Check your BMI", "Body mass index is a quick first check. Enter your height and weight to see your range and which weight-loss peptides people in that range ask about.") + f"""
<section class="section-tight">
  <div class="wrap bmi-grid">
    <form class="bmi-form card" data-bmi novalidate>
      <div class="field">
        <label for="h">Height (cm)</label>
        <input id="h" name="h" type="number" inputmode="decimal" min="120" max="230" step="0.5" required placeholder="e.g. 168">
        <p class="err" data-err="h">Enter a height between 120 and 230 cm.</p>
      </div>
      <div class="field">
        <label for="w">Weight (kg)</label>
        <input id="w" name="w" type="number" inputmode="decimal" min="35" max="300" step="0.1" required placeholder="e.g. 82">
        <p class="err" data-err="w">Enter a weight between 35 and 300 kg.</p>
      </div>
      <button class="btn btn-gold btn-block" type="submit">Calculate my BMI</button>
      <p class="fine">{icon("lock-simple")} Calculated on your device. Nothing is saved or sent.</p>
    </form>
    <div class="bmi-result card" data-bmi-result aria-live="polite">
      <div class="bmi-empty">
        {icon("calculator", "ic big")}
        <p>Your result appears here.</p>
      </div>
    </div>
  </div>
  <div class="wrap narrow">
    <h2 class="h3 side-h">BMI ranges</h2>
    <ul class="ranges">
      <li><strong>Under 18.5</strong><span>Underweight</span></li>
      <li><strong>18.5 to 24.9</strong><span>Healthy range</span></li>
      <li><strong>25 to 29.9</strong><span>Overweight</span></li>
      <li><strong>30 to 34.9</strong><span>Obesity class 1</span></li>
      <li><strong>35 to 39.9</strong><span>Obesity class 2</span></li>
      <li><strong>40 and over</strong><span>Obesity class 3</span></li>
    </ul>
    <p class="fine">BMI doesn't account for muscle, age, sex or ethnicity. Waist size and bloodwork tell you more. GLP-1 medicines are generally considered from a BMI of 30, or 27 with a weight-related condition. Speak to a doctor before starting any weight-loss peptide.</p>
    {bloodwork_note()}
  </div>
</section>"""
    page("bmi/", "BMI calculator", "Free BMI calculator. See your BMI range and which weight-loss peptides people in that range ask about. Calculated on your device.", body, og="cat-weight-loss", priority="0.7")


def bloodwork():
    groups = [
        ("Metabolic health", ["Fasting glucose and HbA1c", "Fasting insulin", "Lipid panel (cholesterol and triglycerides)"]),
        ("Organ function", ["Liver function tests", "Kidney function (U&E and eGFR)", "Full blood count"]),
        ("Hormones", ["Thyroid (TSH and free T4)", "Testosterone or oestradiol", "IGF-1, before growth hormone peptides"]),
        ("Nutrients", ["Vitamin D", "Vitamin B12 and folate", "Iron studies (ferritin)"]),
    ]
    cards = "".join(f'<section class="test-card"><h3 class="h4">{t}</h3>{bullet_list(items, "drop", "ticks")}</section>' for t, items in groups)
    body = crumbs(("bloodwork/", "Bloodwork")) + f"""
<header class="cat-hero wrap">
  <div class="cat-copy">
    <h1>Start with your bloodwork</h1>
    <p class="lead">We can't make anyone do it, but we always recommend it. A blood panel shows what you're short of, flags anything that needs a doctor first, and gives you a baseline to measure results against.</p>
  </div>
  {img("photo", "bloodwork", [800, 1400], "Blood test tubes and a stethoscope on a dark marble counter", "(min-width: 900px) 40vw, 100vw", "cat-img wide", eager=True)}
</header>
<section class="section-tight">
  <div class="wrap">
    <h2 class="h2">What to ask for</h2>
    <p class="muted narrow-p">Ask your GP, or a pathology lab such as Lancet, PathCare or Ampath, for these tests. Many can be done from one blood draw.</p>
    <div class="tests">{cards}</div>
  </div>
</section>
<section class="section">
  <div class="wrap narrow">
    <h2 class="h2">Why it matters</h2>
    <p>Weight-loss peptides change blood sugar and digestion. Growth hormone peptides affect IGF-1 and glucose. Recovery peptides are gentler, but it still helps to know your starting point. If something comes back out of range, sort it out with your doctor before you start.</p>
    <p>Repeat the panel after a few months to see what has changed.</p>
    <a class="btn btn-gold" href="{{R}}shop/">Shop peptides</a>
  </div>
</section>"""
    page("bloodwork/", "Bloodwork before peptides", "Which blood tests to ask for before starting peptides: metabolic, organ, hormone and nutrient markers, and why they matter.", body, priority="0.7")


def guides_page():
    body = crumbs(("guides/", "Guides")) + page_head("Guides", "Full information sheets to download, and how to mix a vial.") + f"""
<section class="section-tight">
  <div class="wrap guides-page">
    <figure class="recon">
      <a href="{{R}}assets/img/photo/reconstitution-guide-1122.webp" target="_blank" rel="noopener">
        {img("photo", "reconstitution-guide", [700, 1122], "Sculpted You peptide reconstitution guide: what's in the package and six steps to mix a vial with 2 mL bacteriostatic water", "(min-width: 900px) 48vw, 100vw", w=1122, h=1402)}
      </a>
      <figcaption>Peptide reconstitution guide. Tap to open full size.</figcaption>
    </figure>
    <div>
      <h2 class="h3">Download info sheets</h2>
      <ul class="guide-list">{guide_items()}</ul>
      <h2 class="h3 side-h">Mixing a vial, in short</h2>
      <ol class="mini-steps">
        <li>Wash your hands and lay everything out on a clean surface.</li>
        <li>Wipe the rubber tops of both vials with an alcohol swab and let them dry.</li>
        <li>Draw up 2 mL of bacteriostatic water with the 3 mL syringe.</li>
        <li>Inject it slowly down the inside wall of the peptide vial.</li>
        <li>Swirl gently until the powder dissolves. Don't shake.</li>
        <li>Store the mixed vial in the fridge and use a new sterile syringe each time.</li>
      </ol>
      <p class="fine">Follow your healthcare professional's instructions for your amount and frequency.</p>
    </div>
  </div>
</section>"""
    page("guides/", "Peptide guides", "Download Sculpted You peptide information sheets and the step-by-step reconstitution guide for mixing a vial.", body, priority="0.6")


def about():
    body = crumbs(("about/", "About")) + f"""
<header class="cat-hero wrap">
  <div class="cat-copy">
    <h1>About Sculpted You</h1>
    <p class="cat-tag">{TAGLINE}</p>
    <p class="lead">Sculpted You began with one-on-one clients: people who wanted to lose weight, recover faster or feel more like themselves, and who wanted straight answers about peptides.</p>
  </div>
  {img("photo", "nutrition", [800, 1400], "A woman eating a healthy salad after training", "(min-width: 900px) 40vw, 100vw", "cat-img wide", eager=True)}
</header>
<section class="section">
  <div class="wrap narrow">
    <p>As the business grew, so did the questions. This shop is the answer: a place to read about every peptide in your own time, compare options, and order without waiting for a reply.</p>
    <p>Every product page tells you what a peptide is, what it's used for, the side effects and who should avoid it. We'd rather you read the downsides before you buy than discover them afterwards.</p>
    <h2 class="h3 side-h">What we stand for</h2>
    {bullet_list(["Clear information, including the downsides", "Bloodwork and a doctor's input before you start", "Premium, sealed products with everything you need to mix them", "Fast, discreet courier delivery across South Africa"], "seal-check", "ticks")}
    <div class="row-cta"><a class="btn btn-gold" href="{{R}}shop/">Shop peptides</a><a class="btn btn-ghost" href="{{R}}contact/">Contact us</a></div>
  </div>
</section>"""
    page("about/", "About us", "Sculpted You helps South Africans make informed choices about peptides, with clear information sheets and fast courier delivery.", body, priority="0.5")


def contact():
    links = contact_links()
    if links:
        inner = '<ul class="contact-list">' + "".join(f"<li>{x}</li>" for x in links) + "</ul>"
    else:
        inner = '<p class="muted">Our contact details are being updated. For now, please use the checkout to place an order; your confirmation is sent to the email you provide.</p>'
    body = crumbs(("contact/", "Contact")) + page_head("Contact", "Questions about a product or an order? Get in touch.") + f"""
<section class="section-tight">
  <div class="wrap narrow">
    <div class="card">{inner}</div>
    <p class="fine">We can share general product information, but we can't give medical advice. For questions about your health, speak to your doctor.</p>
  </div>
</section>"""
    page("contact/", "Contact", "Contact Sculpted You about products and orders.", body, priority="0.4")


# ---------------------------------------------------------------------------------------------- checkout
def checkout():
    provinces = ["Eastern Cape", "Free State", "Gauteng", "KwaZulu-Natal", "Limpopo", "Mpumalanga", "North West", "Northern Cape", "Western Cape"]
    opts = "".join(f"<option>{x}</option>" for x in provinces)
    body = f"""
<section class="checkout wrap" data-checkout>
  <h1 class="h2">Checkout</h1>
  <div class="test-banner" data-test-banner hidden>{icon("info")}<span><strong>Test mode.</strong> Payments go to the PayFast sandbox and no money is taken.</span></div>
  <ol class="progress" aria-label="Checkout steps">
    <li data-step-dot="1" aria-current="step"><span>1</span>Details</li>
    <li data-step-dot="2"><span>2</span>Declaration</li>
    <li data-step-dot="3"><span>3</span>Pay</li>
  </ol>
  <div class="co-grid">
    <div class="co-main">
      <div class="co-empty card" data-co-empty hidden>
        {icon("bag-simple", "ic big")}
        <h2 class="h3">Your cart is empty</h2>
        <p class="muted">Add a peptide to get started.</p>
        <a class="btn btn-gold" href="{{R}}shop/">Shop peptides</a>
      </div>

      <form class="co-step card" data-step="1" novalidate>
        <h2 class="h3">Delivery details</h2>
        <div class="two">
          <div class="field"><label for="fn">First name</label><input id="fn" name="name_first" autocomplete="given-name" required><p class="err">Enter your first name.</p></div>
          <div class="field"><label for="ln">Last name</label><input id="ln" name="name_last" autocomplete="family-name" required><p class="err">Enter your last name.</p></div>
        </div>
        <div class="two">
          <div class="field"><label for="em">Email</label><input id="em" name="email" type="email" autocomplete="email" required><p class="err">Enter a valid email address.</p></div>
          <div class="field"><label for="cell">Cellphone</label><input id="cell" name="cell" type="tel" autocomplete="tel" inputmode="tel" required pattern="^(\\+27|0)[6-8][0-9]{{8}}$" placeholder="082 123 4567"><p class="err">Enter a South African cellphone number.</p></div>
        </div>
        <div class="field"><label for="addr">Street address</label><input id="addr" name="address" autocomplete="street-address" required><p class="err">Enter your street address.</p></div>
        <div class="two">
          <div class="field"><label for="sub">Suburb</label><input id="sub" name="suburb" autocomplete="address-level3" required><p class="err">Enter your suburb.</p></div>
          <div class="field"><label for="city">City or town</label><input id="city" name="city" autocomplete="address-level2" required><p class="err">Enter your city or town.</p></div>
        </div>
        <div class="two">
          <div class="field"><label for="prov">Province</label><select id="prov" name="province" autocomplete="address-level1" required><option value="">Choose a province</option>{opts}</select><p class="err">Choose your province.</p></div>
          <div class="field"><label for="pc">Postal code</label><input id="pc" name="postal" autocomplete="postal-code" inputmode="numeric" required pattern="^[0-9]{{4}}$"><p class="err">Enter a 4-digit postal code.</p></div>
        </div>
        <div class="field"><label for="notes">Delivery notes <span class="opt">(optional)</span></label><input id="notes" name="notes" maxlength="200" placeholder="Complex name, gate code, best time"></div>
        <p class="fine">{icon("truck")} Courier only, R100 anywhere in South Africa. We don't offer collections.</p>
        <button class="btn btn-gold" type="submit">Continue to declaration</button>
      </form>

      <form class="co-step card" data-step="2" novalidate hidden>
        <h2 class="h3">Declaration</h2>
        <p class="muted">Please read the terms and sign below. A copy is kept with your order.</p>
        <div class="terms-box" tabindex="0" role="region" aria-label="Terms summary">
          <h3>Purchase declaration and terms summary</h3>
          <p>By completing this purchase, I declare that:</p>
          <ol>
            <li>I am 18 years or older and the details I've given are true.</li>
            <li>I have read the product information, including the possible side effects and who should avoid each product.</li>
            <li>I understand that the information on this website is general and educational and is not medical advice. Sculpted You recommends bloodwork and consulting a qualified healthcare professional before using any peptide.</li>
            <li>I buy these products of my own free will and at my own risk, and I accept full responsibility for how I store, prepare and use them.</li>
            <li>To the extent allowed by South African law, Sculpted You is not responsible for any consequences or side effects arising from my use of the products.</li>
            <li>I have read and accept the full <a href="{{R}}terms/" target="_blank" rel="noopener">terms and conditions</a> and <a href="{{R}}privacy/" target="_blank" rel="noopener">privacy policy</a>.</li>
          </ol>
          <p class="fine">Terms version {TERMS_VERSION}.</p>
        </div>
        <div class="field" data-id-field>
          <label for="idn">South African ID number</label>
          <input id="idn" name="id_number" inputmode="numeric" autocomplete="off" maxlength="13" required>
          <p class="hint">Used only to record your declaration. We never share it.</p>
          <p class="err" data-id-err>Enter a valid 13-digit SA ID number for someone 18 or older.</p>
        </div>
        <label class="check small"><input type="checkbox" data-passport-toggle><span>I don't have a South African ID</span></label>
        <div class="two" data-passport hidden>
          <div class="field"><label for="pp">Passport number</label><input id="pp" name="passport" autocomplete="off"><p class="err">Enter your passport number.</p></div>
          <div class="field"><label for="dob">Date of birth</label><input id="dob" name="dob" type="date"><p class="err">You must be 18 or older.</p></div>
        </div>
        <div class="field">
          <label for="sig">Signature</label>
          <div class="sig-wrap"><canvas id="sig" class="sig" data-sig aria-label="Signature pad. Draw your signature with a finger or mouse." role="img"></canvas>
          <button class="text-btn" type="button" data-sig-clear>Clear</button></div>
          <p class="hint">Sign with your finger or mouse.</p>
          <p class="err" data-sig-err>Please sign the declaration.</p>
        </div>
        <div class="field"><label for="sname">Full name, as your typed signature</label><input id="sname" name="sign_name" autocomplete="name" required><p class="err">Type your full name.</p></div>
        <div class="checks">
          <label class="check"><input type="checkbox" name="c_terms" required><span>I have read and accept the terms and conditions.</span></label>
          <label class="check"><input type="checkbox" name="c_risk" required><span>I purchase these products at my own risk and accept full responsibility for their use, including any side effects.</span></label>
          <label class="check"><input type="checkbox" name="c_doctor" required><span>I understand Sculpted You recommends bloodwork and consulting a medical professional before use.</span></label>
          <p class="err" data-checks-err>Please tick all three boxes.</p>
        </div>
        <div class="row-cta">
          <button class="btn btn-ghost" type="button" data-back="1">Back</button>
          <button class="btn btn-gold" type="submit">Sign and continue</button>
        </div>
      </form>

      <div class="co-step card" data-step="3" hidden>
        <h2 class="h3">Review and pay</h2>
        <div class="review" data-review></div>
        <p class="muted">You'll be taken to PayFast to pay securely. Your order is packed once payment is confirmed.</p>
        <div class="row-cta">
          <button class="btn btn-ghost" type="button" data-back="2">Back</button>
          <button class="btn btn-gold" type="button" data-pay>{icon("lock-simple")} Pay with PayFast</button>
        </div>
        <form data-payfast method="post" hidden></form>
      </div>
    </div>
    <aside class="co-summary card" aria-label="Order summary">
      <h2 class="h4">Order summary</h2>
      <div data-summary-items></div>
      <dl class="totals">
        <div><dt>Subtotal</dt><dd data-sum-subtotal>R 0</dd></div>
        <div><dt>Courier</dt><dd>{rand(SHIPPING)}</dd></div>
        <div class="grand"><dt>Total</dt><dd data-sum-total>R 0</dd></div>
      </dl>
      <p class="fine">{icon("lock-simple")} Payments are processed by PayFast. We never see your card details.</p>
    </aside>
  </div>
</section>"""
    scripts = '<script src="https://cdnjs.cloudflare.com/ajax/libs/blueimp-md5/2.19.0/js/md5.min.js" defer></script>\n'
    page("checkout/", "Checkout", "Secure checkout.", body, robots="noindex,follow", scripts=scripts, sitemap=False)


def order_pages():
    body = f"""<section class="section wrap narrow center" data-thanks>
  {icon("seal-check", "ic big gold")}
  <h1 class="h2">Thank you for your order</h1>
  <p class="lead">Your payment is being confirmed by PayFast. We'll pack your order and send it by courier as soon as it clears.</p>
  <div class="card review" data-thanks-summary></div>
  <p class="muted">A payment receipt is sent to your email by PayFast. Keep your order reference for any questions.</p>
  <a class="btn btn-gold" href="{{R}}shop/">Continue shopping</a>
</section>"""
    page("order/thank-you/", "Thank you", "Order received.", body, robots="noindex,nofollow", sitemap=False)
    body = f"""<section class="section wrap narrow center">
  {icon("info", "ic big")}
  <h1 class="h2">Payment cancelled</h1>
  <p class="lead">No payment was taken. Your cart is still saved, so you can try again whenever you're ready.</p>
  <div class="row-cta center"><a class="btn btn-gold" href="{{R}}checkout/">Back to checkout</a><a class="btn btn-ghost" href="{{R}}shop/">Keep shopping</a></div>
</section>"""
    page("order/cancelled/", "Payment cancelled", "Payment cancelled.", body, robots="noindex,nofollow", sitemap=False)


# ---------------------------------------------------------------------------------------------- policies
def legal(path, title, desc, sections, lead="", figure=""):
    toc = "".join(f'<li><a href="#s{i}">{e(h)}</a></li>' for i, (h, _) in enumerate(sections, 1))
    secs = "".join(f'<section id="s{i}" class="legal-sec"><h2 class="h4">{i}. {e(h)}</h2>{b}</section>' for i, (h, b) in enumerate(sections, 1))
    body = crumbs((path, title)) + page_head(title, lead or f"Last updated {UPDATED}.") + f"""
<section class="section-tight">
  <div class="wrap legal">
    <nav class="legal-toc" aria-label="On this page"><p class="menu-label">On this page</p><ol>{toc}</ol></nav>
    <div class="legal-body">{figure}{secs}</div>
  </div>
</section>"""
    page(path, title, desc, body, priority="0.3")


def contact_sentence():
    bits = []
    if EMAIL:
        bits.append(f'email <a href="mailto:{EMAIL}">{EMAIL}</a>')
    if WHATSAPP:
        bits.append(f'WhatsApp <a href="https://wa.me/{WHATSAPP}">+{WHATSAPP}</a>')
    return " or ".join(bits) if bits else 'use the details on our <a href="{R}contact/">contact page</a>'


def policies():
    c = contact_sentence()
    legal("terms/", "Terms and conditions", "The terms that apply when you use the Sculpted You website and buy from us.", [
        ("Who we are", f"<p>This website is operated by {NAME} (\"we\", \"us\"), trading in South Africa. These terms apply to every visit and every order. By using the site or placing an order you agree to them. To contact us, {c}.</p>"),
        ("Adults only", "<p>Our products are sold only to people aged 18 and over. By ordering you confirm that you are 18 or older. We may cancel any order where we believe this is not true.</p>"),
        ("Product information", "<p>Product descriptions, guides and other content on this site are general and educational. They are not medical advice, a diagnosis or a treatment plan, and they don't replace a consultation with a qualified healthcare professional. We recommend bloodwork and a doctor's input before using any peptide. Product images are for illustration.</p>"),
        ("Your declaration and own risk", "<p>Before payment you complete a declaration in which you confirm your age and identity, that you have read the product information and these terms, and that you purchase and use the products at your own risk. We keep a record of your declaration with your order.</p><p>You are responsible for storing, preparing and using products safely and as advised by your healthcare professional.</p>"),
        ("Prices and payment", "<p>Prices are shown in South African rand and include any applicable taxes. A flat courier fee of R100 is added to every order. Payment is processed by PayFast (Network International), and we never receive or store your card details. An order is accepted only once payment is confirmed. If a price is shown in error, we may cancel the order and refund you in full.</p>"),
        ("Stock", "<p>Stock is limited and subject to availability. If an item becomes unavailable after you order, we'll contact you and offer a replacement or a full refund for that item.</p>"),
        ("Delivery", '<p>We deliver by courier to addresses in South Africa only. We don\'t offer collections. Delivery times are estimates. Risk passes to you once the parcel is delivered to the address you gave. See our <a href="{R}shipping-returns/">shipping and returns policy</a>.</p>'),
        ("Returns and refunds", '<p>For health and safety reasons, opened, used or unsealed products can\'t be returned. If your order arrives damaged, incomplete or incorrect, tell us within 48 hours of delivery with photos and we\'ll replace the item or refund you. Your rights under the Consumer Protection Act are not affected.</p>'),
        ("Limitation of liability", "<p>To the extent permitted by South African law, including the Consumer Protection Act 68 of 2008, we are not liable for any loss, harm or side effect arising from the use or misuse of products bought from us, from failure to follow professional advice, or from reliance on information on this site. Nothing in these terms limits liability that cannot be limited by law, including liability for gross negligence.</p>"),
        ("Privacy", '<p>We handle your personal information as set out in our <a href="{R}privacy/">privacy policy</a>, in line with the Protection of Personal Information Act 4 of 2013 (POPIA).</p>'),
        ("Changes", f"<p>We may update these terms from time to time. The version that applies to your order is the one in force when you complete your declaration (current version: {TERMS_VERSION}).</p>"),
        ("Governing law", "<p>These terms are governed by the laws of the Republic of South Africa.</p>"),
    ])
    legal("privacy/", "Privacy policy", "How Sculpted You collects, uses and protects your personal information under POPIA.", [
        ("Overview", f"<p>{NAME} respects your privacy and processes personal information in line with the Protection of Personal Information Act 4 of 2013 (POPIA). This policy explains what we collect, why, and your rights. To contact our information officer, {c}.</p>"),
        ("What we collect", "<ul><li><strong>Order details:</strong> your name, email address, cellphone number and delivery address.</li><li><strong>Declaration details:</strong> your SA ID or passport number, date of birth, signature, typed name, the terms version you accepted and the date and time of acceptance.</li><li><strong>Payment details:</strong> handled by PayFast. We receive confirmation of payment but never your card or bank details.</li><li><strong>Device storage:</strong> your cart and age confirmation are saved in your browser's local storage on your own device.</li></ul>"),
        ("What we don't collect", "<p>The BMI calculator runs entirely in your browser. Your height, weight and result are never sent to us or saved.</p>"),
        ("Why we use it", "<p>We use your information to process and deliver your order, keep a record of your purchase declaration, communicate with you about your order, and meet our legal obligations. We don't sell your information or use it for marketing without your consent.</p>"),
        ("Who we share it with", "<ul><li><strong>PayFast</strong>, to process your payment.</li><li><strong>Our courier partner</strong>, who receives your name, cellphone number and delivery address to deliver your parcel.</li><li><strong>Service providers</strong> who host this website or store order records for us, under confidentiality obligations.</li><li><strong>Authorities</strong>, where the law requires it.</li></ul>"),
        ("Transfers outside South Africa", "<p>Some of our service providers, including our website host, store data outside South Africa. We only use providers in countries with adequate data protection laws or under agreements that protect your information as POPIA requires.</p>"),
        ("Security and retention", "<p>We take reasonable technical and organisational measures to protect your information, including restricting access to declaration records. We keep order and declaration records for as long as needed for the purposes above and as required by law (generally five years), then delete them securely.</p>"),
        ("Your rights", '<p>You may ask to see the personal information we hold about you, ask us to correct or delete it, or object to how we use it. You may also lodge a complaint with the Information Regulator (South Africa): <a href="https://inforegulator.org.za/" target="_blank" rel="noopener">inforegulator.org.za</a>.</p>'),
        ("Cookies", '<p>We don\'t use advertising or tracking cookies. See our <a href="{R}cookies/">cookie policy</a>.</p>'),
        ("Changes", "<p>We may update this policy. The latest version is always on this page.</p>"),
    ])
    legal("disclaimer/", "Health disclaimer", "Important health information about peptides sold by Sculpted You.", [
        ("Not medical advice", "<p>Everything on this website, including product pages, comparisons, the BMI calculator and downloadable guides, is general information for educational purposes. It is not medical advice and does not create a doctor-patient relationship.</p>"),
        ("Talk to a professional", "<p>Always consult a qualified healthcare professional before starting, changing or stopping any peptide, especially if you are pregnant or breastfeeding, have a medical condition, or take medication. We recommend bloodwork before you start.</p>"),
        ("Evidence varies", "<p>Some products are approved medicines elsewhere, some are in clinical trials, and some have been studied mainly in animals. Where we mention trial results, they come from published studies of specific pharmaceutical products and do not predict your result.</p>"),
        ("Side effects", "<p>All peptides can cause side effects. Stop and seek medical help if you experience severe symptoms such as intense stomach pain, chest pain, difficulty breathing, fainting or a severe allergic reaction.</p>"),
        ("Your responsibility", "<p>By buying from us you confirm you are 18 or older and that you use the products at your own risk, as set out in our terms and your purchase declaration.</p>"),
    ])
    legal("cookies/", "Cookie policy", "How the Sculpted You website uses cookies and local storage.", [
        ("No tracking cookies", "<p>This website does not use advertising, analytics or social media tracking cookies.</p>"),
        ("Local storage", "<p>We save a few small items in your browser's local storage so the site works: your cart, your age confirmation and, while you check out, your order details. They stay on your device and you can clear them at any time in your browser settings.</p>"),
        ("Third parties", "<p>When you pay, you are taken to PayFast, which may set its own cookies under its own policies.</p>"),
    ])
    legal("shipping-returns/", "Shipping and returns", "Sculpted You courier delivery and returns policy.", [
        ("Courier delivery", "<p>Every order is delivered by courier for a flat fee of R100, anywhere in South Africa. We don't offer collections.</p>"),
        ("When it ships", "<p>We pack your order once payment is confirmed. Most main centres receive parcels within 2 to 4 working days; outlying areas can take longer. You'll receive tracking details when available.</p>"),
        ("Packaging", "<p>Orders are sealed and plainly packed. Each peptide ships with insulin syringes, alcohol swabs, a 3 mL mixing syringe with needle and bacteriostatic water.</p>"),
        ("When it arrives", "<p>Put unmixed vials in the fridge as soon as your parcel arrives.</p>"),
        ("Damaged or incorrect orders", f"<p>If anything arrives damaged, incomplete or incorrect, {c} within 48 hours of delivery with your order reference and photos. We'll replace the item or refund you.</p>"),
        ("Returns", "<p>For health and safety reasons, opened, used or unsealed products can't be returned or exchanged. Your rights under the Consumer Protection Act are not affected.</p>"),
        ("Refunds", "<p>Approved refunds are paid back to your original payment method through PayFast, usually within 7 to 10 working days.</p>"),
    ], figure=img("photo", "package", [800, 1400], "A black gift box lined with gold tissue holding two peptide vials", "(min-width: 900px) 60vw, 100vw", "legal-fig"))


def not_found():
    body = f"""<section class="section wrap narrow center">
  <p class="display big404">404</p>
  <h1 class="h2">This page isn't here</h1>
  <p class="lead">It may have moved. Try the shop or head back home.</p>
  <div class="row-cta center"><a class="btn btn-gold" href="/Sculpted-You/shop/">Shop peptides</a><a class="btn btn-ghost" href="/Sculpted-You/">Home</a></div>
</section>"""
    html = head("404.html", "Page not found", "Page not found.", robots="noindex,follow") + header("") + f'<main id="main">{body}</main>' + footer()
    html = html.replace("{R}", "/Sculpted-You/")
    (ROOT / "404.html").write_text(html, encoding="utf8", newline="\n")


# ---------------------------------------------------------------------------------------------- data + seo files
def products_js():
    data = {p["slug"]: {"name": p["name"], "strength": p["strength"], "price": p["price"],
                        "img": f"assets/img/products/{p['slug']}-400.webp", "url": f"product/{p['slug']}/"} for p in PRODUCTS}
    (ROOT / "assets/js/products.js").write_text("window.SY_PRODUCTS=" + json.dumps(data, separators=(",", ":")) + ";\n", encoding="utf8", newline=chr(10))


def seo_files():
    today = date.today().isoformat()
    urls = "".join(f"<url><loc>{BASE}{p}</loc><lastmod>{today}</lastmod><priority>{pr}</priority></url>\n" for p, pr in pages)
    (ROOT / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n', encoding="utf8", newline=chr(10))
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nDisallow: /Sculpted-You/checkout/\nDisallow: /Sculpted-You/order/\n\nSitemap: {BASE}sitemap.xml\n", encoding="utf8", newline=chr(10))
    manifest = {"name": NAME, "short_name": NAME, "description": "Premium peptides, couriered across South Africa.",
                "start_url": "/Sculpted-You/", "scope": "/Sculpted-You/", "display": "standalone",
                "background_color": "#13110f", "theme_color": "#13110f",
                "icons": [{"src": "icon-192.png", "sizes": "192x192", "type": "image/png"},
                          {"src": "icon-512.png", "sizes": "512x512", "type": "image/png"},
                          {"src": "icon-maskable-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"}]}
    (ROOT / "site.webmanifest").write_text(json.dumps(manifest, indent=2), encoding="utf8", newline=chr(10))
    (ROOT / ".nojekyll").write_text("", encoding="utf8", newline=chr(10))


VERSION = date.today().strftime("%Y%m%d") + "b"

if __name__ == "__main__":
    home(); shop()
    for c in CATEGORIES:
        category(c)
    for p in PRODUCTS:
        product(p)
    compare(); bmi(); bloodwork(); guides_page(); about(); contact(); faq_page()
    checkout(); order_pages(); policies(); not_found()
    products_js(); seo_files()
    print(f"{len(pages)} indexed pages written")
