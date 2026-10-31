#!/usr/bin/env python3
"""Generate front covers for the tiered editions as editable SVG.

Reuses the second-edition artwork (morning light, a field of relations, the
stone) with a different seed per tier, so each edition is recognisably part
of the family without being identical.

Outputs books/v2/tiers/covers/<tier>-front.svg and, if cairosvg is
importable, the PNG used by the EPUB (1600x2400).
"""

from __future__ import annotations

from pathlib import Path

from build_covers import H, W, base, text

OUT = Path(__file__).resolve().parents[1] / "tiers" / "covers"

TIERS = {
    "beginner": (2026_21, "Beginner's Edition", ("The world God made,", "and what it really is")),
    "intermediate": (2026_22, "Intermediate Edition", ("A Scripture-first account", "of a relational creation")),
    "a-level": (2026_23, "A-Level Edition", ("A relational creation: physical order, life,", "persons and restoration under Scripture")),
}


def front(seed: int, label: str, sub: tuple[str, str]) -> str:
    beam = (120, 140, 980, 1520)
    stone = ('<ellipse cx="1010" cy="1590" rx="230" ry="60" fill="url(#glow)"/>'
             '<path d="M842,1572 C850,1500 930,1462 1012,1466 C1100,1470 1172,1508 1180,1566 '
             'C1186,1606 1120,1626 1012,1628 C902,1630 838,1610 842,1572 Z" fill="url(#stone)"/>'
             '<path d="M900,1520 C960,1540 1020,1530 1110,1548" stroke="#c9c3b6" stroke-opacity="0.55" stroke-width="5" fill="none"/>')
    t = [
        text(W / 2, 1880, "COHERENT", 96, weight="bold", spacing=10),
        text(W / 2, 1995, "BIBLICAL ONTOLOGY", 92, weight="bold", spacing=4),
        '<line x1="560" y1="2050" x2="1040" y2="2050" stroke="#d6b875" stroke-width="2.5"/>',
        text(W / 2, 2118, label, 50, colour="#d6b875", style="italic"),
        text(W / 2, 2196, sub[0], 38, colour="#cfc5b0"),
        text(W / 2, 2246, sub[1], 38, colour="#cfc5b0"),
        text(W / 2, 2340, "gellsmore-svg", 36, colour="#a99f8c", spacing=4),
    ]
    shade = '<rect x="0" y="1720" width="1600" height="680" fill="#0c0e14" fill-opacity="0.55"/>'
    return base(seed, beam, stone + shade + "".join(t))


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for tier, (seed, label, sub) in TIERS.items():
        p = OUT / f"{tier}-front.svg"
        p.write_text(front(seed, label, sub), encoding="utf-8")
        try:
            import cairosvg  # optional; PNGs are committed so builds need not render
            cairosvg.svg2png(url=str(p), write_to=str(OUT / f"{tier}-front.png"), output_width=W, output_height=H)
            print("rendered", tier)
        except ImportError:
            print("wrote", p.name, "(cairosvg not available; PNG not regenerated)")


if __name__ == "__main__":
    main()
