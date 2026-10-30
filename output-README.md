# output/

Results, one directory per repo or analysis. Scripts write here; they never read from here
(inputs come from `data/` and `runs/`). Index of the project: `../README.md`.

| Directory | Written by |
|---|---|
| `mic/{mhk,mgit}` | kansasii-mic |
| `mlsa/{locus_discovery,genome_identity_check,sanger_mlsa,sanger_refalign*,sanger_vs_wgs}` and `*_excluded` variants | mlsa-kansasii (`_excluded` = run without the 3 atypical-hsp65 Korean genomes, `--exclude-atypical`) |
| `hsp65_refalign` | hsp65-refalign (`public/`, `public_persicum/`, `public_ctl/`: public assemblies; `MANIFEST_korean_type_check.txt` next to `MANIFEST.txt`) |
| `gyrA_refalign` | gyrA-refalign (`project/`, `public/` separate) |
| `amr`, `amr_bam` | kansasii-amr-marker-screen |
| `mst`, `cgmlst` | kansasii-mst, kansasii-cgmlst |
| `ridom_assemblies.tar.gz`, `ridom_assemblies.zip` (same content) | kansasii-cgmlst `10_export_ridom.py` (manifest `ridom_assemblies.MANIFEST.txt`): the `keep` cohort as real files renamed M001 ..., plus 7 reference genomes. |
| `atypical_samples` | kansasii-docs `bin/make_atypical_table.py` (samples with an atypical gyrA or hsp65, project and public; `docs/ATYPICAL.md`) |
| `SUMMARY.html` | kansasii-docs `bin/make_summary.py` |
| `sanger-microsynth/<date>_species_panel` | sanger-microsynth |
| `imm`, `iTOL`, `<run_name>` | immensekansasii (pipeline results, iTOL files) |
| `immensekansasii` | immensekansasii (GTDB look-ups; the reference-tree run itself stays in `runs/kansasii_complex_gtdb_representatives`, its iTOL files are in `iTOL/`) |
| `*_Mkan329-035` | one-off contamination diagnostics for isolate Mkan329-035 |
| `mlsa-old` | obsolete, do not use |
| `<dir>/logs/` | SLURM logs of the jobs of that directory (`mlsa/logs/legacy/`: logs of before 2026-10-25 that lay in the repo) |

Each directory should hold a `MANIFEST.txt` (commit, script, inputs); see
`../repos/kansasii-docs/docs/PROVENANCE.md`. Directories without one predate it.
