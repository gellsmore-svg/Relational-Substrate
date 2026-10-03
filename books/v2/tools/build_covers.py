#!/usr/bin/env python3
"""Generate the second-edition front and back covers as editable SVG.

Concept (from the book's recurring scene): a shaft of morning light enters
from darkness and makes visible a fine field of relations; where the light
falls, a stone rests within the field. Darkness, differentiation, relation
and transmission, without decorative technical imagery.

Outputs books/v2/covers/{front,back}-cover.svg and, if cairosvg is
importable, the PNG renderings used by the EPUB (1600x2400).
Deterministic: a fixed seed reproduces the artwork exactly.
"""

from __future__ import annotations

import math
import random
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parents[1] / "covers"
W, H = 1600, 2400
SERIF = "DejaVu Serif, Georgia, 'Times New Roman', serif"


def field(seed: int, beam: tuple[float, float, float, float]) -> tuple[list[str], list[tuple[float, float]]]:
    """Relational field: jittered lattice points joined to near neighbours.

    Lines inside the beam are drawn lit; outside it they are barely visible.
    """
    rnd = random.Random(seed)
    pts = []
    step = 92
    for gy in range(-1, H // step + 2):
        for gx in range(-1, W // step + 2):
            x = gx * step + rnd.uniform(-34, 34) + (gy % 2) * step / 2
            y = gy * step + rnd.uniform(-34, 34)
            pts.append((x, y))
    bx0, by0, bx1, by1 = beam

    def light(x, y):
        # distance from the beam's axis, normalised; 1 at the axis, 0 far away
        dx, dy = bx1 - bx0, by1 - by0
        t = ((x - bx0) * dx + (y - by0) * dy) / (dx * dx + dy * dy)
        px, py = bx0 + t * dx, by0 + t * dy
        d = math.hypot(x - px, y - py)
        width = 170 + 260 * max(0.0, min(1.0, t))
        if t > 1.02 or t < -0.05:
            return 0.0
        return max(0.0, 1 - d / width) * max(0.0, min(1.0, 0.25 + t))

    lines = []
    for i, (x, y) in enumerate(pts):
        near = sorted(((math.hypot(x - u, y - v), j) for j, (u, v) in enumerate(pts) if j != i))[:3]
        for dist, j in near:
            if j < i or dist > 150:
                continue
            u, v = pts[j]
            mx, my = (x + u) / 2, (y + v) / 2
            lv = light(mx, my)
            if my > 1700:
                lv = 0.0
            cx = mx + rnd.uniform(-14, 14)
            cy = my + rnd.uniform(-14, 14)
            if lv > 0.04:
                op = 0.10 + 0.62 * lv
                col = "#f2e3bd"
                sw = 1.1 + 1.6 * lv
            else:
                op, col, sw = 0.07, "#8fa0b8", 1.0
            lines.append(f'<path d="M{x:.1f},{y:.1f} Q{cx:.1f},{cy:.1f} {u:.1f},{v:.1f}" '
                         f'stroke="{col}" stroke-opacity="{op:.3f}" stroke-width="{sw:.2f}" fill="none"/>')
    nodes = []
    for x, y in pts:
        lv = light(x, y)
        if lv > 0.25 and y < 1700:
            nodes.append((x, y, lv))
    dots = [f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{2.2 + 3.2 * lv:.2f}" fill="#f6e7c1" fill-opacity="{0.25 + 0.6 * lv:.2f}"/>'
            for x, y, lv in nodes]
    return lines + dots, [(x, y) for x, y, _ in nodes]


def base(seed: int, beam, extra: str) -> str:
    parts, _ = field(seed, beam)
    bx0, by0, bx1, by1 = beam
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <defs>
    <linearGradient id="night" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#0c0e14"/><stop offset="0.55" stop-color="#151a24"/><stop offset="1" stop-color="#231d18"/>
    </linearGradient>
    <linearGradient id="beam" x1="{bx0/W:.3f}" y1="{by0/H:.3f}" x2="{bx1/W:.3f}" y2="{by1/H:.3f}">
      <stop offset="0" stop-color="#fff4d6" stop-opacity="0.32"/><stop offset="0.6" stop-color="#e9cf93" stop-opacity="0.12"/><stop offset="1" stop-color="#e9cf93" stop-opacity="0.02"/>
    </linearGradient>
    <radialGradient id="glow" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="#f3dfa8" stop-opacity="0.35"/><stop offset="1" stop-color="#f3dfa8" stop-opacity="0"/></radialGradient>
    <linearGradient id="stone" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#9c9890"/><stop offset="0.6" stop-color="#6d6a65"/><stop offset="1" stop-color="#3d3b39"/></linearGradient>
  </defs>
  <rect width="{W}" height="{H}" fill="url(#night)"/>
  <polygon points="{bx0-60},{by0-120} {bx0+150},{by0-160} {bx1+330},{by1+60} {bx1-260},{by1+140}" fill="url(#beam)"/>
  <g>{''.join(parts)}</g>
  {extra}
</svg>
"""


def text(x, y, s, size, colour="#efe6d2", weight="normal", anchor="middle", style="normal", spacing=0):
    return (f'<text x="{x}" y="{y}" font-family="{SERIF}" font-size="{size}" fill="{colour}" font-weight="{weight}" '
            f'font-style="{style}" text-anchor="{anchor}" letter-spacing="{spacing}">{escape(s)}</text>')


def front() -> str:
    beam = (120, 140, 980, 1520)
    stone = ('<ellipse cx="1010" cy="1590" rx="230" ry="60" fill="url(#glow)"/>'
             '<path d="M842,1572 C850,1500 930,1462 1012,1466 C1100,1470 1172,1508 1180,1566 '
             'C1186,1606 1120,1626 1012,1628 C902,1630 838,1610 842,1572 Z" fill="url(#stone)"/>'
             '<path d="M900,1520 C960,1540 1020,1530 1110,1548" stroke="#c9c3b6" stroke-opacity="0.55" stroke-width="5" fill="none"/>')
    t = [
        text(W / 2, 1880, "COHERENT", 96, weight="bold", spacing=10),
        text(W / 2, 1995, "BIBLICAL ONTOLOGY", 92, weight="bold", spacing=4),
        f'<line x1="560" y1="2050" x2="1040" y2="2050" stroke="#d6b875" stroke-width="2.5"/>',
        text(W / 2, 2118, "Second Edition", 50, colour="#d6b875", style="italic"),
        text(W / 2, 2196, "A relational creation: physical order, life, persons", 38, colour="#cfc5b0"),
        text(W / 2, 2246, "and restoration under Scripture", 38, colour="#cfc5b0"),
        text(W / 2, 2340, "gellsmore-svg", 36, colour="#a99f8c", spacing=4),
    ]
    shade = '<rect x="0" y="1720" width="1600" height="680" fill="#0c0e14" fill-opacity="0.55"/>'
    return base(2026_10, beam, stone + shade + "".join(t))


BACK = [
    "This second edition of Coherent Biblical Ontology begins",
    "where Scripture begins, with God creating a world that is",
    "really there, and asks what that world is made of.",
    "",
    "Its answer is that created physical reality is relational",
    "from its foundation. Possibility is shaped before anything",
    "happens; what happens unfolds by constrained chance; things",
    "persist by preserving what they are; and a difference here",
    "becomes a consequence there through transmission, carriage",
    "and reception. Mathematics describes this order with",
    "extraordinary precision without being the order itself.",
    "",
    "Because the material world is relational at its base, the",
    "relational life Scripture describes (promise, consequence,",
    "responsibility, love) is not bolted onto an alien world.",
    "Yet material, living, personal and spiritual realities",
    "remain distinct: relation across categories does not",
    "erase category, and creation is not God.",
    "",
    "The book is not an empirical proof of ultimate ontology.",
    "It is an argument for the most globally coherent account",
    "available, honest about evidence, uncertainty and",
    "revelation, and governed throughout by Scripture.",
]


def back() -> str:
    beam = (1480, 160, 760, 1300)
    lines = [text(W / 2, 330, "COHERENT BIBLICAL ONTOLOGY", 56, weight="bold", spacing=6),
             text(W / 2, 398, "Second Edition", 40, colour="#d6b875", style="italic")]
    y = 560
    for ln in BACK:
        if ln:
            lines.append(text(215, y, ln, 38, colour="#ebe2cd", anchor="start"))
        y += 62 if ln else 40
    lines += [f'<line x1="560" y1="{y + 40}" x2="1040" y2="{y + 40}" stroke="#d6b875" stroke-width="2"/>',
              text(W / 2, y + 120, "A free electronic edition and the full research record:", 32, colour="#c9bfa8"),
              text(W / 2, y + 172, "relational-substrate.blogspot.com", 34, colour="#e8d6a6"),
              text(W / 2, y + 220, "github.com/gellsmore-svg/Relational-Substrate", 34, colour="#e8d6a6")]
    shade = '<rect x="140" y="220" width="1320" height="1950" rx="24" fill="#0c0e14" fill-opacity="0.84"/>'
    return base(2026_11, beam, shade + "".join(lines))


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for name, svg in (("front-cover", front()), ("back-cover", back())):
        p = OUT / f"{name}.svg"
        p.write_text(svg, encoding="utf-8")
        try:
            import cairosvg  # optional; PNGs are committed so builds need not render
            cairosvg.svg2png(url=str(p), write_to=str(OUT / f"{name}.png"), output_width=W, output_height=H)
            print("rendered", name)
        except ImportError:
            print("wrote", p.name, "(cairosvg not available; PNG not regenerated)")


if __name__ == "__main__":
    main()
