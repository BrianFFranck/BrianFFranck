#!/usr/bin/env python3
"""Build the "lab notebook" profile card from the Iris experiment log.

Usage: python tools/lab_card.py path/to/experiments.md assets [README.md]

If a README is given, the sentence between <!-- lab:start --> and <!-- lab:end --> is refreshed too.

Reads the newest run from the Models table, the tiling check and the first open idea,
then writes assets/lab.svg (dark) and assets/light/lab.svg. If the log cannot be parsed
the existing card is left untouched. Standard library only.
"""
import os, re, sys, textwrap
from xml.sax.saxutils import escape

FONT = "ui-monospace,SFMono-Regular,Menlo,Consolas,'DejaVu Sans Mono','Liberation Mono',monospace"
CY, LIME, AMBER, ROSE = "#22d3ee", "#a3e635", "#fbbf24", "#fb7185"
FG, MUTED, BG, PANEL, LINE, DIM = "#d6e4ec", "#5f7385", "#070b10", "#0a121a", "#1a2a36", "#12202b"

# dark -> light palette, applied to a finished SVG (masks using #fff / #000 are left alone)
LIGHT = {
    "#070b10": "#f6f8fa", "#0a121a": "#ffffff", "#1a2a36": "#d0d7de", "#12202b": "#e1e7ed",
    "#d6e4ec": "#17212b", "#5f7385": "#57636f", "#22d3ee": "#0e7490", "#a3e635": "#4d7c0f",
    "#fbbf24": "#b45309", "#fb7185": "#be123c", "#c084fc": "#7e22ce", "#a5f3fc": "#06b6d4",
    "#0e7490": "#155e75", "#9fb8c8": "#7b8c99", "#ecfeff": "#0891b2", "#e0fbff": "#0891b2",
    "#f0fdff": "#0891b2", "#06121a": "#eef4f7", "#0b151e": "#eaeff3", "#08111a": "#eef4f7",
    "#0d2231": "#dbe4ea", "#16384a": "#c3d0d9", "#2a4a5e": "#b3c2cd", "#2b5566": "#9db1bd",
    "#a9bccb": "#57636f", "#f472b6": "#be185d", "#60a5fa": "#1d4ed8", "#818cf8": "#4338ca", "#0e2a38": "#d3e3ea",
    "#0e5a6e": "#7fb7c6", "#e6f6fb": "#17212b", "#ecfccb": "#3f6212",
}
_HEX = re.compile("|".join(re.escape(k) for k in LIGHT), re.I)


def to_light(svg_text):
    return _HEX.sub(lambda m: LIGHT[m.group(0).lower()], svg_text)


def T(x, y, size, fill, body, anchor="start", weight=400, ls=0, extra=""):
    return (f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" '
            f'font-weight="{weight}" letter-spacing="{ls}"{(" " + extra) if extra else ""}>{body}</text>')


def clean(s):
    return re.sub(r"\s+", " ", re.sub(r"[*`]", "", s)).strip()


def parse_tables(md):
    """{section title: [ {header: cell} ]} for every pipe table under a '## ' heading."""
    out, section, header = {}, None, None
    for line in md.splitlines():
        if line.startswith("## "):
            section, header = line[3:].strip(), None
            out.setdefault(section, [])
        elif line.startswith("|") and section:
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if header is None:
                header = [c.lower() for c in cells]
            elif not set("".join(cells)) <= set("-: "):
                out[section].append(dict(zip(header, cells)))
        elif not line.strip():
            header = None if not line.startswith("|") else header
    return out


def col(row, key):
    return next((v for k, v in row.items() if key in k), "")


