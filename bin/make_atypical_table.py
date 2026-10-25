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
Writes output/atypical_samples/{atypical_samples.tsv, ATYPICAL_SAMPLES.md, MANIFEST.txt}.
Usage: make_atypical_table.py [--out DIR]    Needs pandas (env_mlsa / env_mic).
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "templates"))
from kansasii_paths import (ATYPICAL_HSP65_GENOMES, MANIFEST_SCRIPT, OUTPUT_ROOT, PUBLIC_PROJECTS, PUBLIC_READS,  # noqa: E402
                            REFERENCE_STRAINS, REPOS, SCREENING_MAP_RESULTS)

MAJOR = {"hsp65_persicum_like", "hsp65_other_species", "gyrA_other_species", "gyrA_divergent", "mixed_culture"}
COLUMNS = ["source", "sample", "bioproject", "genome_species", "hsp65_closest", "hsp65_status", "gyrA_closest", "gyrA_status",
           "categories", "severity", "detail", "strain_or_NR", "country", "biosample"]


def species_short(s: object) -> str:
    return str(s).replace("s__Mycobacterium ", "").replace("s__", "")


def read(path: Path, **kw: object) -> pd.DataFrame:
    return pd.read_csv(path, sep=kw.pop("sep", "\t"), dtype=str, keep_default_na=False, **kw)  # type: ignore[call-overload,no-any-return]


def project_rows(hsp: Path, gyra: Path, results: Path) -> list[dict[str, str]]:
    res = read(results, sep=",").set_index("PROBENNUMMER")
    g = read(gyra / "project" / "isolates.tsv").set_index("probennummer")
    h = read(hsp / "isolates.tsv").set_index("probennummer")
    k = read(hsp / "korean_type_check.tsv").set_index("probennummer")
    rows = []
    for pn in sorted(set(g.index) | set(h.index) | set(k.index)):
        if pn in REFERENCE_STRAINS:
            continue
        sp = res.at[pn, "species"] if pn in res.index else ""
        cat: list[str] = []
        detail: list[str] = []
        gc = g.at[pn, "closest_species"] if pn in g.index else ""
        gs = g.at[pn, "status"] if pn in g.index else ""
        hc = h.at[pn, "called_species"] if pn in h.index else ""
        hv = h.at[pn, "verdict"] if pn in h.index else ""
        contaminated = pn in res.index and res.at[pn, "contamination_flag"] != ""
        if gs in ("ok", "ambiguous") and gc != sp and sp:
            cat.append("gyrA_other_species")
            detail.append(f"gyrA identity {float(g.at[pn, 'identity']):.4f} to {g.at[pn, 'closest_accession']}")
        if gs == "divergent":
            cat.append("gyrA_divergent")
            detail.append(f"gyrA identity {g.at[pn, 'identity']}")
        if gs == "low_coverage":
            cat.append("gyrA_low_coverage")
            detail.append(f"gyrA coverage {g.at[pn, 'gyrA_coverage']}")
        if gs == "ok" and g.at[pn, "exact_match"] == "" and g.at[pn, "gyrA_matches_wgs"] == "True":
            cat.append("gyrA_novel_haplotype")
            detail.append(f"gyrA haplotype {g.at[pn, 'haplotype']}, {g.at[pn, 'diffs']} difference(s) to {g.at[pn, 'closest_accession']}")
        if hc and hc != sp and sp:
            cat.append("hsp65_other_species")
            detail.append(f"Sanger hsp65 reads call {hc}")
        if pn in k.index and k.at[pn, "korean_type"] == "True" and sp == "kansasii":
            cat.append("hsp65_persicum_like")
            detail.append("assembly hsp65 closer to the Korean-type amplicon than to ATCC 12478")
        if hv == "no call: read does not match own genome":
            cat.append("hsp65_read_not_genome")
            detail.append("Sanger hsp65 read matches the isolate's genome at < 90 % (Rothia mucilaginosa co-amplification)")
        if contaminated and cat and set(cat) & MAJOR:
            cat.append("mixed_culture")
            detail.append(f"CheckM contamination {res.at[pn, 'checkm_contamination']} %")
        if not cat:
            continue
        rows.append({"source": "project", "sample": pn, "bioproject": "", "genome_species": sp, "hsp65_closest": hc,
                     "hsp65_status": hv, "gyrA_closest": gc, "gyrA_status": gs, "categories": ",".join(cat),
                     "detail": "; ".join(detail),
                     "strain_or_NR": f"NR {res.at[pn, 'NR']}" if pn in res.index else "", "country": "", "biosample": ""})
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
        sp = species_short(g.at[sid, "gtdb_species"] if sid in g.index else h.at[sid, "gtdb_species"])
        gc = g.at[sid, "closest_species"] if sid in g.index else ""
        gs = g.at[sid, "status"] if sid in g.index else ""
        hc = h.at[sid, "closest_species"] if sid in h.index else ""
        hs = h.at[sid, "status"] if sid in h.index else ""
        if sid in g.index:
            if gs in ("ok", "ambiguous") and gc != sp:
                cat.append("gyrA_other_species")
                detail.append(f"gyrA identical to {g.at[sid, 'closest_accession']} ({gc}), margin {g.at[sid, 'margin']}")
            if gs == "divergent":
                cat.append("gyrA_divergent")
            if gs == "low_coverage":
                cat.append("gyrA_low_coverage")
                detail.append(f"gyrA coverage {g.at[sid, 'gyrA_coverage']}")
            if gs == "ok" and g.at[sid, "exact_match"] == "" and gc == sp:
                cat.append("gyrA_novel_haplotype")
                detail.append(f"gyrA haplotype {g.at[sid, 'haplotype']}, {g.at[sid, 'diffs']} difference(s) to {g.at[sid, 'closest_accession']}")
        if sid in h.index:
            if h.at[sid, "atypical"] == "True":
                cat.append("hsp65_persicum_like")
                detail.append(f"hsp65 closest to {h.at[sid, 'closest_accession']} (Korean-type), runner-up {h.at[sid, 'second_species']}, margin {h.at[sid, 'margin']}")
            elif hc and hc != sp:
                cat.append("hsp65_other_species")
                detail.append(f"hsp65 identical to {h.at[sid, 'closest_accession']} ({hc})")
        if not cat:
            continue
        m = meta.loc[sid] if sid in meta.index else None
        bp = (g.at[sid, "bioproject"] if sid in g.index else h.at[sid, "bioproject"])
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
                     "gyrA_closest": ref.at[acc, "closest_species"] if acc in ref.index else "", "gyrA_status": ref.at[acc, "status"] if acc in ref.index else "",
                     "categories": "hsp65_persicum_like", "detail": "Korean isolates K4/K14/K19 (Samsung Medical Center, submitted by Borstel); "
                     "kansasii by ANI and at gyrA/gyrB/rpoB/recA/tuf/secA/16S/ITS (mlsa-kansasii/LIT.md)",
                     "strain_or_NR": "", "country": "Korea", "biosample": ""})
    wrong = ref[(ref["loo_correct"] == "False")]
    for acc, r in wrong.iterrows():
        rows.append({"source": "reference genome", "sample": str(acc), "bioproject": "", "genome_species": r["gtdb_species"],
                     "hsp65_closest": "", "hsp65_status": "", "gyrA_closest": r["closest_species"], "gyrA_status": r["status"],
                     "categories": "gyrA_other_species", "detail": "leave-one-out gyrA call differs from the GTDB species",
                     "strain_or_NR": "", "country": "", "biosample": ""})
    return rows


