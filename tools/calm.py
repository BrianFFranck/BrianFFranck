"""Make an animated card cheap to draw on phones.

GitHub shows each card as an <img>, and a phone redraws the whole card on every frame while
anything in it moves. Blur filters on moving parts make every one of those redraws expensive.
calm() keeps the look but bounds the cost:

* every looping SMIL animation keeps running until `end` seconds and then holds the frame it
  shows at that moment (end + fill="freeze"), so the card settles into one chosen still frame;
* the shared CSS loops (cursor blink, pulse, flowing dashes) run a few times and then stop;
* blur filters are removed: glowing dots get a radial-gradient halo instead, everything else
  is drawn crisp, and filter definitions that are no longer used are dropped.

It is idempotent, so it can run again on a card that was already calmed.
"""
import math
import re

_SIGMA = {"glow": 3.0, "soft": 1.6, "softU": 1.6}


def _halo(attrs, fid, close, after, defs):
    """A filtered circle redrawn as a gradient halo of the same colour (no blur needed)."""
    col = re.search(r'\bfill="(#[0-9a-fA-F]{6})"', attrs)
    r = re.search(r'\br="([\d.]+)"', attrs)
    if not col or not r or (close == ">" and re.match(r'\s*<animate[^>]*attributeName="r"', after)):
        return f"<circle{attrs}{close}"
    col, r = col.group(1).lower(), float(r.group(1))
    sig = _SIGMA.get(fid, 1.6)
    R = r + 2 * sig
    core = r / R
    gid = f"halo{col[1:]}_{round(core * 100)}"
    defs[gid] = (f'<radialGradient id="{gid}"><stop offset="{core:.2f}" stop-color="{col}"/>'
                 f'<stop offset="{(r + .8 * sig) / R:.2f}" stop-color="{col}" stop-opacity=".35"/>'
                 f'<stop offset="1" stop-color="{col}" stop-opacity="0"/></radialGradient>')
    attrs = re.sub(r'\bfill="#[0-9a-fA-F]{6}"', f'fill="url(#{gid})"', attrs)
    attrs = re.sub(r'\br="[\d.]+"', f'r="{R:.1f}"', attrs)
    return f"<circle{attrs}{close}"


def calm(svg, end):
    end = f"{end:g}s"

    # 1. looping SMIL animations: run until `end`, then hold that frame
    def hold(m):
        tag = m.group(0)
        if ' end="' in tag:
            return tag
        return tag.replace('repeatCount="indefinite"', f'repeatCount="indefinite" end="{end}" fill="freeze"')
    svg = re.sub(r'<animate(?:Transform|Motion)?\b[^>]*repeatCount="indefinite"[^>]*>', hold, svg)

    # 2. CSS loops: a few cycles, then rest (pulse stops on its bright half)
    secs = float(end[:-1])
    svg = svg.replace("steps(2,start) infinite", f"steps(2,start) {max(4, round(secs / 1.1))}")
    svg = svg.replace("2.4s ease-in-out infinite", f"2.4s ease-in-out {max(1, math.floor(secs / 2.4)) + .5:g}")
    svg = svg.replace("1s linear infinite", f"1s linear {max(2, round(secs))}")

    # 3. blur filters: halos for dots, crisp for the rest
    defs = {}
    src = svg
    svg = re.sub(r'<circle\b([^>]*?)\s*filter="url\(#(\w+)\)"([^>]*?)(/>|>)',
                 lambda m: _halo(m.group(1) + m.group(3), m.group(2), m.group(4), src[m.end():m.end() + 120], defs), svg)
    svg = re.sub(r'\s*filter="url\(#(?:glow|soft|softU)\)"', "", svg)
    for fid in re.findall(r'<filter id="(\w+)"', svg):
        if f"url(#{fid})" not in svg:
            svg = re.sub(rf'<filter id="{fid}".*?</filter>\n?', "", svg, flags=re.S)
    if defs:
        add = "".join(v for k, v in defs.items() if f'id="{k}"' not in svg)
        svg = svg.replace("</defs>", add + "\n</defs>", 1)
    return svg
