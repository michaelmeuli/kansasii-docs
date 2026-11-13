# Ridom SeqSphere+ as source of truth

**Ridom SeqSphere+ is the source of truth for the typing results (cgMLST, MST, clusters) and for the final
report.** The outputs of `kansasii-mst` (core-SNP MST) and `kansasii-cgmlst` (chewBBACA scheme, Ridom-style MST) are
kept for comparison and are not cited in the final report, except for the gaps listed under "Not available from Ridom" until those
are decided.

## Rules

- Ridom is operated in the GUI. Every export goes to `data/imm/` as `ridom-<content>.<ext>` (CSV, `;`-separated as
  SeqSphere writes it; figures as SVG/PDF). Do not edit exported files; derived tables belong in `output/`.
- `data/imm/` files have no MANIFEST. Record each export in the table below (date, SeqSphere+ version, project, who) when you add it.
- The input to Ridom is `output/kansasii-ridom/ridom_assemblies.{tar.gz,zip}` (made by `kansasii-ridom/scripts/01_export_ridom.py`, `sbatch submit_export.sbatch`;
  isolates `M001` ..., controls by `LABEL`, references by accession; `ridom/metadata.tsv` for the isolate-data import). It holds the pool of 175 complex
  isolates (incl. M055, `excluded` by chewBBACA coverage only, so Ridom can give its good-target value) + 7 references = 182. The assemblies are
  unmodified (the ATCC 12478 reference keeps its plasmid contig); plasmids are removed by Ridom.
- Why the pool is 175 (`load_cohort()` in `kansasii-ridom/scripts/common.py`: complex species and not `contaminated`; it does not filter on `excluded`):

  | Step | Count |
  |---|---|
  | Rows in `screening_map_results.csv` (NR 1-186) | 186 |
  | Non-complex control strains (H37Rv, *M. avium*, *M. abscessus*, *M. xenopi*, *M. ulcerans*/marinum: NR 126, 127, 129, 130, 131) | -5 = 181 |
  | Contaminated, CheckM > 5 % (NR 10, 21, 35, 106, 113) | -5 = 176 |
  | NR 184, clinical *M. avium* (`LABEL` empty, not in the complex) | -1 = **175** (the pool) |

  The 3 complex controls (NR 128, 132, 133) stay in. M055 (NR 55, 81.5 % of loci called, CheckM 2.47 %) is in the pool but `excluded`, so the
  `keep` cohort of the distance matrices and MSTs is 174. The archive adds the 7 references: 175 + 7 = 182 (`N_POOL` in `01_export_ridom.py`
  asserts 175). Cross-check: `excluded` has 7 rows (5 contaminated, M055, NR 184); 186 - 5 - 7 = 174 = `keep`.
- Sample ids in Ridom exports: `Mkan329-081` is `M081`, controls use `LABEL` (`M_kansasii_ATCC_12478`, ...); `ridom_id()` in
  `immensekansasii/scripts/06_screening_map_results.py` converts.

## Exports in `data/imm/` today

| File | Content | Rows | Status |
|---|---|---|---|
| `ridom-clusters.csv` | good targets %, genome size, sample id, species, MST cluster (`-Group-`) | 181 | complete cohort; `-Group-` set for 63 of 181 (the rest are not in a cluster) |
| `ridom-comparison-table.csv` | allele table: missing-value count, good targets, size, id, species, 1,407 `MKAN_RS*` loci | 182 | complete: pool incl. M055 + the 7 references |
| `ridom-distance-matrix.meg` | pairwise allele distances (MEGA, lower triangle), whole complex | 181 taxa | complete: `keep` cohort + references, without M055; missing-value handling to be confirmed (export log) |
| `ridom-scheme.tasktemplate` | gzip XML: 1,407 core targets and the full Target Definer report (settings, filters, accessory / discarded lists) | 1,407 targets | complete; read by `03_scheme.py` |
| `ridom-kansasii-plasmids.csv` | NCBI plasmid list that the Target Definer excluded | - | used in `PLASMIDS.md` only |

Allele distances of the Ridom scheme per subset (`kansasii-ridom/scripts/02_distance_matrices.py`, `output/kansasii-ridom/results/distance_summary.tsv`;
subsets are submatrices of the complex export, references included in the subset of their species; pairs = within the subset):

