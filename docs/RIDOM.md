# Ridom SeqSphere+ as source of truth

Decision of 2026-10-30: **Ridom SeqSphere+ is the source of truth for the typing results (cgMLST, MST, clusters) and for the final
report.** `kansasii-mst` (core-SNP MST) and `kansasii-cgmlst` (chewBBACA scheme, Ridom-style MST) are **obsolete**: their outputs are
kept for comparison and are not cited in the final report, except for the gaps listed under "Not replaceable by Ridom" until those
are decided.

## Rules

- Ridom is operated in the GUI. Every export goes to `data/imm/` as `ridom-<content>-mkan329[-<subset>].<ext>` (CSV, `;`-separated as
  SeqSphere writes it; figures as SVG/PDF). Do not edit exported files; derived tables belong in `output/`.
- `data/imm/` files have no MANIFEST. Record each export in the table below (date, SeqSphere+ version, project, who) when you add it.
- The input to Ridom is `output/kansasii-cgmlst/ridom_assemblies.{tar.gz,zip}` (made by `kansasii-cgmlst/scripts/10_export_ridom.py`,
  isolates `M001` ..., controls by `LABEL`, references by accession; `ridom/metadata.tsv` for the isolate-data import). That script is
  the only part of `kansasii-cgmlst` still needed, until the export is moved or frozen.
- Sample ids in Ridom exports: `Mkan329-081` is `M081`, controls use `LABEL` (`M_kansasii_ATCC_12478`, ...); `ridom_id()` in
  `immensekansasii/scripts/06_screening_map_results.py` converts.

## Exports in `data/imm/` today

| File | Content | Rows | Status |
|---|---|---|---|
| `ridom-clusters.csv` | good targets %, genome size, sample id, species, MST cluster (`-Group-`) | 181 | complete cohort; `-Group-` set for 63 of 181 (the rest are not in a cluster) |
| `ridom-comparison-table-mkan329.csv` | allele table: missing-value count, good targets, size, id, species, 1,407 `MKAN_RS*` loci | 149 | **incomplete**: lacks the 32 isolates M067-M098 (mixed species), so no complete distance matrix can be derived from it yet |
| `ridom-kansasii-plasmids.csv` | NCBI plasmid list that the Target Definer excluded | - | used in `PLASMIDS.md` only |

Note: Ridom's scheme (about 1,400 loci named after ATCC 12478 `MKAN_RS*` locus tags) is a different scheme from the chewBBACA one
(3,646 cgMLST95 loci). Distances and cluster numbers from the two are not comparable, and the Ridom ones win.

## Exports still needed

Needed to replace the two repos. Each row names what it replaces.

| # | Export (SeqSphere+) | File name | Replaces |
|---|---|---|---|
| 1 | Complete comparison table (allele profiles) of all 181 genomes, **plus M055** (`excluded` at 81.5 % with chewBBACA; needs a Ridom good-target value) | `ridom-comparison-table-mkan329.csv` (replace the 149-row file) | `cgmlst/t0.95` allele table, `shared_loci_*.csv` |
| 2 | Pairwise allele-distance matrix per subset: complex, kansasii, pseudokansasii, persicum (+ attenuatum, ostraviense, innocens, gastri); state the missing-value handling (pairwise ignore vs. columns ignored) | `ridom-distance-<subset>-mkan329.csv` | `allele_distance_*.csv` |
| 3 | MST per subset as graph data: node membership (which isolates share a node), edge distances, the layout is not needed | `ridom-mst-nodes-<subset>-mkan329.csv` | `mst_nodes_*.tsv`, node merging of `kansasii-mst` |
| 4 | MST figures per subset (SVG or PDF, with the colouring used in the report) | `ridom-mst-<subset>-mkan329.{svg,pdf}` | `mst_cgmlst_*.{png,pdf}`, `mst_*.{png,pdf}` of the SNP MST |
| 5 | Cluster definition: distance threshold, linkage, and the cluster table for **all** isolates incl. singletons (today only 63 have a group) | `ridom-clusters.csv` (replace) | cluster/node tables, "≤ N SNPs" statements |
| 6 | Scheme definition: scheme name and version, SeqSphere+ version, Target Definer parameters, query genome, core and accessory target lists with locus tag, length, coordinates | `ridom-scheme-mkan329.csv` + `ridom-scheme-parameters.txt` | `scheme_summary.tsv`, `schema_evaluator_loci.tsv`, `cgmlst/` locus lists, README "Scheme" table |
| 7 | Per-isolate QC: good targets %, number of missing/failed/new-allele targets, genome size, assembly metrics | `ridom-qc-mkan329.csv` | `sample_qc.tsv` (`cgmlst_called_pct`), `allele_call/` stats |
| 8 | Per-isolate list of targets with a failure reason (not found, ambiguous, truncated) | `ridom-target-failures-mkan329.csv` | `allele_call` reports, `paralogous_loci.txt` |
| 9 | Allele-distance histogram or the distances between pairs used for statements in the text (replicates, controls vs. public references) | `ridom-control-distances-mkan329.csv` | `control_check.tsv` |
| 10 | Newick or other tree if a UPGMA/NJ tree is used next to the MST | `ridom-tree-<subset>-mkan329.nwk` | none yet (new) |
| 11 | MLST/ST as called by Ridom if a scheme is installed; otherwise ST stays from `ASSEMBLIES/<sample>/5_typing/mlst/` | `ridom-mlst-mkan329.csv` | ST column of `metadata.tsv` |
| 12 | Isolate-data import log (metadata that was loaded: species, ST, MIC, dates) | `ridom-isolate-data-mkan329.csv` | `ridom/metadata.tsv` |

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
| `run_downstream.sh` runs both repos | `immensekansasii/scripts/run_downstream.sh` | drop `kansasii-mst` and steps 08-09 of `kansasii-cgmlst` after the switch; keep step 10 |
| `excluded` read by `kansasii-amr-marker-screen`, `kansasii-mst`, `kansasii-cgmlst` | `screening_map_results.csv` | unchanged |

## Where the Ridom results go

`kansasii-ridom` (created 2026-10-30) reads the exports. `scripts/00_check_exports.py` compares `data/imm/ridom-*` with the list above
(`config/expected_exports.tsv`) and writes `output/kansasii-ridom/results/export_status.tsv`; run it after every new export. Tables and
figures for the report are added there as numbered scripts once an export format has been seen. `immensekansasii/scripts/06` still
joins `ridom-clusters.csv` into `screening_map_results.csv` (`ridom_*` columns). Do not extend the obsolete repos.

## Export log

| Date | Files | SeqSphere+ version / scheme | Notes |
|---|---|---|---|
| (earlier, undated) | `ridom-clusters.csv`, `ridom-comparison-table-mkan329.csv` | not recorded | version and scheme to be filled in |
