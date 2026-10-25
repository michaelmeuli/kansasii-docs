# output/

Results, one directory per repo or analysis. Scripts write here; they never read from here
(inputs come from `data/` and `runs/`). Index of the project: `../README.md`.

| Directory | Written by |
|---|---|
| `mic/{mhk,mgit}` | kansasii-mic |
| `mlsa/{main1..main4,genome_identity_check}` and `*_excluded` variants | mlsa-kansasii (`_excluded` = run without the excluded isolates) |
| `hsp65_refalign` | hsp65-refalign |
| `gyrA_refalign` | gyrA-refalign (`project/`, `public/` separate) |
| `arm`, `amr_bam` | kansasii-amr-marker-screen |
| `mst`, `cgmlst`, `ridom` | kansasii-mst, kansasii-cgmlst (`ridom`: all assemblies except isolates with `contamination_flag` = contaminated, CheckM > 5 %: Mkan329-010, -021, -035, -106, -113; `ridom_assemblies.tar.gz` is built by kansasii-cgmlst `10_export_ridom.py`: real files, renamed M001 ..., plus 7 reference genomes) |
| `sanger-microsynth/<date>_species_panel` | sanger-microsynth |
| `imm`, `iTOL`, `<run_name>` | immensekansasii (pipeline results, iTOL files) |
| `immensekansasii`, `kansasii_complex_gtdb_representatives` | immensekansasii (GTDB look-ups, reference tree) |
| `*_Mkan329-035` | one-off contamination diagnostics for isolate Mkan329-035 |
| `mlsa-old` | obsolete, do not use |

Each directory should hold a `MANIFEST.txt` (commit, script, inputs); see
`../repos/kansasii-docs/docs/PROVENANCE.md`. Directories without one predate it.
