#!/usr/bin/env python3
"""Assemble the tiered editions from books/v2/tiers/<tier>/*.md.

Each tier's chapter files are its editable sources; the assembled file
books/coherent-biblical-ontology-<tier>.md is the published manuscript and
the input to the EPUB build. Image paths in chapters are relative to books/
(for example v2/figures/fig-tcr.png), as in the second edition.

Run: python3 books/v2/tools/assemble_tiers.py [--check]
--check exits non-zero if any assembled file is out of date.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

BOOKS = Path(__file__).resolve().parents[2]
TIERS = ("beginner", "intermediate", "a-level")


def parts(tier: str) -> list[Path]:
    return sorted((BOOKS / "v2" / "tiers" / tier).glob("[0-9][0-9]-*.md"))


def out(tier: str) -> Path:
    return BOOKS / f"coherent-biblical-ontology-{tier}.md"


def assemble(tier: str) -> str:
    chunks = [p.read_text(encoding="utf-8").strip() for p in parts(tier)]
    if not chunks:
        raise SystemExit(f"no chapter files for tier {tier}")
    text = "\n\n---\n\n".join(chunks) + "\n"
    for m in re.finditer(r"!\[[^\]]*\]\(([^)]+)\)", text):
        if not (BOOKS / m.group(1)).exists():
            raise SystemExit(f"missing image in {tier}: {m.group(1)}")
    return text


def main() -> int:
    stale = []
    for tier in TIERS:
        text = assemble(tier)
        target = out(tier)
        if "--check" in sys.argv:
            current = target.read_text(encoding="utf-8") if target.exists() else ""
            if current != text:
                stale.append(target.name)
            continue
        target.write_text(text, encoding="utf-8")
        print(f"wrote {target.relative_to(BOOKS.parent)} ({len(text.split())} words from {len(parts(tier))} parts)")
    if stale:
        print(f"out of date: {', '.join(stale)}; run assemble_tiers.py", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
