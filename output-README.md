# output/

Results, one directory per repo or analysis. Scripts write here; they never read from here
(inputs come from `data/` and `runs/`). Index of the project: `../README.md`.

| Directory | Written by |
|---|---|
| `mic/{mhk,mgit}` | kansasii-mic |
| `mlsa/{main1..main4,genome_identity_check}` and `*_excluded` variants | mlsa-kansasii (`_excluded` = run without the excluded isolates) |
| `hsp65_refalign` | hsp65-refalign |
| `gwas` | kansasii-gwas |
| `arm`, `arm_bam` | kansasii-arm |
| `mst`, `cgmlst`, `ridom` | kansasii-mst, kansasii-cgmlst |
| `sanger-microsynth/<date>_species_panel` | sanger-microsynth |
| `imm`, `iTOL`, `<run_name>` | immensekansasii (pipeline results, iTOL files) |
| `lit`, `kansasii_complex_gtdb_representatives` | immensekansasii (GTDB look-ups, reference tree) |
| `*_Mkan329-035` | one-off contamination diagnostics for isolate Mkan329-035 |
| `mlsa-old` | obsolete, do not use |

Each directory should hold a `MANIFEST.txt` (commit, script, inputs); see
`../repos/kansasii-docs/docs/PROVENANCE.md`. Directories without one predate it.
