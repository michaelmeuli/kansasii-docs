# output/

Results, one directory per repo or analysis. Scripts write here; they never read from here
(inputs come from `data/` and `runs/`). Index of the project: `../README.md`.

Every top-level directory is named exactly like the repo in `repos/` that wrote it, and has the same inner layout:
`results/` (one subdirectory per analysis/program), `logs/` (SLURM logs of that repo's jobs) and, per analysis
directory, a `MANIFEST.txt`. The path constants are `OUT_*` in `kansasii_paths` (e.g. `OUT_MLSA`, results in `OUT_MLSA / "results"`).

| Directory | Contents (below `results/`) |
|---|---|
| `kansasii-mic` | `mhk/`, `mgit/` |
| `mlsa-kansasii` | `locus_discovery`, `genome_identity_check`, `sanger_mlsa`, `sanger_refalign*`, `sanger_vs_wgs*` and `*_excluded` variants (`_excluded` = run without the 3 atypical-hsp65 Korean genomes, `--exclude-atypical`); `logs/legacy/` = archived logs with other job names (`mlsa-sanger-differentiation-*`, `mlsa-refalign-*`), not written by any current job |
| `hsp65-refalign` | validation tables (`reads.tsv`, `isolates.tsv`, `SUMMARY.txt`), `figures/`, `blast/`, Korean-type check; `public/`, `public_persicum/`, `public_ctl/`: public assemblies; `MANIFEST_korean_type_check.txt` next to `MANIFEST.txt` |
| `gyrA-refalign` | `project/`, `public/`, `public_reads/` (kept separate) |
| `kansasii-amr-marker-screen` | `assembly/`, `bam/` (its `refs` links to `../assembly/refs`) |
| `kansasii-mst`, `kansasii-cgmlst` | MST and cgMLST results, not used for the report (`docs/RIDOM.md`); `kansasii-cgmlst/results/sample_qc.tsv` feeds `excluded`. `kansasii-cgmlst/ridom_mst_cluster_summary.docx` is a loose file without manifest |
| `kansasii-ridom` | `ridom_assemblies.{tar.gz,zip}` (+ `.MANIFEST.txt`) from `01_export_ridom.py`: the 175 pool isolates incl. M055 + 7 references for Ridom SeqSphere+; `results/`: `export_status.tsv` (check of the `data/imm/ridom-*` exports) and the tables derived from the exports (`docs/RIDOM.md`) |
| `kansasii-docs` | `atypical_samples/` from `bin/make_atypical_table.py` (`docs/ATYPICAL.md`) |
| `immensekansasii` | `gtdb/` (GTDB look-ups); `results/{iTOL,screening_map_*,*_Mkan329-035}` (pipeline results, iTOL files, one-off contamination diagnostics for isolate Mkan329-035). The reference-tree run itself stays in `runs/kansasii_complex_gtdb_representatives` |
| `sanger-microsynth` | `<date>_species_panel`, `report_<date>_<time>.pdf`, `examples_7genomes` (no `results/` level) |
| `SUMMARY.html` | `kansasii-docs/bin/make_summary.py` (project-wide index, stays at the top) |

Each directory should hold a `MANIFEST.txt` (commit, script, inputs); see
`../repos/kansasii-docs/docs/PROVENANCE.md`. One-off directories (`immensekansasii/results/*_Mkan329-035`, `hsp65-refalign/results/blast`) have none.