| Subset | n (all genomes) | Median | Max | Identical pairs | n (study isolates) | Median (study) | Max (study) | Identical pairs (study) |
|---|---|---|---|---|---|---|---|---|
| complex | 181 | 1132 | 1356 | 6 | 171 | 329 | 1352 | 6 |
| kansasii | 123 | 170 | 910 | 1 | 121 | 172 | 910 | 1 |
| pseudokansasii | 21 | 7 | 475 | 5 | 19 | 6 | 27 | 5 |
| persicum | 29 | 535.5 | 730 | 0 | 27 | 540 | 730 | 0 |
| attenuatum | 3 | 783 | 803 | 0 | 2 | 733 | 733 | 0 |
| ostraviense | 2 | 258 | 258 | 0 | 1 | - | - | 0 |
| innocens | 2 | 543 | 543 | 0 | 1 | - | - | 0 |
| gastri | 1 | - | - | - | 0 | - | - | 0 |

"Study isolates" (`study_*` columns of `distance_summary.tsv`) leave out the `GCF_*` references **and** the control / type strains (strains with a `LABEL`, e.g. `M_kansasii_ATCC_12478`). The report and `08_paper_numbers.py` use these (kansasii 172, persicum 540, pseudokansasii 6). The `iso_*` columns leave out only the references (171 / 539 / 6) and are not cited.

The attenuatum, ostraviense, innocens and gastri rows are the species of the combined `minor` subset of `SUBSETS` (all genomes: n = 8, median 1253, max 1279, 0 identical pairs; study isolates: n = 4, median 1242, max 1261, 0 identical pairs); the script writes both the combined `minor` matrix and one matrix per species. gastri is a single isolate, so it has no pair. With 2-3 isolates the medians are single distances, not distributions.

Note: Ridom's scheme (about 1,400 loci named after ATCC 12478 `MKAN_RS*` locus tags) is a different scheme from the chewBBACA one
(3,647 cgMLST95 loci). Distances and cluster numbers from the two are not comparable, and the Ridom ones win.

## What comes from Ridom and what is derived

Only five GUI exports are needed (one export per source, everything else is computed from it by `kansasii-ridom`; no export is
requested that a script can derive). `config/expected_exports.tsv` lists them; `00_check_exports.py` checks them.

| Export (SeqSphere+) | File | Status |
|---|---|---|
| Comparison table (allele profiles), pool + references | `ridom-comparison-table.csv` | have |
| Pairwise allele distances, whole complex, pairwise ignore | `ridom-distance-matrix.meg` | have |
| Cluster table (`-Group-`) | `ridom-clusters.csv` | have |
| Scheme as task template (holds the targets **and** the Target Definer report) | `ridom-scheme.tasktemplate` | have |
| MST figures of the whole complex, as drawn for the report (SVG + PNG) | `ridom-mst-{species,cluster,species-and-cluster}.{svg,png}`: coloured by species, by cluster, by both | have (2026-11-02); presence only, layout and colours are not reproducible in code, no script reads them |

Derived tables (`output/kansasii-ridom/results/`, run `sbatch submit_all.sbatch`):

| Need | Script | Output |
|---|---|---|
| Distances per subset | `02_distance_matrices.py` | `distance_<subset>.tsv`, `distance_summary.tsv` |
| Scheme: targets, Target Definer settings, filters, funnel, genomes | `03_scheme.py` | `scheme_targets.tsv`, `scheme_loci_classes.tsv` (core / accessory / discarded), `scheme_filters.tsv`, `scheme_funnel.tsv`, `scheme_genomes.tsv`, `scheme_summary.tsv`, `scheme_parameters.txt`, `scheme_target_definer_report.txt` |
| Per-isolate QC, failed targets, locus statistics | `04_qc.py` | `qc.tsv`, `qc_summary.tsv`, `target_failures.tsv`, `locus_stats.tsv` |
| Clusters for all isolates incl. singletons, threshold | `05_clusters.py` | `clusters.tsv`, `cluster_summary.tsv`, `cluster_threshold.tsv` |
| MST nodes and edges, UPGMA trees per subset | `06_mst_trees.py` | `mst_nodes.tsv`, `mst_edges.tsv`, `tree_upgma_<subset>.nwk` |
| Controls vs. references | `07_control_distances.py` | `control_distances.tsv` |
| Numbers and species table for the text | `08_paper_numbers.py` | `paper_numbers.md`, `paper_species_table.tsv` |

