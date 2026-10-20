# Changelog

Notable changes to data tables and outputs, newest first.

## 2026-10-20
- `output/ridom/` (185 -> 183 assemblies): removed `Mkan329-009-jc` and `Mkan329-056-jc` (originals kept);
  `manifest.tsv` and `output/ridom_assemblies.tar.gz` updated. `Mkan329-035`, `-106`, `-113` are not
  in the export (CheckM contamination 113 %, 20 %, 61 %; no recorded exclusion rule).
- `screening_map_results.csv`: new column `NGS_USED` after `NGS_MM` (`NGS_MM` if done, else `NGS_JC`);
  immensekansasii commit `3a8fb7f`. All four copies updated.
