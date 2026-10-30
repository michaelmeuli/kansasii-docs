# output/

Results, one directory per repo or analysis. Scripts write here; they never read from here
(inputs come from `data/` and `runs/`). Index of the project: `../README.md`.

Every top-level directory is named exactly like the repo in `repos/` that wrote it, and has the same inner layout:
`results/` (one subdirectory per analysis/program), `logs/` (SLURM logs of that repo's jobs) and, per analysis
directory, a `MANIFEST.txt`. The path constants are `OUT_*` in `kansasii_paths` (e.g. `OUT_MLSA`, results in `OUT_MLSA / "results"`).

| Directory | Contents (below `results/`) |
|---|---|
| `kansasii-mic` | `mhk/`, `mgit/` |
| `mlsa-kansasii` | `locus_discovery`, `genome_identity_check`, `sanger_mlsa`, `sanger_refalign*`, `sanger_vs_wgs*` and `*_excluded` variants (`_excluded` = run without the 3 atypical-hsp65 Korean genomes, `--exclude-atypical`); `logs/legacy/` = logs from before 2026-10-25 |
| `hsp65-refalign` | `public/`, `public_persicum/`, `public_ctl/`: public assemblies; `MANIFEST_korean_type_check.txt` next to `MANIFEST.txt` |
| `gyrA-refalign` | `project/`, `public/` (kept separate) |
| `kansasii-amr-marker-screen` | `assembly/` (was `amr`), `bam/` (was `amr_bam`; its `refs` links to `../assembly/refs`) |
| `kansasii-mst`, `kansasii-cgmlst` | MST and cgMLST results. `kansasii-cgmlst/` also holds `ridom_assemblies.{tar.gz,zip}` (+ `ridom_assemblies.MANIFEST.txt`, `ridom_mst_cluster_summary.docx`) from `10_export_ridom.py`: the `keep` cohort as real files renamed M001 ..., plus 7 reference genomes |
| `kansasii-gwas` | GWAS tables (was `gwas`; the repo is not in `repos/` any more) |
| `kansasii-docs` | `atypical_samples/` from `bin/make_atypical_table.py` (`docs/ATYPICAL.md`) |
| `immensekansasii` | `gtdb/` (GTDB look-ups); `results/{imm,iTOL,screening_map_*,*_Mkan329-035}` (pipeline results, iTOL files, one-off contamination diagnostics for isolate Mkan329-035). The reference-tree run itself stays in `runs/kansasii_complex_gtdb_representatives` |
| `sanger-microsynth` | `<date>_species_panel` |
| `SUMMARY.html` | `kansasii-docs/bin/make_summary.py` (project-wide index, stays at the top) |

Each directory should hold a `MANIFEST.txt` (commit, script, inputs); see
`../repos/kansasii-docs/docs/PROVENANCE.md`. Directories without one predate it.