def read_log(md):
    tabs = parse_tables(md)
    models = next((v for k, v in tabs.items() if k.lower().startswith("model")), [])
    data = next((v for k, v in tabs.items() if k.lower().startswith("data")), [])
    runs = []
    for r in models:
        q = clean(col(r, "qwk"))
        m = re.search(r"(\d\.\d+)\s*±\s*(\d\.\d+)", q)
        if not m:
            continue
        folds = re.search(r"folds?\s*([\d.\s/]+)", q)
        runs.append({
            "date": clean(col(r, "date")), "model": clean(col(r, "model")), "slides": clean(col(r, "slides")),
            "mean": float(m.group(1)), "std": float(m.group(2)),
            "folds": [float(v) for v in re.findall(r"\d\.\d+", folds.group(1))] if folds else [],
            "gg2": clean(col(r, "gg2")), "notes": clean(col(r, "notes")),
        })
    if not runs:
        return None
    blob = " ".join(clean(" ".join(r.values())) for r in data)
    til = re.search(r"Karolinska\s*([\d.]+),\s*Radboud\s*([\d.]+)", blob)
    nxt = re.search(r"^- \[ \] (.+)$", md, re.M)
    names = " ".join(r["model"].lower() for r in runs)
    stages = [("DATA", "PANDA slides", "ownload" in blob), ("TILING", "tissue tiles", "iling check" in blob),
              ("BASELINE", "mean/max pooling", bool(re.search(r"baseline|meanmax", names))),
              ("ATTENTION MIL", "learns which tiles", bool(re.search(r"abmil|attention|gated|clam", names))),
              ("BOUNDARY LOSS", "ISUP 1 vs 2", "boundary" in names)]
    return {"latest": runs[0], "best": max(runs, key=lambda r: r["mean"]), "n": len(runs),
            "tiling": til.groups() if til else None, "next": clean(nxt.group(1)) if nxt else "", "stages": stages}


