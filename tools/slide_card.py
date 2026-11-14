#!/usr/bin/env python3
"""Build the "real slide" profile card: one PANDA biopsy with the tiles Iris keeps.

Run with the Iris environment (needs openslide, numpy, Pillow) from the Iris repo root:
    .venv/bin/python path/to/tools/slide_card.py <image_id> path/to/assets

The slide thumbnail and three tiles are embedded as JPEG; everything drawn on top is vector.
Slide imagery: PANDA challenge dataset (Radboud UMC and Karolinska Institutet), CC BY-SA-NC 4.0.
"""
import base64, io, os, sys

import numpy as np
import openslide
import pandas as pd
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from calm import calm
from lab_card import AMBER, BG, CY, DIM, FG, FONT, LIME, LINE, MUTED, PANEL, T, to_light

LEVEL, TILE = 1, 256  # same as iris.config.TileConfig


def jpeg(img, q=82):
    buf = io.BytesIO()
    img.convert("RGB").save(buf, "JPEG", quality=q, optimize=True)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


def main():
    image_id, out = sys.argv[1], sys.argv[2]
    row = pd.read_csv("data/tiling_check.csv").set_index("image_id").loc[image_id]
    slide = openslide.OpenSlide(f"data/panda/train_images/{image_id}.tiff")
    mask = openslide.OpenSlide(f"data/panda/train_label_masks/{image_id}_mask.tiff")
    coords = np.load(f"data/coords/{image_id}.npy")
    low = slide.level_count - 1
    down = slide.level_downsamples[low]
    thumb = slide.read_region((0, 0), low, slide.level_dimensions[low]).convert("RGB")
    labels = np.asarray(mask.read_region((0, 0), low, mask.level_dimensions[low]).convert("RGB"))[..., 0]
    tile_l0 = TILE * slide.level_downsamples[LEVEL]
    side = int(round(tile_l0 / down))

    # per tile: share of pixels the PANDA mask labels as cancer (Radboud 3/4/5, Karolinska 2)
    cancer = labels >= 3 if row.data_provider == "radboud" else labels == 2
    frac = []
    for x, y in coords:
        cx, cy = int(x / down), int(y / down)
        win = cancer[cy:cy + side, cx:cx + side]
        frac.append(float(win.mean()) if win.size else 0.0)
    frac = np.array(frac)

    W, H = 1000, 480
    PX, PY, PW = 30, 62, 600
    sc = PW / thumb.width
    PH = round(thumb.height * sc)
    b = [f'<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="8" fill="{BG}" stroke="{LINE}"/>',
         f'<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="8" fill="url(#dots)"/>',
         f'<line x1="0" y1="40" x2="{W}" y2="40" stroke="{LINE}"/>',
         f'<rect x="24" y="16" width="8" height="12" fill="{CY}" class="blink"/>',
         T(40, 26, 12, CY, "IRIS / REAL SLIDE", ls=1.5),
         T(W / 2, 26, 12, MUTED, "WHAT THE MODEL ACTUALLY SEES", anchor="middle", ls=2),
         T(W - 24, 26, 12, MUTED, f"PANDA {image_id[:8]}", anchor="end", ls=1.5)]
    big = thumb.resize((PW * 2, PH * 2), Image.LANCZOS)
    b.append(f'<image x="{PX}" y="{PY}" width="{PW}" height="{PH}" href="{jpeg(big, 80)}" preserveAspectRatio="none"/>')
    k = sc / down
    order = np.argsort(coords[:, 0])
    for n, i in enumerate(order):
        x, y = coords[i]
        col = AMBER if frac[i] > 0.02 else CY
        b.append(f'<rect x="{PX + x * k:.1f}" y="{PY + y * k:.1f}" width="{tile_l0 * k:.1f}" height="{tile_l0 * k:.1f}" '
                 f'fill="{col}" fill-opacity=".07" stroke="{col}" stroke-width="1.1">'
                 f'<animate attributeName="opacity" values="0;0;1" keyTimes="0;{n / (len(order) + 1) * .9:.3f};1" dur="2.4s" begin="0s" fill="freeze"/></rect>')
    b.append(f'<rect x="{PX}" y="{PY}" width="{PW}" height="{PH}" fill="none" stroke="{CY}" stroke-opacity=".5"/>')
    ly = PY + PH + 20
    b.append(f'<rect x="{PX}" y="{ly - 9}" width="10" height="10" fill="{CY}" fill-opacity=".15" stroke="{CY}"/>')
    b.append(T(PX + 17, ly, 10.5, MUTED, "TILE KEPT", ls=1.2))
    b.append(f'<rect x="{PX + 112}" y="{ly - 9}" width="10" height="10" fill="{AMBER}" fill-opacity=".15" stroke="{AMBER}"/>')
    b.append(T(PX + 129, ly, 10.5, MUTED, "KEPT, CANCER IN PANDA LABEL MASK (NOT A MODEL OUTPUT)", ls=1.2))

    # three real tiles at the resolution the encoder reads: most cancer, some cancer, none
    RX = 660
    with_c = [i for i in np.argsort(-frac) if frac[i] > 0.02]
    picks = [with_c[0], with_c[len(with_c) // 2], int(np.argmin(frac))] if with_c else list(np.argsort(-frac)[:3])
    b.append(T(RX, 76, 11, CY, "THREE OF ITS TILES  ·  256 PX AT ~5×", ls=1.5))
    for n, i in enumerate(picks):
        x, y = coords[i]
        tile = slide.read_region((int(x), int(y)), LEVEL, (TILE, TILE)).convert("RGB").resize((192, 192), Image.LANCZOS)
        tx = RX + 105 * n
        col = AMBER if frac[i] > 0.02 else CY
        b.append(f'<image x="{tx}" y="88" width="96" height="96" href="{jpeg(tile, 84)}"/>')
        b.append(f'<rect x="{tx}" y="88" width="96" height="96" fill="none" stroke="{col}" stroke-width="1.5"/>')
        b.append(T(tx, 201, 10, col, f"{frac[i] * 100:.0f}% CANCER" if frac[i] > 0.02 else "NO CANCER", weight=700, ls=1))
    grade = int(row.isup_grade)
    stats = [("ISUP GRADE", str(grade), FG), ("TILES KEPT", str(int(row.tiles)), CY),
             ("TISSUE KEPT", f"{row.tissue_recall:.2f}", LIME), ("CANCER KEPT", f"{row.cancer_recall:.2f}", LIME)]
    for n, (kk, v, col) in enumerate(stats):
        x, y = RX + 157 * (n % 2), 222 + 58 * (n // 2)
        b.append(f'<rect x="{x}" y="{y}" width="149" height="48" rx="3" fill="{PANEL}" stroke="{LINE}"/>')
        b.append(T(x + 10, y + 17, 10.5, MUTED, kk, ls=1.2))
        b.append(T(x + 10, y + 38, 17, col, v, weight=700))
    for n, l in enumerate(["One label for the whole slide, dozens of", "tiles. Iris has to learn which ones matter."]):
        b.append(T(RX, 358 + 18 * n, 12.5, FG, l))
    b.append(f'<line x1="30" y1="{H - 62}" x2="{W - 30}" y2="{H - 62}" stroke="{LINE}"/>')
    b.append(T(30, H - 40, 11, MUTED, f"Real biopsy from the PANDA challenge dataset ({row.data_provider.capitalize()}), tissue mask and tiling by Iris."))
    b.append(T(30, H - 22, 11, MUTED, "Slide imagery: Radboud UMC and Karolinska Institutet, CC BY-SA-NC 4.0. Research use only, not a medical device."))
    b.append(f'<path d="M{W - 14} {H - 26} V{H - 14} H{W - 26}" fill="none" stroke="{CY}" stroke-width="1.5"/>')

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="{FONT}">
<defs>
<pattern id="dots" width="22" height="22" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r="0.8" fill="{DIM}"/></pattern>
<style>
  .blink{{animation:blink 1.1s steps(2,start) infinite}}
  @keyframes blink{{to{{visibility:hidden}}}}
</style>
</defs>
{chr(10).join(b)}
</svg>
'''
    svg = calm(svg)
    os.makedirs(os.path.join(out, "light"), exist_ok=True)
    for path, text in ((os.path.join(out, "slide.svg"), svg), (os.path.join(out, "light", "slide.svg"), to_light(svg))):
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(text)
    print(f"slide.svg {len(svg) / 1024:.0f} KB, panel {PW}x{PH}, {len(coords)} tiles, {int((frac > 0.02).sum())} with cancer")


if __name__ == "__main__":
    main()
