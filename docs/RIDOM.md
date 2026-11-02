# Ridom SeqSphere+ as source of truth

Decision of 2026-10-30: **Ridom SeqSphere+ is the source of truth for the typing results (cgMLST, MST, clusters) and for the final
report.** `kansasii-mst` (core-SNP MST) and `kansasii-cgmlst` (chewBBACA scheme, Ridom-style MST) are **obsolete**: their outputs are
kept for comparison and are not cited in the final report, except for the gaps listed under "Not replaceable by Ridom" until those
are decided.

## Rules

- Ridom is operated in the GUI. Every export goes to `data/imm/` as `ridom-<content>-mkan329[-<subset>].<ext>` (CSV, `;`-separated as
  SeqSphere writes it; figures as SVG/PDF). Do not edit exported files; derived tables belong in `output/`.
- `data/imm/` files have no MANIFEST. Record each export in the table below (date, SeqSphere+ version, project, who) when you add it.
- The input to Ridom is `output/kansasii-ridom/ridom_assemblies.{tar.gz,zip}` (made by `kansasii-ridom/scripts/01_export_ridom.py`, `sbatch submit_export.sbatch`;
  isolates `M001` ..., controls by `LABEL`, references by accession; `ridom/metadata.tsv` for the isolate-data import). It holds the pool of 175 complex
  isolates (incl. M055, `excluded` by chewBBACA coverage only, so Ridom can give its good-target value) + 7 references = 182. Plasmids are removed by Ridom.
  The earlier archive of `kansasii-cgmlst` (181, without M055) is superseded; the 181 genomes are the same files, except that the ATCC 12478 reference
  now keeps its plasmid contig.
- Sample ids in Ridom exports: `Mkan329-081` is `M081`, controls use `LABEL` (`M_kansasii_ATCC_12478`, ...); `ridom_id()` in
  `immensekansasii/scripts/06_screening_map_results.py` converts.

## Exports in `data/imm/` today

| File | Content | Rows | Status |
|---|---|---|---|
| `ridom-clusters.csv` | good targets %, genome size, sample id, species, MST cluster (`-Group-`) | 181 | complete cohort; `-Group-` set for 63 of 181 (the rest are not in a cluster) |
| `ridom-comparison-table.csv` | allele table: missing-value count, good targets, size, id, species, 1,408 `MKAN_RS*` loci | 182 | complete: pool incl. M055 + the 7 references |
| `ridom-distance-matrix.meg` | pairwise allele distances (MEGA, lower triangle), whole complex | 181 taxa | complete: `keep` cohort + references, without M055; missing-value handling to be confirmed (export log) |
| `ridom-scheme.tasktemplate` | gzip XML: 1,407 core targets and the full Target Definer report (settings, filters, accessory / discarded lists) | 1,407 targets | complete; read by `03_scheme.py` |
| `ridom-kansasii-plasmids.csv` | NCBI plasmid list that the Target Definer excluded | - | used in `PLASMIDS.md` only |

Allele distances of the Ridom scheme per subset (`kansasii-ridom/scripts/02_distance_matrices.py`, `output/kansasii-ridom/results/distance_summary.tsv`;
subsets are submatrices of the complex export, references included in the subset of their species; pairs = within the subset):

| Subset | n | Median distance | Max | Identical pairs |
|---|---|---|---|---|
| complex | 181 | 1132 | 1356 | 6 |
| kansasii | 123 | 170 | 910 | 1 |
| pseudokansasii | 21 | 7 | 475 | 5 |
| persicum | 29 | 535.5 | 730 | 0 |
| attenuatum | 3 | 783 | 803 | 0 |
| ostraviense | 2 | 258 | 258 | 0 |
| innocens | 2 | 543 | 543 | 0 |
| gastri | 1 | - | - | - |

The attenuatum, ostraviense, innocens and gastri rows are the species of the combined `minor` subset of `SUBSETS` (n = 8, median 1253, max 1279, 0 identical pairs); the script writes both the combined `minor` matrix and one matrix per species. gastri is a single isolate, so it has no pair. With 2-3 isolates the medians are single distances, not distributions.

Note: Ridom's scheme (about 1,400 loci named after ATCC 12478 `MKAN_RS*` locus tags) is a different scheme from the chewBBACA one
(3,646 cgMLST95 loci). Distances and cluster numbers from the two are not comparable, and the Ridom ones win.

## What comes from Ridom and what is derived

Only five GUI exports are needed (decision 2026-11-02: one export per source, everything else is computed from it by `kansasii-ridom`; no export is
requested that a script can derive). `config/expected_exports.tsv` lists them; `00_check_exports.py` checks them.

| Export (SeqSphere+) | File | Status |
|---|---|---|
| Comparison table (allele profiles), pool + references | `ridom-comparison-table.csv` | have |
| Pairwise allele distances, whole complex, pairwise ignore | `ridom-distance-matrix.meg` | have |
| Cluster table (`-Group-`) | `ridom-clusters.csv` | have |
| Scheme as task template (holds the targets **and** the Target Definer report) | `ridom-scheme.tasktemplate` | have |
| MST figures per subset (SVG or PDF, as drawn for the report) | `ridom-mst-<subset>-mkan329.{svg,pdf}` for complex, kansasii, pseudokansasii, persicum, minor | **missing**: layout and colours are not reproducible in code |

Derived tables (`output/kansasii-ridom/results/`, run `sbatch submit_all.sbatch`):

