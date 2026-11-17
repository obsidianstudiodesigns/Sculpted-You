"""Builds every raster asset: photos, product vials with printed labels, favicons, emblem, social previews, guides.
Needs the originals outside the repository: ../_source/gen (generated photography), ../_source/client (from the
client's PDFs), and the client's files in the parent folder.  Run: python tools/make-images.py  (Pillow, numpy, pymupdf)
"""
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageChops

sys.path.insert(0, str(Path(__file__).parent))
from catalog import CATEGORIES, PRODUCTS  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT.parent
GEN = SRC / "_source/gen"
CLIENT = SRC / "_source/client"
IMG = ROOT / "assets/img"
OG = ROOT / "assets/og"
GUIDES = ROOT / "assets/guides"
FONTS = ROOT / "assets/fonts"
for d in (IMG / "photo", IMG / "products", IMG / "brand", OG, GUIDES):
    d.mkdir(parents=True, exist_ok=True)

ONYX = (19, 17, 15)
IVORY = (239, 233, 223)
GOLD = (207, 169, 89)
MUTE = (167, 158, 144)

SERIF = FONTS / "cormorant-garamond-600.ttf"
SERIF_IT = FONTS / "cormorant-garamond-500-italic.ttf"
SANS = FONTS / "manrope.ttf"


def font(path, size):
    return ImageFont.truetype(str(path), size)


def save_sizes(im, out, stem, widths, q=80):
    for w in widths:
        h = round(im.height * w / im.width)
        im.resize((w, h), Image.LANCZOS).save(out / f"{stem}-{w}.webp", quality=q, method=6)


def trim_white(im, thresh=245):
    a = np.asarray(im.convert("L"))
    rows = np.where(a.min(axis=1) < thresh)[0]
    cols = np.where(a.min(axis=0) < thresh)[0]
    return im.crop((cols[0], rows[0], cols[-1] + 1, rows[-1] + 1))


def fit_text(draw, text, path, max_w, start, min_size=20):
    s = start
    while s > min_size:
        f = font(path, s)
        if draw.textlength(text, font=f) <= max_w:
            return f
        s -= 2
    return font(path, min_size)


def tracked(draw, xy_center, text, f, fill, tracking):
    """Draw letter-spaced text centred on x."""
    widths = [draw.textlength(ch, font=f) for ch in text]
    total = sum(widths) + tracking * (len(text) - 1)
    x = xy_center[0] - total / 2
    for ch, w in zip(text, widths):
        draw.text((x, xy_center[1]), ch, font=f, fill=fill)
        x += w + tracking


# ------------------------------------------------------------------ photography
HERO_LABELS = {"hero-wide": (1807, 738, 365), "hero-tall": (707, 1431, 265)}  # label centre x, y and width


