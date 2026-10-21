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
  GTDB --> MLSA[mlsa-kansasii main1-3, genome_identity_check]
  SANG --> MLSA
  LT --> MLSA
  MLSA --> M4[main4 / hsp65-refalign]
  MIC --> RES[06 screening_map_results.py]
  MLSA --> RES
  PIPE --> RES
  RES --> RT[(screening_map_results.csv)]
  RT --> GWAS[kansasii-gwas]
  RT --> ARM[kansasii-amr-marker-screen]
  MIC --> GWAS
  MIC --> ARM
  PIPE --> GWAS
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
| `data/imm/screening_map_link.csv` | `immensekansasii/scripts/02_screening_map_link.py` | mic, mlsa, gwas, arm, mst, cgmlst |
| `data/imm/screening_map_results.csv` | `immensekansasii/scripts/06_screening_map_results.py` | gwas, arm (reannot), mlsa main4, iTOL, SAMPLES.md |
| `output/mic/{mhk,mgit}/` | `kansasii-mic/scripts/run_analysis.py` | results table, gwas, arm |
| `output/mlsa/main1..4/` | `mlsa-kansasii` sbatch programs | results table (`species_mlsa1/2`, `species_ref`), sanger-microsynth |
| `runs/<run>/` and `output/<run>/` | `run_IMMENSE.sh` | results table, gwas, arm, mst, cgmlst |
| `output/gwas/` | `kansasii-gwas/run_all.sbatch` | reports only |
| `output/arm/`, `output/arm_bam/` | `kansasii-amr-marker-screen/submit_arm*.sbatch` | reports only |

`screening_map_results.csv` has `NGS_USED` (after `NGS_MM`): the sequencing data used per isolate.
If `NGS_MM` was done it is used, not `NGS_JC`; `NGS_JC` only if there is no `NGS_MM` (Mkan329-001..133
= `NGS_MM`, 134..186 = `NGS_JC`). Mkan329-009 and -056 have both and use `NGS_MM`; their `-jc`
resequencing (run `mkan329_jc`) is not used. Copies: `data/imm/`, `output/`, `output/imm/`,
`output/iTOL/mkan329/` (06 only writes the first two; copy by hand).

The rows for mst, cgmlst and hsp65-refalign inputs were inferred from the repo summaries; check
each repo's README when relying on them.