| Need | Script | Output | Replaces |
|---|---|---|---|
| Distances per subset | `02_distance_matrices.py` | `distance_<subset>.tsv`, `distance_summary.tsv` | `allele_distance_*.csv` |
| Scheme: targets, Target Definer settings, filters, funnel, genomes | `03_scheme.py` | `scheme_targets.tsv`, `scheme_loci_classes.tsv` (core / accessory / discarded), `scheme_filters.tsv`, `scheme_funnel.tsv`, `scheme_genomes.tsv`, `scheme_summary.tsv`, `scheme_parameters.txt`, `scheme_target_definer_report.txt` | `scheme_summary.tsv`, `schema_evaluator_loci.tsv`, README "Scheme" table (no separate parameter export) |
| Per-isolate QC, failed targets, locus statistics | `04_qc.py` | `qc.tsv`, `qc_summary.tsv`, `target_failures.tsv`, `locus_stats.tsv` | `sample_qc.tsv`, `allele_call/` stats |
| Clusters for all isolates incl. singletons, threshold | `05_clusters.py` | `clusters.tsv`, `cluster_summary.tsv`, `cluster_threshold.tsv` | cluster / node tables |
| MST nodes and edges, UPGMA trees per subset | `06_mst_trees.py` | `mst_nodes.tsv`, `mst_edges.tsv`, `tree_upgma_<subset>.nwk` | `mst_nodes_*.tsv` |
| Controls vs. references | `07_control_distances.py` | `control_distances.tsv` | `control_check.tsv` |
| Numbers and species table for the text | `08_paper_numbers.py` | `paper_numbers.md`, `paper_species_table.tsv` | hand-copied numbers |

Findings of the derivation (2026-11-02):

- **Ridom's MST clusters are single linkage at <= 5 allele differences**: that threshold (and only that one) reproduces the 18 clusters of `ridom-clusters.csv`
  exactly (`cluster_threshold.tsv`); isolates without `-Group-` are singletons.
- The comparison table has no failure reason and no "new allele" flag, so `target_failures.tsv` lists targets without an allele only. There is no export for
  reasons; if a reason is needed for the text, it has to be looked up in the GUI.
- The task template has no genomic coordinates of the targets (only locus tag, length, strand); coordinates would come from the ATCC 12478 annotation.
- MST edges are recomputed from the Ridom distances (same total length as Ridom's MST, tie-breaking can differ); use the Ridom SVG for the figure.
- Not exported and not needed: MLST (stays from `ASSEMBLIES/<sample>/5_typing/mlst/`), isolate-data import log (`ridom/metadata.tsv` of `01_export_ridom.py` is the source).

## Not replaceable by Ridom (decide before final report)

SeqSphere+ works on allele profiles. It gives no SNP distances, so these findings of `kansasii-mst` have no Ridom equivalent:

- SNP counts between and within species, and the node-merge thresholds (kansasii 50, pseudokansasii 20, persicum 100 SNPs).
- The effect of masking PE/PPE, IS and phage regions (`core_snp_summary.tsv`).
- Resolution inside a clonal group where alleles are identical but SNPs differ (node `max_internal_snps`).

Options: (a) keep `kansasii-mst` for a supplementary SNP figure and say so in the methods; (b) drop the SNP statements and report allele
distances only. Until decided, `kansasii-mst` is obsolete for the main report but not deleted.

## Still depending on the obsolete repos

| Dependency | Where | Action |
|---|---|---|
| `cgmlst_called_pct` and `excluded` (< 90 % called) | `immensekansasii/scripts/06_screening_map_results.py` reads `output/kansasii-cgmlst/results/sample_qc.tsv` | switch to `ridom_perc_good_targets` once export 7 covers all complex isolates (incl. M055); keep the 90 % threshold |
| `run_downstream.sh` runs both repos | `immensekansasii/scripts/run_downstream.sh` | drop `kansasii-mst` and steps 08-10 of `kansasii-cgmlst` after the switch, add `kansasii-ridom` `submit_export.sbatch` |
| `excluded` read by `kansasii-amr-marker-screen`, `kansasii-mst`, `kansasii-cgmlst` | `screening_map_results.csv` | unchanged |

## Where the Ridom results go

`kansasii-ridom` (created 2026-10-30) reads the exports. `scripts/00_check_exports.py` compares `data/imm/ridom-*` with the list above
(`config/expected_exports.tsv`, the five GUI exports) and writes `output/kansasii-ridom/results/export_status.tsv`; run it after every new export. All tables for the report are derived there by scripts 02-08 (table above). `immensekansasii/scripts/06` still
joins `ridom-clusters.csv` into `screening_map_results.csv` (`ridom_*` columns). Do not extend the obsolete repos.

## Export log

| Date | Files | SeqSphere+ version / scheme | Notes |
|---|---|---|---|
| (earlier, undated) | `ridom-clusters.csv`, `ridom-comparison-table-mkan329.csv` | not recorded | version and scheme to be filled in |
| 2026-11-02 (file date) | `ridom-comparison-table-mkan329.csv` (export 1, replaces the 149-row file) | not recorded | 182 isolates incl. M055 and the 7 references, 1,408 loci; checked by `00_check_exports.py` (OK) |
| 2026-11-02 (file date) | `ridom-distance-matrix.meg` (export 2) | not recorded | MEGA (`DataType=distance DataFormat=LowerLeft`), 181 taxa (`keep` cohort + references, without M055); **missing-value handling not recorded in the file: pairwise ignore intended, to be confirmed**; subsets are sliced by `kansasii-ridom/scripts/02_distance_matrices.py` |
| 2026-11-02 | `ridom-scheme-mkan329.tasktemplate` (export 6) | Ridom Typer 12.0.7 (2026-09), cgMLST Target Definer 1.5, run 2026-10-29 | scheme `... cgMLST 1407 targets ATCC 12478`; 1,407 core, 3,854 accessory, 503 discarded; replaces the csv + parameters exports; `03_scheme.py` |