def branded(name, em):
    """Print the brand onto the blank label of a hero vial."""
    im = Image.open(GEN / f"{name}.jpg").convert("RGBA")
    cx, cy, w = HERO_LABELS[name]
    k = w / 365
    layer = Image.new("RGBA", im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    s = int(70 * k)
    layer.alpha_composite(em.resize((s, s), Image.LANCZOS), (int(cx - s / 2), int(cy - 120 * k)))
    tracked(d, (cx, cy - 18 * k), "SCULPTED YOU", font(SERIF, int(24 * k)), GOLD + (235,), 4 * k)
    d.line((cx - 70 * k, cy + 30 * k, cx + 70 * k, cy + 30 * k), fill=GOLD + (140,), width=max(1, int(2 * k)))
    tracked(d, (cx, cy + 46 * k), "SCIENCE. BEAUTY. YOU.", font(SANS, int(11 * k)), MUTE + (200,), 2.4 * k)
    im.alpha_composite(layer.filter(ImageFilter.GaussianBlur(0.7 * k)))
    return im.convert("RGB")


def photos(em):
    rgb = lambda p: Image.open(p).convert("RGB")
    save_sizes(branded("hero-wide", em), IMG / "photo", "hero-wide", [960, 1600, 2400], q=78)
    save_sizes(branded("hero-tall", em), IMG / "photo", "hero-tall", [600, 900, 1200], q=78)
    for name in ("bloodwork", "package"):
        save_sizes(trim_white(rgb(GEN / f"{name}.jpg")), IMG / "photo", name, [800, 1400])
    for c in CATEGORIES:
        save_sizes(rgb(GEN / f"{c['image']}.jpg"), IMG / "photo", c["image"], [480, 900])
    save_sizes(rgb(CLIENT / "torso.png"), IMG / "photo", "torso", [540])
    save_sizes(rgb(CLIENT / "nutrition.jpg"), IMG / "photo", "nutrition", [800, 1400])
    save_sizes(rgb(SRC / "WhatsApp Image 2026-11-16 at 15.05.36.jpeg"), IMG / "photo", "reconstitution-guide", [700, 1122], q=84)


# ------------------------------------------------------------------ brand
def emblem():
    """The shield emblem from the client's logo artwork, gold on transparent."""
    im = Image.open(SRC / "WhatsApp Image 2026-11-16 at 15.05.36.jpeg").convert("RGB").crop((316, 12, 416, 112))
    im = im.resize((im.width * 3, im.height * 3), Image.LANCZOS).filter(ImageFilter.UnsharpMask(2, 80, 2))
    a = np.asarray(im).astype(float)
    alpha = a.max(axis=2)
    alpha = np.clip((alpha - 18) * 1.25, 0, 255)
    safe = np.maximum(alpha, 1)[..., None] / 255
    rgb = np.clip(a / safe, 0, 255)
    out = np.dstack([rgb, alpha]).astype(np.uint8)
    em = Image.fromarray(out, "RGBA")
    em.save(IMG / "brand/emblem.png", optimize=True)
    em.resize((96, 96), Image.LANCZOS).save(IMG / "brand/emblem-96.png", optimize=True)
    return em


def monogram(size, pad=0.0, radius=0.22):
    s = size * 4
    im = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    inset = int(s * pad)
    d.rounded_rectangle((inset, inset, s - inset, s - inset), radius=int(s * radius), fill=ONYX)
    d.rounded_rectangle((inset + s * .04, inset + s * .04, s - inset - s * .04, s - inset - s * .04),
                        radius=int(s * radius * .85), outline=GOLD + (120,), width=max(2, s // 90))
    f = font(SERIF, int(s * (0.56 - pad * .9)))
    d.text((s / 2, s / 2 + s * .02), "SY", font=f, fill=GOLD, anchor="mm")
    return im.resize((size, size), Image.LANCZOS)


def favicons():
    monogram(32).save(ROOT / "favicon-32.png")
    monogram(96).save(ROOT / "favicon-96.png")
    monogram(180, radius=0).save(ROOT / "apple-touch-icon.png")
    monogram(192).save(ROOT / "icon-192.png")
    monogram(512).save(ROOT / "icon-512.png")
    monogram(512, pad=0.0, radius=0).save(ROOT / "icon-maskable-512.png")
    big = monogram(256)
    big.save(ROOT / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])


# ------------------------------------------------------------------ product vials
LABEL = (490, 735, 1100, 1500)  # label box on vial.jpg (1600x2000)


def split_name(p):
    name = p["name"]
    sub = ""
    if "(" in name:
        name, sub = name.split("(", 1)
        name, sub = name.strip(), sub.rstrip(")").strip()
    if p["slug"] == "glow-blend-70mg":
        name, sub = "Glow", "BPC-157  TB500  GHK-Cu"
    if p["slug"] == "cjc-1295-ipa":
        name, sub = "CJC-1295", "No DAC + Ipamorelin"
    return name, sub


def vial_label(p, em):
    base = Image.open(GEN / "vial.jpg").convert("RGB")
    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    x0, y0, x1, y1 = LABEL
    cx = (x0 + x1) / 2
    inner = (x1 - x0) * 0.72

    e = em.resize((92, 92), Image.LANCZOS)
    layer.alpha_composite(e, (int(cx - 46), y0 + 70))
    tracked(d, (cx, y0 + 180), "SCULPTED YOU", font(SERIF, 34), GOLD + (235,), 7)
    d.line((cx - 120, y0 + 236, cx + 120, y0 + 236), fill=GOLD + (150,), width=2)

    name, sub = split_name(p)
    fname = fit_text(d, name, SERIF, inner, 110, 44)
    d.text((cx, y0 + 360), name, font=fname, fill=IVORY + (245,), anchor="mm")
    y = y0 + 360 + fname.size * 0.62
    if sub:
        fsub = fit_text(d, sub, SANS, inner, 32, 18)
        d.text((cx, y + 18), sub, font=fsub, fill=MUTE + (230,), anchor="mm")
        y += 50
    if p["strength"]:
        fs = font(SERIF, 64)
        d.text((cx, y + 62), p["strength"], font=fs, fill=GOLD + (245,), anchor="mm")
    d.line((cx - 120, y1 - 150, cx + 120, y1 - 150), fill=GOLD + (110,), width=2)
    tracked(d, (cx, y1 - 120), "LYOPHILISED PEPTIDE", font(SANS, 22), MUTE + (210,), 4)

    layer = layer.filter(ImageFilter.GaussianBlur(0.6))
    out = base.convert("RGBA")
    out.alpha_composite(layer)
    out = out.convert("RGB")
    save_sizes(out, IMG / "products", p["slug"], [400, 800])
    return out


# ------------------------------------------------------------------ social previews (1200x630)
def og_canvas():
    return Image.new("RGB", (1200, 630), ONYX)


def og_brand(d, x, y):
    tracked(d, (x, y), "SCULPTED YOU", font(SERIF, 30), GOLD, 7)


def og_home():
    im = branded("hero-wide", emblem()).resize((1200, 675), Image.LANCZOS).crop((0, 22, 1200, 652))
    d = ImageDraw.Draw(im)
    og_brand(d, 330, 150)
    d.text((80, 230), "Small peptides.", font=font(SERIF, 86), fill=IVORY)
    d.text((80, 325), "Big results.", font=font(SERIF_IT, 86), fill=GOLD)
    d.text((82, 450), "Premium peptides, couriered across South Africa.", font=font(SANS, 30), fill=MUTE)
    im.save(OG / "home.jpg", quality=86)


def og_category(c):
    im = og_canvas()
    photo = Image.open(GEN / f"{c['image']}.jpg").convert("RGB")
    photo = photo.resize((504, 630), Image.LANCZOS)
    im.paste(photo, (696, 0))
    d = ImageDraw.Draw(im)
    og_brand(d, 300, 110)
    d.text((80, 200), c["name"], font=font(SERIF, 96), fill=IVORY)
    words, line, lines = c["tagline"].split(), "", []
    f = font(SANS, 30)
    for w in words:
        if d.textlength(line + " " + w, font=f) > 540:
            lines.append(line)
            line = w
        else:
            line = (line + " " + w).strip()
    lines.append(line)
    for i, l in enumerate(lines):
        d.text((82, 330 + i * 44), l, font=f, fill=MUTE)
    d.text((82, 520), "Shop the range", font=font(SANS, 28), fill=GOLD)
    im.save(OG / f"cat-{c['slug']}.jpg", quality=86)


def og_product(p, vial):
    im = og_canvas()
    v = vial.crop((300, 180, 1300, 1900)).resize((367, 630), Image.LANCZOS)
    im.paste(v, (760, 0))
    d = ImageDraw.Draw(im)
    og_brand(d, 300, 100)
    name, sub = split_name(p)
    f = fit_text(d, name, SERIF, 620, 96, 48)
    d.text((80, 185), name, font=f, fill=IVORY)
    y = 185 + f.size + 10
    meta = " ".join(x for x in (sub, p["strength"]) if x)
    if meta:
        d.text((82, y), meta, font=fit_text(d, meta, SANS, 620, 32, 20), fill=MUTE)
    d.text((80, 470), f"R {p['price']:,}".replace(",", " "), font=font(SERIF, 72), fill=GOLD)
    d.text((82, 560), "Courier anywhere in South Africa: R100", font=font(SANS, 24), fill=MUTE)
    im.save(OG / f"{p['slug']}.jpg", quality=86)


# ------------------------------------------------------------------ PDF guides
def guides():
    import pymupdf
    seen = set()
    for p in PRODUCTS:
        g = p.get("guide")
        if not g or g in seen:
            continue
        seen.add(g)
        out = GUIDES / f"{p['slug']}-guide.pdf"
        compress(pymupdf, SRC / g, out)
    compress(pymupdf, SRC / "Weight-Loss Plateau Guide.pdf", GUIDES / "weight-loss-plateau-guide.pdf")


def compress(pymupdf, src, out):
    if out.exists() and out.stat().st_mtime > src.stat().st_mtime:
        return
    doc = pymupdf.open(src)
    try:
        doc.rewrite_images(dpi_threshold=160, dpi_target=130, quality=70)
    except Exception as e:  # older pymupdf
        print("  rewrite_images unavailable:", e)
    doc.save(out, garbage=4, deflate=True, clean=True)
    print(f"  {out.name}: {src.stat().st_size // 1024} KB -> {out.stat().st_size // 1024} KB")


if __name__ == "__main__":
    print("brand"); em = emblem(); favicons()
    print("photos"); photos(em)
    print("social"); og_home()
    for c in CATEGORIES:
        og_category(c)
    print("vials")
    for p in PRODUCTS:
        og_product(p, vial_label(p, em))
    print("guides"); guides()
    print("done")