def markdown(df: pd.DataFrame) -> str:
    out = ["# Samples with an atypical gyrA or hsp65", "",
           "Generated by `kansasii-docs/bin/make_atypical_table.py` from the hsp65-refalign and gyrA-refalign outputs; "
           "criteria and interpretation in `docs/ATYPICAL.md`.", ""]
    counts = df.assign(cat=df["categories"].str.split(",")).explode("cat").groupby(["source", "cat"]).size()
    out += ["| source | category | samples |", "|---|---|---|"] + [f"| {s} | {c} | {n} |" for (s, c), n in counts.items()] + [""]
    for sev, title in (("major", "Species-level discordance (major)"), ("minor", "Other findings (minor)")):
        d = df[df["severity"] == sev]
        out += [f"## {title}: {len(d)} samples", "",
                "| source | sample | project | genome species | hsp65 | gyrA | categories | detail |", "|---|---|---|---|---|---|---|---|"]
        for r in d.itertuples():
            out.append(f"| {r.source} | {r.sample} | {r.bioproject} | {r.genome_species} | {r.hsp65_closest} {r.hsp65_status} | "
                       f"{r.gyrA_closest} {r.gyrA_status} | {r.categories} | {r.detail} |")
        out.append("")
    return "\n".join(out) + "\n"


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--hsp65-dir", type=Path, default=OUTPUT_ROOT / "hsp65_refalign")
    ap.add_argument("--gyra-dir", type=Path, default=OUTPUT_ROOT / "gyrA_refalign")
    ap.add_argument("--screening-map-results", type=Path, default=SCREENING_MAP_RESULTS)
    ap.add_argument("--out", type=Path, default=OUTPUT_ROOT / "atypical_samples")
    args = ap.parse_args()
    rows = (reference_rows(args.gyra_dir) + project_rows(args.hsp65_dir, args.gyra_dir, args.screening_map_results)
            + public_rows(args.hsp65_dir, args.gyra_dir))
    df = pd.DataFrame(rows)
    df["severity"] = ["major" if set(c.split(",")) & MAJOR else "minor" for c in df["categories"]]
    df = df[COLUMNS].sort_values(["severity", "source", "categories", "sample"], key=lambda c: c.map({"major": 0, "minor": 1}) if c.name == "severity" else c)
    args.out.mkdir(parents=True, exist_ok=True)
    df.to_csv(args.out / "atypical_samples.tsv", sep="\t", index=False)
    (args.out / "ATYPICAL_SAMPLES.md").write_text(markdown(df), encoding="utf-8")
    subprocess.run(["bash", str(MANIFEST_SCRIPT), str(args.out), str(REPOS / "kansasii-docs"), "bin/make_atypical_table.py",
                    str(args.hsp65_dir), str(args.gyra_dir), str(args.screening_map_results)], check=True)
    print(df.groupby(["source", "severity"]).size().to_string())
    print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
