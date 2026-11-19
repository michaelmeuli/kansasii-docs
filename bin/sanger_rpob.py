#!/usr/bin/env python3
"""Which rpoB region a routine Sanger file covers, from its file name; tables for docs/SANGER_RPOB.md.

Usage: sanger_rpob.py [DIR]          (default: ROOT/data/sanger/seq_mol_routine)
       sanger_rpob.py --list [DIR]   (tab-separated: region, check, path; one line per rpoB file)

The name is reduced to its marker/primer part (lab number, run date/time, well and extension removed) and matched
against the rules in REGIONS, first match wins. Every .seq/.fasta read is then checked for the M. tuberculosis RRDR
(81-bp core) so that the name rules can be judged against the sequence. Standard library only.
"""
from __future__ import annotations

import os
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "templates"))
from kansasii_paths import ROOT  # noqa: E402

# Files that belong to any rpoB assay: the name says rpo, or carries a primer of a TB rpoB assay without "rpoB".
SELECT = re.compile(r"rpo|(?<![A-Za-z])TR\s?\d|(?<!\d)81\s?bp|Tb176(?!\d)", re.I)
SKIP = re.compile(r"^~\$|\.(phd\.\d+|db)$", re.I)
READ_EXT = re.compile(r"\.(ab1|seq|fasta)$", re.I)

# Leading lab number (YYYY + 6 digits, typo variants, old 6-digit numbers), run suffix, extension.
LAB = re.compile(r"^\d{5,11}(-\d\d)?(?=[_ A-Za-z]|$)")
SUFFIX = re.compile(r"([_ ]\d{4}-\d\d-\d\d(_\d\d-\d\d-\d\d|_\d+)_[A-H]\d\d)?(_Peaktraced)?\.(ab1|seq|fasta)$", re.I)

# (region, rule); first match wins. The order matters: e.g. `rpoB_R_TR2b` is TR, not the NTM reverse read.
REGIONS: list[tuple[str, re.Pattern[str]]] = [
    ("other genus", re.compile(r"strep|univ|GrpoB", re.I)),
    ("NTM: M. abscessus (MAB)", re.compile(r"MAB", re.I)),
    ("NTM: M. marinum (RPO_F/R)", re.compile(r"marinum", re.I)),
    ("Mtb: 5' region (Tb176)", re.compile(r"Tb176(?!\d)", re.I)),
    ("Mtb: Xpert region (F1/F2/R2)", re.compile(r"genexpert|rpoB-?[FR]\d(?!\d)", re.I)),
    ("Mtb: RRDR 81 bp (TR1/TR2b)", re.compile(r"(?<!\d)81(?!\d)|TR\s?\d|core|mut|rpoBc", re.I)),
    ("NTM: 2573f/3337r", re.compile(r"25[67][2-5]|573f|258f|3?337r|myco", re.I)),
    ("NTM: no primer in name", re.compile(r"")),
]
XPERT = "Mtb: Xpert region (F1/F2/R2)"

# M. tuberculosis RRDR (codons ~516-531); NTM RRDRs differ, so a miss in an NTM isolate is expected.
RRDR = re.compile("CACAAGCGCCGACTGTC|CTGTCGGCGCTGGGG|CCGCTGTCGGGGTTGAC")
RC = str.maketrans("ACGT", "TGCA")


def marker_part(name: str) -> str:
    """File name without lab number, run date/time, well and extension."""
    return LAB.sub("", SUFFIX.sub("", name))


def region(name: str) -> str:
    part = marker_part(name)
    return next(r for r, rule in REGIONS if rule.search(part))


def lab_number(name: str) -> str:
    m = re.match(r"\d{10}", name)
    return m.group(0) if m else ""


def read_check(path: Path) -> str:
    """'RRDR', 'no RRDR' or 'empty' (< 100 bases) for .seq/.fasta; '' for .ab1."""
    if not re.search(r"\.(seq|fasta)$", path.name, re.I):
        return ""
    seq = "".join(l.strip() for l in path.open(errors="ignore") if not l.startswith(">")).upper()
    if len(seq) < 100:
        return "empty"
    return "RRDR" if RRDR.search(seq) or RRDR.search(seq[::-1].translate(RC)) else "no RRDR"


def collect(top: Path) -> list[tuple[str, str, Path]]:
    rows = []
    for d, _, files in os.walk(top):
        reads = [f for f in files if READ_EXT.search(f) and SELECT.search(f) and not SKIP.search(f)]
        regs = {f: region(f) for f in reads}
        # A bare rpoB-F/-R next to F1/F2/R2 of the same lab number is the Xpert assay (rpoB-R is its reverse primer).
        xpert_ids = {lab_number(f) for f, r in regs.items() if r == XPERT} - {""}
        for f in reads:
            r = regs[f]
            if r.startswith("NTM: no primer") and lab_number(f) in xpert_ids and re.search(r"rpoB-[FR](?![A-Za-z0-9])", f):
                r = XPERT
            p = Path(d) / f
            rows.append((r, read_check(p), p))
    return rows


def main() -> None:
    args = [a for a in sys.argv[1:] if a != "--list"]
    top = Path(args[0]) if args else Path(ROOT) / "data/sanger/seq_mol_routine"
    rows = collect(top)
    if "--list" in sys.argv:
        for r, c, p in sorted(rows, key=lambda x: str(x[2])):
            print(f"{r}\t{c}\t{p.relative_to(top)}")
        return

    order = [r for r, _ in REGIONS]
    ext: dict[str, Counter[str]] = defaultdict(Counter)
    chk: dict[str, Counter[str]] = defaultdict(Counter)
    years: dict[str, Counter[str]] = defaultdict(Counter)
    for r, c, p in rows:
        ext[r][p.suffix.lower()] += 1
        if c:
            chk[r][c] += 1
        ym = re.search(r"(20\d\d)-\d\d-\d\d", p.name) or re.search(r"/(20\d\d)[-/]", str(p))
        years[r][ym.group(1) if ym else "?"] += 1

    print(f"Directory: `{top}`; rpoB reads (.ab1/.seq/.fasta): {len(rows)}\n")
    print("| region | files | ab1 | seq | fasta | reads with RRDR | without | empty |")
    print("|---|---|---|---|---|---|---|---|")
    for r in order:
        if ext[r]:
            e = ext[r]
            print(f"| {r} | {sum(e.values())} | {e['.ab1']} | {e['.seq']} | {e['.fasta']} | "
                  f"{chk[r]['RRDR']} | {chk[r]['no RRDR']} | {chk[r]['empty']} |")

    all_years = sorted({y for c in years.values() for y in c})
    used = [r for r in order if ext[r]]
    print("\n| year | " + " | ".join(used) + " |")
    print("|---" * (len(used) + 1) + "|")
    for y in all_years:
        print(f"| {y} | " + " | ".join(str(years[r][y]) for r in used) + " |")

    print("\nName and sequence disagree (NTM name with RRDR, or TR name without RRDR):\n")
    for r, c, p in sorted(rows, key=lambda x: str(x[2])):
        if (r.startswith("NTM") and c == "RRDR") or (r.startswith("Mtb: RRDR") and c == "no RRDR"):
            print(f"- {r} / {c}: `{p.name}`")


if __name__ == "__main__":
    main()
