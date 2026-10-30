# Excluded samples and why

One place that lists which isolates/genomes are left out of which analysis. The per-sample source of truth is
`output/immensekansasii/results/screening_map_results.csv` (built by `immensekansasii/scripts/06_screening_map_results.py`); this file only
explains it. If the two disagree, the CSV wins. Counts as of 2026-10-24 (186 rows, NR 1-186). Rule: `excluded` = contaminated, or < 90 % cgMLST loci called, or a clinical sample (`LABEL` empty) outside the complex.

## 1. The `excluded` column

`excluded` = true when `contamination_flag` = `contaminated` (CheckM contamination > 5 %, `--max-contamination`), **or**
`cgmlst_called_pct` < 90 (Ridom's good-target threshold), **or** the row is a clinical sample (`LABEL` empty) whose GTDB species is
outside the complex (since 2026-10-24). Seven isolates:

| NR | Isolate | Species | Reason | Value |
|---|---|---|---|---|
| 10 | Mkan329-010 | persicum | contaminated | CheckM 7.67 % |
| 21 | Mkan329-021 | kansasii | contaminated | CheckM 7.76 % |
| 35 | Mkan329-035 | kansasii | contaminated | CheckM 113.37 % (diagnosis: `mlsa-kansasii/Mkan329-035_contamination.md`) |
| 55 | Mkan329-055 | persicum | low cgMLST coverage | 81.52 % of loci called (CheckM 2.47 %, not contaminated) |
| 106 | Mkan329-106 | kansasii | contaminated | CheckM 20.44 % |
| 113 | Mkan329-113 | persicum | contaminated | CheckM 61.40 % |
| 184 | Mkan329-184 | avium | not in the *M. kansasii* complex | clinical sample, `LABEL` empty |

Contaminated isolates are mixed cultures (see `immensekansasii/SPECIES.md`). CheckM is the criterion, not a species call.
The 5 % threshold was documented as 10 % until 2026-10-21; NR 10 and 21 sit between the two (CHANGELOG 2026-10-21).

## 2. Which analysis uses which rule

| Analysis | Rule | Source |
|---|---|---|
| kansasii-cgmlst steps 08-10 (distances, MSTs, Ridom export) | `excluded`. Step 00 takes 175 QC-passing assemblies: no contaminated, no non-complex; ATCC/DSM controls of complex species (NR 128/132/133) kept | `kansasii-cgmlst/README.md` |
| kansasii-mst | `excluded` = true, plus control strains (`LABEL` set) and non-complex species | `kansasii-mst/README.md`, `scripts/01_select_samples.py` -> `output/kansasii-mst/results/samples_used.tsv` |
| kansasii-amr-marker-screen | complex species with `excluded` = false | `kansasii-amr-marker-screen/README.md` |
| `output/kansasii-cgmlst/ridom_assemblies.tar.gz` and `.zip` (cgMLST step 10) | `keep`, as for the distance matrices and MSTs: 174 cohort assemblies (no `excluded`, no non-complex, so without 055 and 184; the 3 complex controls kept) + 7 public references = 181 | `kansasii-cgmlst/scripts/10_export_ridom.py` |
| gyrA-refalign | no exclusion: every Mkan329 isolate except the reference strains 126-133 is called; contaminated and non-complex isolates are flagged (`contaminated`, `wgs_species`) and listed in `docs/ATYPICAL.md` | `gyrA-refalign/README.md` |
| hsp65-refalign, mlsa `sanger_vs_wgs` | `contamination_flag` only (035, 106, 113 have an hsp65 read); validates species calls, so low cgMLST coverage is irrelevant | `hsp65-refalign/README.md` |
| kansasii-mic | flat-profile MIC rows (>= 8 distinct antibiotics with an identical point estimate within one TNR) go to `excluded_qc.csv` with `exclusion_reason`. Currently `output/kansasii-mic/results/mhk/excluded_qc.csv` has a header only, so no rows are removed. Isolates with `excluded=true` in `screening_map_results.csv` (previous run's table) are dropped before QC and listed in `results/excluded_isolates.csv`; `--keep-excluded` disables this | `kansasii-mic/README.md` |

hsp65-refalign removes 021, 035, 106 and 113 (136 complex isolates with an hsp65 read, 4 removed, 132 analysed; rerun 2026-10-25). The first run
(2026-10-16) predated the 5 % CheckM threshold and kept 021; Mkan329-010 has no Sanger hsp65 read, so it never appears there.

## 3. Non-complex and control strains

Control strains (`LABEL` set) are not marked `excluded` even when non-complex; complex-only analyses drop them by species/`LABEL`:

- Controls (`LABEL` set), NR 126-133: H37Rv, M. avium ATCC 19421, M. kansasii ATCC 12478, M. abscessus, M. xenopi, M. ulcerans (GTDB: marinum), M. persicum DSM 104278, M. pseudokansasii DSM 107152. MST drops all of them; cgMLST keeps the complex ones (128, 132, 133).
- Non-complex clinical sample: NR 184 (avium), now `excluded` = true (section 1).
- `immensekansasii/SPECIES.md` lists the non-complex species as avium 2, tuberculosis, abscessus, xenopi, marinum.

## 4. Reference genomes left out (mlsa-kansasii)

`*_excluded` variants of `locus_discovery` and `sanger_mlsa` (output: `output/mlsa-kansasii/results/locus_discovery_excluded`, `output/mlsa-kansasii/results/sanger_mlsa_excluded`)
drop three atypical Korean *M. kansasii* GTDB genomes: **GCF_002705785.1, GCF_002705825.1, GCF_002705865.1**.
This is a sensitivity check, not a correction: `mlsa-kansasii/LIT.md` explains why they are real *M. kansasii*.
A matching hsp65 variant exists (`submit_hsp65_iupac_excluded.sbatch`).

## 5. Per-analysis no-calls (not exclusions)

- hsp65 vs WGS: of 132 analysed isolates 108 get a call (all correct) and 24 do not: 13 Rothia mucilaginosa contaminant reads (genomes are clean), 10 unusable traces, 1 poor reads (Mkan329-102). These isolates stay in all genome analyses. Details in `hsp65-refalign/README.md`.
- 69 of 177 complex isolates have no MLSA call, probably missing Sanger reads (`immensekansasii/SPECIES.md`).

## 6. Resequenced duplicates

`NGS_USED` in `screening_map_results.csv` says which sequencing run is used per isolate (`NGS_MM` if present, else `NGS_JC`); the resequencing run `mkan329_jc` is otherwise not used (`DATAFLOW.md`).
Mkan329-056 was suspected contaminated, resequenced as `Mkan329-056-jc`; `contamination_flag` does not exclude it (`immensekansasii/WORKFLOW.md`).

## 7. Ridom export (`output/kansasii-cgmlst/ridom_assemblies.tar.gz`, `.zip`)

Rerun on 2026-10-24 (cgMLST step 10, job 7543102, 17.5 min) after `excluded` was extended to NR 184. The result is unchanged: the same 181
FASTA files plus `ridom/metadata.tsv`, identical content hashes (the tarball differs only in embedded timestamps). The export contains
the `keep` set (section 2): 174 cohort assemblies, 3 of them complex control strains (NR 128, 132, 133), plus the 7 public GTDB references.

| Species in the export | Genomes |
|---|---|
| *M. kansasii* | 123 |
| *M. persicum* | 29 |
| *M. pseudokansasii* | 21 |
| *M. attenuatum* | 3 |
| *M. innocens* | 2 |
| *M. ostraviense* | 2 |
| *M. gastri* | 1 |

Not exported: 12 of the 186 rows.

| Reason | Samples |
|---|---|
| Contaminated (CheckM > 5 %): mixed cultures | Mkan329-010 (7.67 %), -021 (7.76 %), -035 (113.37 %), -106 (20.44 %), -113 (61.40 %) |
| Low cgMLST coverage (< 90 % of loci called) | Mkan329-055 (81.52 %) |
| Not in the complex, control strains | Mkan329-126 (*M. tuberculosis* H37Rv), -127 (*M. avium* ATCC 19421), -129 (*M. abscessus*), -130 (*M. xenopi*), -131 (*M. ulcerans*) |
| Not in the complex, clinical sample | Mkan329-184 (*M. avium*) |

## Sample counts by stage

| Stage | Genomes | Notes |
|---|---|---|
| `screening_map_results.csv` | 186 | all rows |
| cgMLST step 00 / allele calling (pool: complex, not contaminated) | 175 (+ 7 public GTDB references) | includes NR 55 |
| cgMLST steps 08-10 (`keep`): distance matrices | 174 (+ 7 references) | 186 - 7 excluded - 5 non-complex controls; the 3 complex controls (NR 128, 132, 133) are kept |
| cgMLST complex MST (`output/kansasii-cgmlst/results/mst/mst_nodes_complex.tsv`) | 181 = 174 + 7 references | 179 nodes: genomes with identical allele profiles share a node |
| SNP MST (`output/kansasii-mst/results/mst_nodes_complex.tsv`, `samples_used.tsv`) | 171 | no references; the 3 controls are dropped as well; 78 nodes |

The MST outputs date from 2026-10-21, before NR 184 became `excluded`; the counts are unaffected because both repos already dropped it as "not in complex".

## Maintenance

Add a row here whenever a threshold, a flag or a hard-coded exclusion changes, and add the change to `CHANGELOG.md`.
