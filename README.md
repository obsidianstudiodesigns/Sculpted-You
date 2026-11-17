# Sculpted You

Online store and information site for Sculpted You: premium peptides, couriered across South Africa. "Science. Beauty. You."

Live: https://obsidianstudiodesigns.github.io/Sculpted-You/

Static site on GitHub Pages from `main`. The Python tools only run on your machine.

## Change products, prices or copy
1. Edit `tools/catalog.py` (categories, products, prices, benefits, side effects, who it suits).
2. Run `python tools/make-images.py` if you added a product (it prints the name on the vial label and makes the WhatsApp preview), then `python tools/build.py`.
3. Commit and push.

Contact details (WhatsApp, email, Instagram, Facebook) are constants at the top of `tools/build.py`. Empty values are hidden.

## Checkout and PayFast
`assets/js/config.js` holds the PayFast settings. It ships in sandbox mode with PayFast's public test merchant, so the whole checkout can be tried without real money. Going live needs the client's own merchant ID and key, `sandbox: false`, and, for a passphrase and payment notifications (ITN), a small server function, because a passphrase must never sit in public JavaScript. The signed declaration is shown on the review step; `declarationEndpoint` sends it to a secure endpoint once one exists.

## Images
`tools/make-images.py` builds every raster asset from originals kept outside this repository in `../_source/` (generated photography and images from the client's PDF guides) and the client's files in the parent folder. It needs Pillow, numpy and pymupdf, plus TTF copies of the fonts in `assets/fonts/` (convert the woff2 files with fontTools).

Site by [Obsidian Studio Designs](https://obsidianstudiodesigns.co.za/).
