# Data flow between repos

Derived from `immensekansasii/scripts/run_downstream.sh` and `WORKFLOW.md` (run order). If they
disagree with this file, they win; update this file.

```mermaid
flowchart TD
  subgraph inputs [data/]
    SM[imm/screening_map_*.csv]
    MICIN[imm/mic.csv]
    READS[illumina reads]
    SANG[sanger .ab1]
    GTDB[GTDB genomes]
  end
  SM --> LINK[02 screening_map_link.py]
  LINK --> LT[(screening_map_link.csv)]
  READS --> PIPE[IMMENSE pipeline, runs/]
  LT --> MIC[kansasii-mic]
  MICIN --> MIC
  GTDB --> MLSA[mlsa-kansasii (locus_discovery, sanger_mlsa, sanger_refalign), genome_identity_check]
  MLSA --> AMP[(HSP65_AMPLICONS)]
  SANG --> MLSA
  LT --> MLSA
  MLSA --> M4[sanger_vs_wgs]
  AMP --> HSPR[hsp65-refalign]
  RT --> HSPR
  PIPE --> HSPR
  GTDB --> GYR[gyrA-refalign]
  RT --> GYR
  PIPE --> GYR
  HSPR --> ATY[atypical gyrA/hsp65 table]
  GYR --> ATY
  MIC --> RES[06 screening_map_results.py]
  MLSA --> RES
  PIPE --> RES
  RES --> RT[(screening_map_results.csv)]
  RT --> ARM[kansasii-amr-marker-screen]
  MIC --> ARM
  PIPE --> ARM
  PIPE --> MST[kansasii-mst]
  PIPE --> CG[kansasii-cgmlst]
  RT --> ITOL[iTOL labels, SAMPLES.md]
  SANG --> MS[sanger-microsynth routine]
  MLSA -.references.-> MS
```

## Key files

| File | Produced by | Consumed by |
|---|---|---|
| `data/imm/screening_map_link.csv` | `immensekansasii/scripts/02_screening_map_link.py` | mic, mlsa, arm, mst, cgmlst |
| `data/imm/screening_map_results.csv` | `immensekansasii/scripts/06_screening_map_results.py` | arm (reannot), mlsa sanger_vs_wgs, hsp65-refalign, gyrA-refalign, iTOL, SAMPLES.md, mst, cgmlst (`excluded`) |
| `GTDB_REPRESENTATIVES` (`data/gtdb_genomes/.../kansasii_complex_gtdb_representatives/`) | `immensekansasii/scripts/03_run_gtdb_tree.sh` (links of the 7 type-strain genomes) | mlsa `09/10`, hsp65-refalign `01`, sanger-microsynth, cgmlst `00`, arm `03b` (flag `--gtdb-representatives` / `-g`) |
| `HSP65_AMPLICONS` (`.../kansasii_complex_hsp65_amplicons/`) | `mlsa-kansasii/scripts/06_make_hsp65_references.py` | hsp65-refalign `04/05`, mlsa `submit_hsp65_amplicon_alignment`, sanger-microsynth (flag `--hsp65-amplicons`) |
| `GYRA_REFERENCES` (`.../kansasii_complex_gyrA/`) | `gyrA-refalign/scripts/01` | gyrA-refalign `02/03` (flag `--gyra-references`) |
| `GTDB_COMPLEX_GENOMES` (`.../mlsa-kansasii/<species>/`) | `mlsa-kansasii/scripts/02_link_gtdb_kansasii_complex.sh` | mlsa `04/05/08`, gyrA-refalign `01` (flag `--complex-genomes`) |
| `output/cgmlst/sample_qc.tsv` | `kansasii-cgmlst/scripts/07_summarise_scheme.py` | results table (`cgmlst_called_pct`, `excluded`) |
| `output/mic/{mhk,mgit}/` | `kansasii-mic/submit_mic.sbatch` (`scripts/01_run_analysis.py`) | results table, arm |
| `output/mlsa/<program>/` (locus_discovery, sanger_mlsa, sanger_refalign, sanger_vs_wgs, ...) | `mlsa-kansasii` `submit_*.sbatch` (`scripts/04-10`) | results table (`species_sanger_mlsa`/`species_sanger_mlsa_excl`, `species_ref`), sanger-microsynth |
| `runs/<run>/` and `output/<run>/` | `run_IMMENSE.sh` | results table, arm, mst, cgmlst (reads `runs/mkan329/assembly/results/` directly), hsp65/gyrA-refalign |
| `output/hsp65_refalign/`, `output/gyrA_refalign/{project,public}/` | hsp65-refalign, gyrA-refalign `submit_*.sbatch` | `kansasii-docs/bin/make_atypical_table.py` |
| `output/atypical_samples/` | `kansasii-docs/bin/make_atypical_table.py` | reports only (docs/ATYPICAL.md) |
| `output/ridom_assemblies.tar.gz`, `output/ridom_assemblies.zip` | `kansasii-cgmlst/scripts/10_export_ridom.py` | Ridom SeqSphere+ (manual) |
| `output/arm/`, `output/amr_bam/` | `kansasii-amr-marker-screen/submit_arm*.sbatch` | reports only |

`screening_map_results.csv` has `NGS_USED` (after `NGS_MM`): the sequencing data used per isolate.
If `NGS_MM` was done it is used, not `NGS_JC`; `NGS_JC` only if there is no `NGS_MM` (Mkan329-001..133
= `NGS_MM`, 134..186 = `NGS_JC`). Mkan329-009 and -056 have both and use `NGS_MM`; their `-jc`
resequencing (run `mkan329_jc`) is not used. The canonical files are in `data/imm/` (`SCREENING_MAP_LINK`, `SCREENING_MAP_RESULTS`); scripts read only these. `output/` gets a copy
with a `<file>.MANIFEST.txt` from 02 and 06; `output/imm/` and `output/iTOL/mkan329/` hold older copies kept by hand (not read by any script).

`bash immensekansasii/scripts/run_downstream.sh` runs every row above except the pipeline and sanger-microsynth; the order of
its dependency chain is the order of this table.
