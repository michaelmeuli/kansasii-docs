#!/usr/bin/env python3
"""Tables of the lab numbers (TNR) in the routine Sanger file names, for docs/SANGER_LABNUMBERS.md.

Usage: sanger_labnumbers.py [DIR]   (default: ROOT/data/sanger/seq_mol_routine)
A file name starting with YYYY + 6 digits (e.g. `2014500121_clr_...ab1`) gives the lab number; the 6 digits are a
counter whose first three digits mark the workstation. Prints markdown: file counts, unique lab numbers per range and
year, and per range the most frequent marker token and the per-year min/max. Standard library only.
"""
from __future__ import annotations

import os
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "templates"))
from kansasii_paths import ROOT  # noqa: E402

ID_RE = re.compile(r"(20\d\d)(\d{6})(?!\d)[ _]*([A-Za-z0-9]+)?")


def group(counter: str) -> str:
    """Workstation range of a 6-digit counter."""
    p = int(counter[:3])
    if p == 500:
        return "500 (tbe)"
    if 333 <= p <= 343:
        return "333-343 (tbc)"
    if 176 <= p <= 185:
        return "176-185"
    if p in (186, 670, 100, 650):
        return str(p)
    if p in (316, 317):
        return "316/317"
    if 120 <= p <= 131:
        return "120-131"
    return "other"


ORDER = ["500 (tbe)", "333-343 (tbc)", "176-185", "186", "316/317", "120-131", "670", "100", "650", "other"]


def main() -> None:
    top = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(ROOT) / "data/sanger/seq_mol_routine"
    names = [f for _, _, files in os.walk(top) for f in files]
    ids: dict[tuple[str, str], set[int]] = defaultdict(set)
    tokens: dict[str, Counter[str]] = defaultdict(Counter)
    for n in names:
        m = ID_RE.match(n)
        if not m:
            continue
        year, counter, tok = m.groups()
        g = group(counter)
        ids[(g, year)].add(int(counter))
        tokens[g][(tok or "").lower()] += 1
    total = sum(len(v) for v in ids.values())
    with_id = sum(1 for n in names if ID_RE.match(n))
    print(f"Directory: `{top}`\n")
    print(f"- files: {len(names)}; starting with YYYY + 6 digits: {with_id}; unique lab numbers: {total}\n")

    years = sorted({y for _, y in ids})
    print("| year | " + " | ".join(ORDER) + " |")
    print("|---" * (len(ORDER) + 1) + "|")
    for y in years:
        print(f"| {y} | " + " | ".join(str(len(ids.get((g, y), ()))) for g in ORDER) + " |")

    print("\n| range | most frequent tokens after the number |\n|---|---|")
    for g in ORDER:
        print(f"| {g} | " + ", ".join(f"{t or '(none)'} {c}" for t, c in tokens[g].most_common(8)) + " |")

    print("\n| range | year | n | min | max |\n|---|---|---|---|---|")
    for g in ["500 (tbe)", "333-343 (tbc)", "176-185", "186", "316/317"]:
        for y in years:
            s = ids.get((g, y))
            if s and len(s) > 3:
                print(f"| {g} | {y} | {len(s)} | {min(s)} | {max(s)} |")


if __name__ == "__main__":
    main()