Findings of the derivation (exports of 2026-11-02):

- **Ridom's MST clusters are single linkage at <= 5 allele differences**: that threshold (and only that one) reproduces the 18 clusters of `ridom-clusters.csv`
  exactly (`cluster_threshold.tsv`); isolates without `-Group-` are singletons.
- The comparison table has no failure reason and no "new allele" flag, so `target_failures.tsv` lists targets without an allele only. There is no export for
  reasons; if a reason is needed for the text, it has to be looked up in the GUI.
- The task template has no genomic coordinates of the targets (only locus tag, length, strand); coordinates would come from the ATCC 12478 annotation.
- MST edges are recomputed from the Ridom distances (same total length as Ridom's MST, tie-breaking can differ); use the Ridom SVG for the figure.
- Not exported and not needed: MLST (stays from `ASSEMBLIES/<sample>/5_typing/mlst/`), isolate-data import log (`ridom/metadata.tsv` of `01_export_ridom.py` is the source).

## Not available from Ridom (decide before final report)

SeqSphere+ works on allele profiles. It gives no SNP distances, so these findings of `kansasii-mst` have no Ridom equivalent:

- SNP counts between and within species, and the node-merge thresholds (kansasii 50, pseudokansasii 20, persicum 100 SNPs).
- The effect of masking PE/PPE, IS and phage regions (`core_snp_summary.tsv`).
- Resolution inside a clonal group where alleles are identical but SNPs differ (node `max_internal_snps`).

Options: (a) keep `kansasii-mst` for a supplementary SNP figure and say so in the methods; (b) drop the SNP statements and report allele
distances only. Until decided, `kansasii-mst` stays in the project but is not used for the main report.

## What `kansasii-mst` and `kansasii-cgmlst` feed

| Dependency | Where | Action |
|---|---|---|
| `cgmlst_called_pct` and `excluded` (< 90 % called) | `immensekansasii/scripts/06_screening_map_results.py` reads `output/kansasii-cgmlst/results/sample_qc.tsv` | planned: switch to the Ridom good-targets value (`ridom-comparison-table.csv` covers the pool incl. M055); keep the 90 % threshold |
| `run_downstream.sh` runs both repos | `immensekansasii/scripts/run_downstream.sh` | planned: drop `kansasii-mst` and steps 08-09 of `kansasii-cgmlst` after the switch, add `kansasii-ridom` `submit_export.sbatch` and `submit_all.sbatch` (not in the chain today) |
| `excluded` read by `kansasii-amr-marker-screen`, `kansasii-mst`, `kansasii-cgmlst` | `screening_map_results.csv` | unchanged |

## Where the Ridom results go

`kansasii-ridom` reads the exports. `scripts/00_check_exports.py` compares `data/imm/ridom-*` with the list above
(`config/expected_exports.tsv`, the five GUI exports) and writes `output/kansasii-ridom/results/export_status.tsv`; run it after every new export. All tables for the report are derived there by scripts 02-08 (table above). `immensekansasii/scripts/06`
joins `ridom-clusters.csv` into `screening_map_results.csv` (`ridom_*` columns). Do not extend `kansasii-mst` or `kansasii-cgmlst`.

## Export log

| Date | Files | SeqSphere+ version / scheme | Notes |
|---|---|---|---|
| 2026-10-30 (file date) | `ridom-clusters.csv` (export 5) | not recorded | 181 isolates (`keep` cohort + the 7 references); version and scheme to be filled in |
| 2026-11-02 (file date) | `ridom-comparison-table.csv` (export 1) | not recorded | 182 isolates incl. M055 and the 7 references, 1,407 loci; checked by `00_check_exports.py` (OK) |
| 2026-11-02 (file date) | `ridom-distance-matrix.meg` (export 2) | not recorded | MEGA (`DataType=distance DataFormat=LowerLeft`), 181 taxa (`keep` cohort + references, without M055); **missing-value handling not recorded in the file: pairwise ignore intended, to be confirmed**; subsets are sliced by `kansasii-ridom/scripts/02_distance_matrices.py` |
| 2026-11-02 | `ridom-scheme.tasktemplate` (export 6) | Ridom Typer 12.0.7 (2026-09), cgMLST Target Definer 1.5, run 2026-10-29 | scheme `... cgMLST 1407 targets ATCC 12478`; 1,407 core, 3,854 accessory, 503 discarded; read by `03_scheme.py` |
