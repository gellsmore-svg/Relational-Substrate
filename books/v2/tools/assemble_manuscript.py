#!/usr/bin/env python3
"""Assemble the second-edition manuscript from books/v2/manuscript/*.md.

The chapter files are the editable sources; the assembled file
books/coherent-biblical-ontology-second-edition.md is the published
manuscript and the input to the EPUB build. Image paths in chapters are
relative to books/ (for example v2/figures/fig-tcr.png).

Run: python3 books/v2/tools/assemble_manuscript.py [--check]
--check exits non-zero if the assembled file is out of date.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

BOOKS = Path(__file__).resolve().parents[2]
PARTS = sorted((BOOKS / "v2" / "manuscript").glob("[0-9][0-9]-*.md"))
OUT = BOOKS / "coherent-biblical-ontology-second-edition.md"


def assemble() -> str:
    chunks = [p.read_text(encoding="utf-8").strip() for p in PARTS]
    text = "\n\n---\n\n".join(chunks) + "\n"
    for m in re.finditer(r"!\[[^\]]*\]\(([^)]+)\)", text):
        if not (BOOKS / m.group(1)).exists():
            raise SystemExit(f"missing image: {m.group(1)}")
    return text


def main() -> int:
    text = assemble()
    if "--check" in sys.argv:
        current = OUT.read_text(encoding="utf-8") if OUT.exists() else ""
        if current != text:
            print(f"{OUT.name} is out of date; run assemble_manuscript.py", file=sys.stderr)
            return 1
        return 0
    OUT.write_text(text, encoding="utf-8")
    print(f"wrote {OUT.relative_to(BOOKS.parent)} ({len(text.split())} words from {len(PARTS)} parts)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
