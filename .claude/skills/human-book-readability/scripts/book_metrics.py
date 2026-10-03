#!/usr/bin/env python3
"""Low-level readability evidence for long-form Markdown books.

Produces indicators, not verdicts. Surface formulas (Flesch) are reported only
as low-level signals; see ../REFERENCE.md for why they are not comprehension
scores.

Terms file (optional, JSON): either a list of strings, or
  {"terms": [{"id": "tcr", "term": "Transmit-Carry-Receive",
              "aliases": ["T-C-R", "TCR"], "requires": ["relation"]}]}
"requires" lists prerequisite term ids; the script reports any term whose first
use precedes a prerequisite's first use.

Usage:
  book_metrics.py BOOK.md [--terms terms.json] [--level 1] [--out report.md]
"""

from __future__ import annotations

import argparse
import bisect
import json
import re
import statistics
import sys
from dataclasses import dataclass, field

STOP = set("""a an the and or but if then so of to in on at by for with from as is are was
were be been being it its this that these those there here which who whom whose what
when where why how not no nor than too very can could may might must shall should will
would do does did done have has had having he she they them their his her we our you
your i me my one ones also such into onto over under about between through within
without upon more most less least all any both each few other some only own same just
because while whether yet ever every""".split())

META = re.compile(r"\b(this (chapter|section|book) (will|has|argues|shows|establishes|does)|"
                  r"as (we|the reader) (saw|will see)|in (the|this) (next|previous|following) chapter)\b", re.I)
NOT_BUT = re.compile(r"\bnot\b[^.;:!?]{1,60}?\bbut\b", re.I)
PRONOUN_START = re.compile(r"^(this|that|it|these|those|such)\b", re.I)
CONNECTIVE_START = re.compile(r"^(but|so|therefore|because|yet|however|thus|hence|and|then|"
                              r"this means|that is|for|instead|still|again|first|second|finally)\b", re.I)


def syllables(word: str) -> int:
    w = word.lower().strip("'")
    if not w:
        return 0
    groups = re.findall(r"[aeiouy]+", w)
    n = len(groups)
    if w.endswith("e") and n > 1 and not w.endswith(("le", "ee")):
        n -= 1
    return max(1, n)


def words(text: str) -> list[str]:
    return re.findall(r"[A-Za-z][A-Za-z'\-]*", text)


def sentences(text: str) -> list[str]:
    parts = re.split(r"(?<=[.!?])\s+(?=[A-Z\"'`(*])", text)
    return [p for p in (s.strip() for s in parts) if len(words(p)) > 0]


def strip_markup(md: str) -> str:
    md = re.sub(r"```.*?```", " ", md, flags=re.S)
    md = re.sub(r"`([^`]*)`", r"\1", md)
    md = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", md)
    md = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", md)
    md = re.sub(r"[*_]{1,3}", "", md)
    return md


@dataclass
class Section:
    title: str
    start_word: int
    body: str
    paragraphs: list[str] = field(default_factory=list)


def split_sections(md: str, level: int) -> list[Section]:
    pat = re.compile(r"^(#{1,%d})\s+(.*)$" % level, re.M)
    secs: list[Section] = []
    last, title = 0, "(front matter)"
    for m in pat.finditer(md):
        secs.append(Section(title, 0, md[last:m.start()]))
        title, last = m.group(2).strip(), m.end()
    secs.append(Section(title, 0, md[last:]))
    count = 0
    out = []
    for s in secs:
        s.start_word = count
        clean = strip_markup(s.body)
        s.paragraphs = [p.strip() for p in re.split(r"\n\s*\n", clean)
                        if p.strip() and not p.strip().startswith(("#", "|", ">"))]
        count += len(words(clean))
        if words(clean):
            out.append(s)
    return out


def content_set(text: str) -> set[str]:
    return {w.lower() for w in words(text) if len(w) > 3 and w.lower() not in STOP}


def load_terms(path: str | None):
    if not path:
        return []
    data = json.load(open(path, encoding="utf-8"))
    items = data["terms"] if isinstance(data, dict) else data
    terms = []
    for it in items:
        if isinstance(it, str):
            it = {"id": it, "term": it}
        names = [it["term"], *it.get("aliases", [])]
        rx = re.compile(r"(?<![A-Za-z])(" + "|".join(re.escape(n) for n in names) + r")(?![A-Za-z])", re.I)
        terms.append({"id": it.get("id", it["term"]), "term": it["term"], "rx": rx,
                      "requires": it.get("requires", [])})
    return terms


