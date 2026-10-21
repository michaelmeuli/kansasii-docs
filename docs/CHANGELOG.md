# Changelog

Notable changes to data tables and outputs, newest first.

## 2026-10-21
- mlsa-kansasii `93de64d`, sanger-microsynth `ce2c956`: `_COMP` in `refalign.py` now has the full IUPAC complement (reverse-strand
  hits with R/Y/K/M/S/W were not complemented). mlsa-kansasii also gets opt-in `--iupac` alignment; tested on 127 hsp65 reads, no call
  changes, so the default stays. New output `output/mlsa/main3_reference_alignment_hsp65_iupac/` (runs B-E and the consensus references).
  See mlsa-kansasii README, section "IUPAC-aware alignment".
- `output/mlsa/main3_reference_alignment_hsp65_iupac/F_consensus_k1_noatypical/`: IUPAC consensus without the 3 Korean kansasii genomes; persicum margin 2.85 -> 7.1+, i.e. the narrow persicum/kansasii margin comes from those genomes (README, "The margin to the second-best species").

## 2026-10-20
- `output/ridom_assemblies.tar.gz` rebuilt by the new `kansasii-cgmlst/scripts/10_export_ridom.py`: it now holds real FASTA files
  (the old archive, 8 KB, contained only symlinks into `runs/`), 175 cohort isolates named `M001` ..., the control strains
  `Mkan329-128/-132/-133` as `M_kansasii_ATCC_12478`, `M_persicum_DSM_104278`, `M_pseudokansasii_DSM_107152`, the 7 public
  references (`GCF_*`) and `ridom/metadata.tsv` (species as `M. kansasii` ...). Same cohort as kansasii-cgmlst (complex species only,
  not contaminated), so the non-complex isolates of `output/ridom/` are no longer in the archive.
- `output/ridom/` (183 -> 181 assemblies): `Mkan329-010` (7.67 %) and `-021` (7.76 %) removed (and their symlinks), now
  `contamination_flag` = contaminated because `--max-contamination` is 5 % (was documented as 10 %); `manifest.tsv` filtered accordingly
  (ST, CheckM, species unchanged and consistent with `screening_map_results.csv`). Excluded now: `-010`, `-021`, `-035`, `-106`, `-113`.
- `output/cgmlst/` slimmed from 380 MB to 45 MB: working state (genome symlinks, `schema*`, `cgmlst_schema`, `loci_reports`, `cds_coordinates.tsv`, `results_contigsInfo.tsv`, logs) moved to `runs/cgmlst/`; only result tables, `cgMLST.html`, `schema_report.html` and `mst/` remain. kansasii-cgmlst scripts updated.
- `output/ridom/` (185 -> 183 assemblies): removed `Mkan329-009-jc` and `Mkan329-056-jc` (originals kept);
  `manifest.tsv` and `output/ridom_assemblies.tar.gz` updated. `Mkan329-035`, `-106`, `-113` are
  deliberately not in the export: CheckM contamination > 10 % (113 %, 20 %, 61 %), the
  `contamination_flag` threshold of `06_screening_map_results.py`; kansasii-cgmlst excludes the same
  flagged isolates (`scripts/common.py`). No other isolate is above 7.8 %.
- `screening_map_results.csv`: new column `NGS_USED` after `NGS_MM` (`NGS_MM` if done, else `NGS_JC`);
  immensekansasii commit `3a8fb7f`. All four copies updated.
