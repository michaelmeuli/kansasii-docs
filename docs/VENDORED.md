# Code that is copied between repos

The repos are independent (each has its own git history and can be cloned alone), so a few files are **copies**. Three kinds:

## 1. Shared files, identical everywhere (checked by `check_sync.sh`)

| File in kansasii-docs | Copy in every repo | `--fix` |
|---|---|---|
| `templates/kansasii_paths.py` | `<package>/kansasii_paths.py` or `scripts/kansasii_paths.py` | yes |
| `templates/gitattributes` | `.gitattributes` | yes |
| `templates/vscode-settings.json` | `.vscode/settings.json` | yes |
| `templates/gitignore` | lines of `.gitignore` (the repo may add more) | yes |

`templates/kansasii_paths.sh` is not copied: shell and sbatch files `source` it from kansasii-docs.
Change a shared constant in the template and run `bash repos/check_sync.sh --fix`, then commit in each repo.

## 2. Vendored analysis code (copies that may differ; keep the matching logic in sync by hand)

| Module | Source of truth | Copies | Differences today |
|---|---|---|---|
| `refalign.py` (read vs reference alignment, `identify_read`, `ReadResult`) | `mlsa-kansasii/mlsa/refalign.py` | `sanger-microsynth/sanger_ms/refalign.py`, `hsp65-refalign/hsp65_refalign/refalign.py`, `gyrA-refalign/gyrA_refalign/refalign.py` | only mlsa has the opt-in `--iupac` mode (`IUPAC_BASES`, `_iupac_aligner`, `iupac` arguments); mlsa and sanger_ms have the PDF/figure code; hsp65 and gyrA are the shortest and identical to each other except the docstring. The full IUPAC `_COMP` complement is in all four. |
| `sanger_io.py` (AB1 parsing, Mott trimming, locus from file name) | `mlsa-kansasii/mlsa/sanger_io.py` | `hsp65-refalign/hsp65_refalign/sanger_io.py`, `sanger-microsynth/sanger_ms/sanger_io.py` | sanger_ms keeps only AB1 parsing and trimming (no locus classification) |
| in-silico hsp65 PCR (`in_silico_pcr`, TB-11/TB-12(w)) | `mlsa-kansasii/mlsa/loci.py` + `protocols.py` | `hsp65-refalign/hsp65_refalign/insilico.py` | primers are constants there; mlsa reads them from the lab protocol `.docx` |
| `ridom_id()` (`Mkan329-081` -> `M081`, controls by `LABEL`) | `immensekansasii/scripts/06_screening_map_results.py` | `kansasii-cgmlst/scripts/10_export_ridom.py`, `kansasii-ridom/scripts/common.py` | same rule; change all three together |
| `common.load_samples` (QC exclusion rules) | `kansasii-mst/scripts/common.py` | `kansasii-cgmlst/scripts/common.py` | cgmlst keeps complex control strains (NR 128/132/133) and has the `in_pool` column on purpose |

When the alignment or trimming logic changes in `mlsa-kansasii`, apply it to the three copies and rerun their checks
(`hsp65-refalign` submit_validate must still give 108 correct / 0 wrong for the same reads; `gyrA-refalign` leave-one-out
72/72). The vendoring is deliberate: hsp65-refalign and gyrA-refalign are meant to stand alone, and sanger-microsynth is a routine
tool that must not break when the research repo is reorganised. Nothing imports another repo.

## 3. Copies of data tables

`output/immensekansasii/results/screening_map_{link,results}.csv` (+ `.MANIFEST.txt`) are copies of the files in `data/imm/` written by
`immensekansasii/scripts/02` and `06`; scripts read only `data/imm/`. See `DATAFLOW.md`.