def card(d):
    W, H = 1000, 430
    r, b = d["latest"], []
    b += [f'<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="8" fill="{BG}" stroke="{LINE}"/>',
          f'<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="8" fill="url(#dots)"/>',
          f'<line x1="0" y1="40" x2="{W}" y2="40" stroke="{LINE}"/>',
          f'<rect x="24" y="16" width="8" height="12" fill="{CY}" class="blink"/>',
          T(40, 26, 12, CY, "IRIS / LAB NOTEBOOK", ls=1.5),
          T(W / 2, 26, 12, MUTED, "tail -n 1 experiments.md", anchor="middle", ls=2),
          T(W - 24, 26, 12, MUTED, escape(f"LAST RUN {r['date']}"), anchor="end", ls=1.5)]

    # --- headline number
    b.append(T(30, 76, 11, CY, "LATEST RUN  ·  VALIDATION FOLDS", ls=1.5))
    b.append(T(30, 100, 14, FG, escape(r["model"]), weight=700))
    b.append(T(28, 178, 76, FG, f"{r['mean']:.2f}", weight=300, ls=2))
    b.append(T(222, 150, 20, MUTED, f"± {r['std']:.2f}"))
    b.append(T(222, 176, 12, MUTED, "QWK", ls=2))
    b.append(T(30, 208, 11, MUTED, escape(f"WEIGHTED KAPPA  ·  {len(r['folds']) or 5}-FOLD  ·  {r['slides']} SLIDES"), ls=1))
    is_best = d["best"] is r
    tag = "NUMBER TO BEAT" if d["n"] == 1 or is_best and "baseline" in r["model"].lower() else (
        "BEST SO FAR" if is_best else f"BEST SO FAR {d['best']['mean']:.2f}")
    b.append(f'<rect x="30" y="222" width="{len(tag) * 7.6 + 22:.0f}" height="22" rx="3" fill="{LIME}" fill-opacity=".1" stroke="{LIME}"/>')
    b.append(T(41, 237, 11, LIME, escape(tag), weight=700, ls=1.2))

    # --- per-fold bars
    x0, base, hmax = 392, 214, 120
    b.append(T(x0, 76, 11, MUTED, "PER FOLD", ls=1.5))
    for g in (0.25, 0.5, 0.75, 1.0):
        b.append(f'<line x1="{x0}" y1="{base - hmax * g:.1f}" x2="{x0 + 250}" y2="{base - hmax * g:.1f}" stroke="{DIM}"/>')
        b.append(T(x0 + 256, base - hmax * g + 3.5, 9.5, MUTED, f"{g:.2f}".rstrip("0").rstrip(".") if g < 1 else "1"))
    b.append(f'<line x1="{x0}" y1="{base}" x2="{x0 + 250}" y2="{base}" stroke="{LINE}"/>')
    folds = r["folds"][:8]
    if folds:
        step = 250 / len(folds)
        bw = min(30, step - 12)
        for i, v in enumerate(folds):
            x, h = x0 + step * i + (step - bw) / 2, max(2, hmax * min(v, 1))
            b.append(f'<rect x="{x:.1f}" y="{base - h:.1f}" width="{bw:.1f}" height="{h:.1f}" rx="2" fill="{CY}" fill-opacity=".85">'
                     f'<animate attributeName="height" values="0;{h:.1f}" dur=".7s" begin="{i * .12:.2f}s" fill="freeze" calcMode="spline" keySplines=".2 .7 .2 1"/>'
                     f'<animate attributeName="y" values="{base};{base - h:.1f}" dur=".7s" begin="{i * .12:.2f}s" fill="freeze" calcMode="spline" keySplines=".2 .7 .2 1"/></rect>')
            b.append(T(f"{x + bw / 2:.1f}", f"{base - h - 6:.1f}", 11, FG, f"{v:.2f}", anchor="middle", weight=700))
            b.append(T(f"{x + bw / 2:.1f}", base + 15, 9.5, MUTED, f"F{i}", anchor="middle", ls=1))
        my = base - hmax * min(r["mean"], 1)
        b.append(f'<line x1="{x0}" y1="{my:.1f}" x2="{x0 + 250}" y2="{my:.1f}" stroke="{LIME}" stroke-width="1.2" stroke-dasharray="4 4"/>')

    # --- side stats
    sx, sw = 690, 280
    bad = bool(re.match(r"0\s*/", r["gg2"]))
    stats = [("ISUP 2 SLIDES CALLED ISUP 2", escape(r["gg2"]) or "–", ROSE if bad else LIME,
              "the boundary Iris exists to fix" if bad else "the boundary Iris targets")]
    if d["tiling"]:
        stats.append(("CANCER KEPT BY TILING", f"{d['tiling'][0]} · {d['tiling'][1]}", LIME, "median recall, Karolinska · Radboud"))
    for i, (k, v, colr, hint) in enumerate(stats):
        y = 62 + 96 * i
        b.append(f'<rect x="{sx}" y="{y}" width="{sw}" height="84" rx="3" fill="{PANEL}" stroke="{LINE}"/>')
        b.append(T(sx + 14, y + 20, 10.5, MUTED, k, ls=1.2))
        b.append(T(sx + 14, y + 52, 28, colr, v, weight=700, ls=1))
        b.append(T(sx + 14, y + 72, 11, MUTED, escape(hint)))

    # --- finding + next, as plain sentences
    def lines(label, text, y, colr):
        out = [T(30, y, 11, colr, label, weight=700, ls=1.5)]
        wrapped = textwrap.wrap(text, 100)[:2]
        if len(textwrap.wrap(text, 100)) > 2:
            wrapped[1] = wrapped[1][:97].rstrip() + "…"
        for i, l in enumerate(wrapped):
            out.append(T(118, y + 18 * i, 13, FG, escape(l)))
        return out, y + 18 * max(1, len(wrapped)) + 8
    y = 276
    if r["notes"]:
        o, y = lines("FINDING", r["notes"], y, AMBER); b += o
    if d["next"]:
        o, y = lines("NEXT", d["next"], y, CY); b += o

    # --- where the project is: done, in progress, to do
    cur = next((i for i, s in enumerate(d["stages"]) if not s[2]), len(d["stages"]))
    for i, (k, v, done) in enumerate(d["stages"]):
        x = 30 + 194 * i
        now = i == cur
        edge = LIME if done else (CY if now else LINE)
        b.append(f'<rect x="{x}" y="358" width="164" height="46" rx="3" fill="{PANEL}" stroke="{edge}"'
                 f'{" stroke-width=" + chr(34) + "1.5" + chr(34) if now else ""}/>')
        if now:
            b.append(f'<rect x="{x}" y="358" width="164" height="46" rx="3" fill="{CY}" fill-opacity=".1" class="pulse"/>')
        if done:
            b.append(f'<path d="M{x + 142} 381 l5 5 l9 -10" fill="none" stroke="{LIME}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>')
        b.append(T(x + 12, 378, 13, FG if (done or now) else MUTED, k, weight=700, ls=.8))
        b.append(T(x + 12, 394, 10.5, CY if now else MUTED, "up next" if now else v))
        if i < len(d["stages"]) - 1:
            ax = x + 168
            b.append(f'<line x1="{ax}" y1="381" x2="{ax + 14}" y2="381" stroke="{LIME if done else LINE}" stroke-width="2"/>')
            b.append(f'<polygon points="{ax + 13},375 {ax + 23},381 {ax + 13},387" fill="{LIME if done else LINE}"/>')

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="{FONT}">
<defs>
<pattern id="dots" width="22" height="22" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r="0.8" fill="{DIM}"/></pattern>
<style>
  .blink{{animation:blink 1.1s steps(2,start) infinite}}
  @keyframes blink{{to{{visibility:hidden}}}}
  .pulse{{animation:pulse 2.4s ease-in-out infinite}}
  @keyframes pulse{{0%,100%{{opacity:.25}}50%{{opacity:1}}}}