def analyse(md: str, level: int, terms):
    secs = split_sections(md, level)
    full_clean = strip_markup(md)
    total_words = len(words(full_clean))
    rows = []
    for s in secs:
        clean = strip_markup(s.body)
        ws = words(clean)
        prose = "\n".join(p for p in s.paragraphs if not re.match(r"^[-*\d]+[.)]?\s", p))
        sents = sentences(prose)
        lens = [len(words(x)) for x in sents] or [0]
        syl = sum(syllables(w) for w in words(prose))
        nw = max(1, len(words(prose)))
        ns = max(1, len(sents))
        flesch = 206.835 - 1.015 * (nw / ns) - 84.6 * (syl / nw)
        overlaps, zero = [], 0
        pron = 0
        for i, p in enumerate(s.paragraphs):
            if PRONOUN_START.match(p):
                pron += 1
            if i:
                a, b = content_set(s.paragraphs[i - 1]), content_set(p)
                ov = len(a & b) / max(1, min(len(a), len(b)))
                overlaps.append(ov)
                if not (a & b) and not CONNECTIVE_START.match(p):
                    zero += 1
        lines = s.body.splitlines()
        bullets = sum(1 for ln in lines if re.match(r"^\s*([-*]|\d+\.)\s", ln))
        nonblank = max(1, sum(1 for ln in lines if ln.strip()))
        term_hits = sum(len(t["rx"].findall(clean)) for t in terms)
        rows.append({
            "title": s.title, "words": len(ws), "sentences": len(sents),
            "mean_sent": round(statistics.mean(lens), 1),
            "p90_sent": sorted(lens)[int(0.9 * (len(lens) - 1))],
            "long_sent": sum(1 for x in lens if x > 40),
            "flesch": round(flesch, 1),
            "term_density": round(100 * term_hits / max(1, len(ws)), 2),
            "overlap": round(statistics.mean(overlaps), 2) if overlaps else None,
            "zero_overlap_starts": zero, "pronoun_starts": pron,
            "bullet_share": round(bullets / nonblank, 2),
            "emdash_per_k": round(1000 * s.body.count("—") / max(1, len(ws)), 2),
            "not_but": len(NOT_BUT.findall(clean)), "meta": len(META.findall(clean)),
        })
    term_rows = []
    first_use = {}
    word_starts = [m.start() for m in re.finditer(r"[A-Za-z][A-Za-z'\-]*", full_clean)]
    for t in terms:
        positions = [bisect.bisect_left(word_starts, m.start()) for m in t["rx"].finditer(full_clean)]
        if positions:
            gaps = [b - a for a, b in zip(positions, positions[1:])]
            first_use[t["id"]] = positions[0]
            sec = next((s.title for s in reversed(secs) if s.start_word <= positions[0]), "?")
            term_rows.append({"id": t["id"], "uses": len(positions), "first_word": positions[0],
                              "first_section": sec, "max_gap": max(gaps) if gaps else 0})
        else:
            term_rows.append({"id": t["id"], "uses": 0, "first_word": None,
                              "first_section": "-", "max_gap": None})
    order_violations = []
    for t in terms:
        for req in t["requires"]:
            if t["id"] in first_use and req in first_use and first_use[req] > first_use[t["id"]]:
                order_violations.append((t["id"], req, first_use[t["id"]], first_use[req]))
            elif t["id"] in first_use and req not in first_use:
                order_violations.append((t["id"], req, first_use[t["id"]], None))
    return total_words, rows, term_rows, order_violations


def render(path, total, rows, term_rows, viol) -> str:
    out = [f"# Readability metrics: `{path}`", "",
           f"Total words: {total}. Indicators only; see the skill's REFERENCE.md.", "",
           "| Section | Words | Mean sent | P90 | >40w | Flesch* | Term/100w | Adj. overlap | Zero-overlap starts | Pronoun starts | Bullets | Em-dash/k | not…but | Meta |",
           "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|"]
    for r in rows:
        out.append("| {title} | {words} | {mean_sent} | {p90_sent} | {long_sent} | {flesch} | {term_density} | "
                   "{overlap} | {zero_overlap_starts} | {pronoun_starts} | {bullet_share} | {emdash_per_k} | "
                   "{not_but} | {meta} |".format(**{k: ("–" if v is None else v) for k, v in r.items()}))
    out += ["", "*Flesch Reading Ease is a surface indicator, not a comprehension measure.", ""]
    if term_rows:
        out += ["## Terms", "", "| Term | Uses | First word | First section | Max reactivation gap (words) |",
                "|---|---:|---:|---|---:|"]
        for t in term_rows:
            out.append(f"| {t['id']} | {t['uses']} | {t['first_word'] if t['first_word'] is not None else '–'} | "
                       f"{t['first_section']} | {t['max_gap'] if t['max_gap'] is not None else '–'} |")
        out.append("")
    out += ["## Prerequisite-order violations", ""]
    if viol:
        for a, b, pa, pb in viol:
            out.append(f"- `{a}` first used at word {pa} before prerequisite `{b}` "
                       f"({'never used' if pb is None else 'first used at word ' + str(pb)})")
    else:
        out.append("- none detected")
    return "\n".join(out) + "\n"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("book")
    ap.add_argument("--terms")
    ap.add_argument("--level", type=int, default=1, help="heading level at which to split sections")
    ap.add_argument("--out")
    ap.add_argument("--json", action="store_true", help="emit JSON instead of Markdown")
    a = ap.parse_args(argv)
    md = open(a.book, encoding="utf-8").read()
    total, rows, term_rows, viol = analyse(md, a.level, load_terms(a.terms))
    if a.json:
        text = json.dumps({"total_words": total, "sections": rows, "terms": term_rows,
                           "order_violations": viol}, indent=2)
    else:
        text = render(a.book, total, rows, term_rows, viol)
    if a.out:
        open(a.out, "w", encoding="utf-8").write(text)
    else:
        sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
