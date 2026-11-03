#!/usr/bin/env python3
"""One table of every sample with an atypical gyrA or hsp65: project isolates (Mkan329-*), public WGS samples and
public reference genomes, built from the outputs of hsp65-refalign and gyrA-refalign.

"Atypical" means the sample differs from what its species label predicts at one of the two marker genes (criteria
and the current findings are explained in docs/ATYPICAL.md):

  major   hsp65_persicum_like   kansasii-by-genome with the persicum-like (Korean-type) hsp65
          hsp65_other_species   hsp65 closest to another species than the genome species
          gyrA_other_species    gyrA closest to another species than the genome species (status ok or ambiguous)
          gyrA_divergent        gyrA < 98 % identical to every reference (not a complex genome, or a new lineage)
          mixed_culture         contaminated isolate (CheckM > 5 %) whose markers disagree with each other
  minor   gyrA_novel_haplotype  gyrA identical to none of the 72 public genomes (closest one is named)
          gyrA_low_coverage     assembly too fragmented to call gyrA
          hsp65_read_not_genome Sanger hsp65 read does not match the isolate's own genome (co-amplified contaminant)

Reads  output/{hsp65_refalign,gyrA_refalign}/..., data/imm/screening_map_results.csv, data/illumina/public/*/selected.tsv.
Writes output/kansasii-docs/results/atypical_samples/{atypical_samples.tsv, ATYPICAL_SAMPLES.md, ATYPICAL_SAMPLES.docx, MANIFEST.txt}.
Usage: make_atypical_table.py [--out DIR]    Needs pandas and python-docx (env_mlsa).
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "templates"))
from kansasii_paths import (ATYPICAL_HSP65_GENOMES, MANIFEST_SCRIPT, OUT_DOCS, OUT_GYRA, OUT_HSP65, PUBLIC_PROJECTS,  # noqa: E402
                            PUBLIC_READS, REFERENCE_STRAINS, REPOS, SCREENING_MAP_RESULTS)

MAJOR = {"hsp65_persicum_like", "hsp65_other_species", "gyrA_other_species", "gyrA_divergent", "mixed_culture"}
COLUMNS = ["source", "sample", "bioproject", "genome_species", "hsp65_closest", "hsp65_status", "gyrA_closest", "gyrA_status",
           "categories", "severity", "detail", "strain_or_NR", "country", "biosample"]


def species_short(s: object) -> str:
    return str(s).replace("s__Mycobacterium ", "").replace("s__", "")


def read(path: Path, **kw: object) -> pd.DataFrame:
    return pd.read_csv(path, sep=kw.pop("sep", "\t"), dtype=str, keep_default_na=False, **kw)  # type: ignore[call-overload,no-any-return]


def cell(df: pd.DataFrame, row: object, col: str) -> str:
    """One table cell as str (every column is read with dtype=str; DataFrame.at is typed as a wide union)."""
    return str(df.at[row, col])


def project_rows(hsp: Path, gyra: Path, results: Path) -> list[dict[str, str]]:
    res = read(results, sep=",").set_index("PROBENNUMMER")
    g = read(gyra / "project" / "isolates.tsv").set_index("probennummer")
    h = read(hsp / "isolates.tsv").set_index("probennummer")
    k = read(hsp / "korean_type_check.tsv").set_index("probennummer")
    rows = []
    for pn in sorted(set(g.index) | set(h.index) | set(k.index)):
        if pn in REFERENCE_STRAINS:
            continue
        sp = cell(res, pn, "species") if pn in res.index else ""
        cat: list[str] = []
        detail: list[str] = []
        gc = cell(g, pn, "closest_species") if pn in g.index else ""
        gs = cell(g, pn, "status") if pn in g.index else ""
        hc = cell(h, pn, "called_species") if pn in h.index else ""
        hv = cell(h, pn, "verdict") if pn in h.index else ""
        contaminated = pn in res.index and cell(res, pn, "contamination_flag") != ""
        if gs in ("ok", "ambiguous") and gc != sp and sp:
            cat.append("gyrA_other_species")
            detail.append(f"gyrA identity {float(cell(g, pn, 'identity')):.4f} to {cell(g, pn, 'closest_accession')}")
        if gs == "divergent":
            cat.append("gyrA_divergent")
            detail.append(f"gyrA identity {cell(g, pn, 'identity')}")
        if gs == "low_coverage":
            cat.append("gyrA_low_coverage")
            detail.append(f"gyrA coverage {cell(g, pn, 'gyrA_coverage')}")
        if gs == "ok" and cell(g, pn, "exact_match") == "" and cell(g, pn, "gyrA_matches_wgs") == "True":
            cat.append("gyrA_novel_haplotype")
            detail.append(f"gyrA haplotype {cell(g, pn, 'haplotype')}, {cell(g, pn, 'diffs')} difference(s) to {cell(g, pn, 'closest_accession')}")
        if hc and hc != sp and sp:
            cat.append("hsp65_other_species")
            detail.append(f"Sanger hsp65 reads call {hc}")
        if pn in k.index and cell(k, pn, "korean_type") == "True":
            cat.append("hsp65_persicum_like")
            detail.append("assembly hsp65 closer to the Korean-type amplicon than to ATCC 12478")
        if hv == "no call: read does not match own genome":
            cat.append("hsp65_read_not_genome")
            detail.append("Sanger hsp65 read matches the isolate's genome at < 90 % (Rothia mucilaginosa co-amplification)")
        if contaminated and cat and set(cat) & MAJOR:
            cat.append("mixed_culture")
            detail.append(f"CheckM contamination {cell(res, pn, 'checkm_contamination')} %")
        if not cat:
            continue
        rows.append({"source": "project", "sample": pn, "bioproject": "", "genome_species": sp, "hsp65_closest": hc,
                     "hsp65_status": hv, "gyrA_closest": gc, "gyrA_status": gs, "categories": ",".join(cat),
                     "detail": "; ".join(detail),
                     "strain_or_NR": f"NR {cell(res, pn, 'NR')}" if pn in res.index else "", "country": "", "biosample": ""})
    return rows


def public_rows(hsp: Path, gyra: Path) -> list[dict[str, str]]:
    meta = pd.concat([read(PUBLIC_READS / p / "selected.tsv") for p in PUBLIC_PROJECTS if (PUBLIC_READS / p / "selected.tsv").exists()])
    meta = meta.drop_duplicates("sample_id").set_index("sample_id")
    g = read(gyra / "public" / "samples.tsv").set_index("sample")
    parts = [read(hsp / d / "insilico_public.tsv") for d in ("public", "public_persicum") if (hsp / d / "insilico_public.tsv").exists()]
    h = pd.concat(parts).drop_duplicates("sample").set_index("sample")
    rows = []
    for sid in sorted(set(g.index) | set(h.index)):
        cat: list[str] = []
        detail: list[str] = []
        sp = species_short(cell(g, sid, "gtdb_species") if sid in g.index else cell(h, sid, "gtdb_species"))
        gc = cell(g, sid, "closest_species") if sid in g.index else ""
        gs = cell(g, sid, "status") if sid in g.index else ""
        hc = cell(h, sid, "closest_species") if sid in h.index else ""
        hs = cell(h, sid, "status") if sid in h.index else ""
        if sid in h.index and cell(h, sid, "atypical") == "True":
            hc = "persicum-like (Korean-type genome)"  # the closest reference is one of the 3 atypical-hsp65 kansasii genomes
        if sid in g.index:
            if gs in ("ok", "ambiguous") and gc != sp:
                cat.append("gyrA_other_species")
                detail.append(f"gyrA identical to {cell(g, sid, 'closest_accession')} ({gc}), margin {cell(g, sid, 'margin')}")
            if gs == "divergent":
                cat.append("gyrA_divergent")
            if gs == "low_coverage":
                cat.append("gyrA_low_coverage")
                detail.append(f"gyrA coverage {cell(g, sid, 'gyrA_coverage')}")
            if gs == "ok" and cell(g, sid, "exact_match") == "" and gc == sp:
                cat.append("gyrA_novel_haplotype")
                detail.append(f"gyrA haplotype {cell(g, sid, 'haplotype')}, {cell(g, sid, 'diffs')} difference(s) to {cell(g, sid, 'closest_accession')}")
        if sid in h.index:
            if cell(h, sid, "atypical") == "True" and sp == "persicum":
                pass  # a persicum genome is expected to sit next to the persicum-like (Korean-type) kansasii genomes
            elif cell(h, sid, "atypical") == "True" and sp == "kansasii":
                cat.append("hsp65_persicum_like")
                detail.append(f"hsp65 closest to {cell(h, sid, 'closest_accession')} (Korean-type), runner-up {cell(h, sid, 'second_species')}, margin {cell(h, sid, 'margin')}")
            elif hc and hc != sp and cell(h, sid, "atypical") != "True":
                cat.append("hsp65_other_species")
                detail.append(f"hsp65 identical to {cell(h, sid, 'closest_accession')} ({hc})")
        if not cat:
            continue
        m = meta.loc[sid] if sid in meta.index else None
        bp = (cell(g, sid, "bioproject") if sid in g.index else cell(h, sid, "bioproject"))
        rows.append({"source": "public", "sample": sid, "bioproject": bp, "genome_species": sp, "hsp65_closest": hc,
                     "hsp65_status": hs, "gyrA_closest": gc, "gyrA_status": gs, "categories": ",".join(cat),
                     "detail": "; ".join(detail),
                     "strain_or_NR": (m["strain"] or m["isolate"]) if m is not None else "",
                     "country": m["country"] if m is not None else "", "biosample": m["biosample"] if m is not None else ""})
    return rows


def reference_rows(gyra: Path) -> list[dict[str, str]]:
    ref = read(gyra / "public" / "reference_genomes.tsv").set_index("accession")
    rows = []
    for acc in ATYPICAL_HSP65_GENOMES:
        rows.append({"source": "reference genome", "sample": acc, "bioproject": "", "genome_species": "kansasii",
                     "hsp65_closest": "persicum", "hsp65_status": "11 SNPs from other kansasii (441 bp amplicon)",
                     "gyrA_closest": cell(ref, acc, "closest_species") if acc in ref.index else "", "gyrA_status": cell(ref, acc, "status") if acc in ref.index else "",
                     "categories": "hsp65_persicum_like", "detail": "Korean isolates K4/K14/K19 (Samsung Medical Center, submitted by Borstel); "
                     "kansasii by ANI and at gyrA/gyrB/rpoB/recA/tuf/secA/16S/ITS (mlsa-kansasii/LIT.md)",
                     "strain_or_NR": "", "country": "Korea", "biosample": ""})
    wrong = ref[(ref["loo_correct"] == "False")]
    for wacc, r in wrong.iterrows():
        rows.append({"source": "reference genome", "sample": str(wacc), "bioproject": "", "genome_species": r["gtdb_species"],
                     "hsp65_closest": "", "hsp65_status": "", "gyrA_closest": r["closest_species"], "gyrA_status": r["status"],
                     "categories": "gyrA_other_species", "detail": "leave-one-out gyrA call differs from the GTDB species",
                     "strain_or_NR": "", "country": "", "biosample": ""})
    return rows


TITLE = "Samples with an atypical gyrA or hsp65"
INTRO = ("Generated by `kansasii-docs/bin/make_atypical_table.py` from the hsp65-refalign and gyrA-refalign outputs; "
         "criteria and interpretation in `docs/ATYPICAL.md`.")
DETAIL_HEADER = ["source", "sample", "project", "genome species", "hsp65", "gyrA", "categories", "detail"]

Table = tuple[str, list[str], list[list[str]]]  # (heading or "", header, rows)


def tables(df: pd.DataFrame) -> list[Table]:
    counts = df.assign(cat=df["categories"].str.split(",")).explode("cat").groupby(["source", "cat"]).size()
    out: list[Table] = [("", ["source", "category", "samples"], counts.reset_index(name="n").astype(str).values.tolist())]
    for sev, title in (("major", "Species-level discordance (major)"), ("minor", "Other findings (minor)")):
        d = df[df["severity"] == sev]
        out.append((f"{title}: {len(d)} samples", DETAIL_HEADER,
                    [[str(r.source), str(r.sample), str(r.bioproject), str(r.genome_species),
                      f"{r.hsp65_closest} {r.hsp65_status}", f"{r.gyrA_closest} {r.gyrA_status}",
                      str(r.categories), str(r.detail)] for r in d.itertuples()]))
    return out


def markdown(df: pd.DataFrame) -> str:
    out = [f"# {TITLE}", "", INTRO, ""]
    for heading, header, rows in tables(df):
        if heading:
            out += [f"## {heading}", ""]
        out += ["| " + " | ".join(header) + " |", "|" + "---|" * len(header)] + ["| " + " | ".join(r) + " |" for r in rows] + [""]
    return "\n".join(out) + "\n"


def write_docx(df: pd.DataFrame, path: Path) -> None:
    """Same content as the markdown, as landscape A4 Word tables (needs python-docx: env_mlsa)."""
    from docx import Document
    from docx.enum.section import WD_ORIENT
    from docx.oxml import OxmlElement
    from docx.shared import Mm, Pt

    doc = Document()
    sec = doc.sections[0]
    sec.orientation = WD_ORIENT.LANDSCAPE
    sec.page_width, sec.page_height = Mm(297), Mm(210)
    sec.left_margin = sec.right_margin = sec.top_margin = sec.bottom_margin = Mm(12)
    doc.add_heading(TITLE, 1)
    doc.add_paragraph(INTRO.replace("`", ""))
    for heading, header, rows in tables(df):
        if heading:
            doc.add_heading(heading, 2)
        t = doc.add_table(rows=1, cols=len(header))
        t.style = "Table Grid"
        for i, row in enumerate([header] + rows):
            cells = t.rows[0].cells if i == 0 else t.add_row().cells
            for cell, text in zip(cells, row):
                cell.text = ""
                run = cell.paragraphs[0].add_run(text)
                run.font.size = Pt(7.5)
                run.bold = i == 0
        flag = OxmlElement("w:tblHeader")
        t.rows[0]._tr.get_or_add_trPr().append(flag)  # repeat the header row on every page
        doc.add_paragraph()
    doc.save(str(path))


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--hsp65-dir", type=Path, default=OUT_HSP65 / "results")
    ap.add_argument("--gyra-dir", type=Path, default=OUT_GYRA / "results")
    ap.add_argument("--screening-map-results", type=Path, default=SCREENING_MAP_RESULTS)
    ap.add_argument("--out", type=Path, default=OUT_DOCS / "results" / "atypical_samples")
    args = ap.parse_args()
    rows = (reference_rows(args.gyra_dir) + project_rows(args.hsp65_dir, args.gyra_dir, args.screening_map_results)
            + public_rows(args.hsp65_dir, args.gyra_dir))
    df = pd.DataFrame(rows)
    df["severity"] = ["major" if set(c.split(",")) & MAJOR else "minor" for c in df["categories"]]
    df = df[COLUMNS].sort_values(["severity", "source", "categories", "sample"], key=lambda c: c.map({"major": 0, "minor": 1}) if c.name == "severity" else c)
    args.out.mkdir(parents=True, exist_ok=True)
    df.to_csv(args.out / "atypical_samples.tsv", sep="\t", index=False)
    (args.out / "ATYPICAL_SAMPLES.md").write_text(markdown(df), encoding="utf-8")
    write_docx(df, args.out / "ATYPICAL_SAMPLES.docx")
    subprocess.run(["bash", str(MANIFEST_SCRIPT), str(args.out), str(REPOS / "kansasii-docs"), "bin/make_atypical_table.py",
                    str(args.hsp65_dir), str(args.gyra_dir), str(args.screening_map_results)], check=True)
    print(df.groupby(["source", "severity"]).size().to_string())
    print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