</style>
</defs>
{chr(10).join(b)}
</svg>
'''


def summary(d):
    r = d["latest"]
    out = (f"<b>Where Iris is today ({escape(r['date'])}).</b> Latest run: <code>{escape(r['model'])}</code> on {escape(r['slides'])} PANDA slides, "
           f"validation QWK <b>{r['mean']:.2f} ± {r['std']:.2f}</b>")
    if r["gg2"]:
        out += f", with {escape(r['gg2'].replace(' / ', ' of '))} ISUP 2 slides called ISUP 2"
    out += "."
    if d["tiling"]:
        out += f" Tiling keeps a median {d['tiling'][0]} to {d['tiling'][1]} of the cancer tissue."
    if d["next"]:
        out += f" Next: {escape(d['next'][0].lower() + d['next'][1:])}"
    return out


def refresh_readme(path, d):
    with open(path, encoding="utf-8") as fh:
        txt = fh.read()
    new = re.sub(r"(<!-- lab:start -->).*?(<!-- lab:end -->)", lambda m: f"{m.group(1)}\n{summary(d)}\n{m.group(2)}", txt, flags=re.S)
    if new != txt:
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(new)


def main():
    src, out = sys.argv[1], sys.argv[2]
    with open(src, encoding="utf-8") as fh:
        d = read_log(fh.read())
    if d is None:
        print("no run with a 'mean ± std' QWK found; card left unchanged")
        return
    s = card(d)
    os.makedirs(os.path.join(out, "light"), exist_ok=True)
    for path, text in ((os.path.join(out, "lab.svg"), s), (os.path.join(out, "light", "lab.svg"), to_light(s))):
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(text)
    if len(sys.argv) > 3:
        refresh_readme(sys.argv[3], d)
    r = d["latest"]
    print(f"lab.svg: {r['model']} {r['date']} QWK {r['mean']:.2f} ± {r['std']:.2f}")


if __name__ == "__main__":
    main()
