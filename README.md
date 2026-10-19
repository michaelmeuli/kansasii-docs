# kansasii project index

Entry point for the *M. kansasii* complex project (species differentiation, MIC, genotype vs
phenotype). Everything runs on the s3it cluster under `$KANSASII_ROOT`
(`/shares/sander.imm.uzh/MM/kansasii`; `~/kansasii` is a symlink to it). Code blocks in the docs
use the full path, so they can be pasted as they are.

This repo holds only the project-level documentation. The root `README.md` is a symlink to this
file. Repo-specific details live in each repo's own README.

## Directories

| Path | Content | Status |
|---|---|---|
| `repos/` | 10 git repos (table below) and `check_sync.sh` | active |
| `data/` | inputs only: GTDB genomes, Illumina reads, Sanger `.ab1`, `imm/` tables, lab protocols | active |
| `output/` | results, one directory per repo or analysis (see `output/README.md`) | active |
| `runs/` | Nextflow run dirs (large `work/`) and SLURM logs | temporary, large |
| `output-old/`, `output/mlsa-old` | superseded results (`output-old/README.md` lists them) | do not use |
| `scratch/` | unexplained one-off files (`scratch/README.md`) | safe to delete |
| `singularity_images_cache/` | container cache | regenerable |

**Rule:** scripts read from `data/` and `runs/` only. `output/` receives copies and results.

## Repos

| Repo | Purpose | Entry point |
|---|---|---|
| `immensekansasii` | IMMENSE pipeline (Nextflow, branch `kansasii`) plus project scripts that link, run and summarise it | `run_IMMENSE.sh`, `scripts/run_downstream.sh` |
| `kansasii-mic` | MIC outlier analysis (MHK and MGIT) | `scripts/run_analysis.py` |
| `mlsa-kansasii` | species-complex differentiation by MLSA, Sanger and reference alignment (main1-4) | `submit_*.sbatch` |
| `hsp65-refalign` | checks that hsp65 reference alignment of the Sanger reads gives the genome species | `01-04_*.py` |
| `kansasii-gwas` | genotype vs MIC: candidate genes, hotspots, lineages, recombination | `run_all.sbatch` |
| `kansasii-arm` | literature AMR-marker screen on assemblies and reads | `submit_arm*.sbatch` |
| `kansasii-mst` | core-SNP minimum spanning tree figures | `run_all.sbatch` |
| `kansasii-cgmlst` | chewBBACA cgMLST scheme and Ridom-style MST | `run_all.sbatch` |
| `sanger-microsynth` | routine: fetch Microsynth Sanger results by mail, identify, report | `submit_fetch_analyse.sbatch` |
| `kansasii-lit` | exploratory GTDB and type-strain look-ups (not in the run order) | `scripts/01-05` |

Check for uncommitted or unpushed work in all repos: `bash repos/check_sync.sh`.

## Where to read next

- **Run order and every script's inputs/outputs:** `repos/immensekansasii/WORKFLOW.md`.
- **Which file feeds which repo (with diagram):** [docs/DATAFLOW.md](docs/DATAFLOW.md).
- **Run everything after the pipeline:** `bash repos/immensekansasii/scripts/run_downstream.sh --dry-run`.
- **Samples, species, public data:** `immensekansasii/{SAMPLES,SPECIES,PROJECTS}.md`.
- **Draft article:** `hsp65-refalign/article/hsp65_differentiates_kansasii_complex.md` (the earlier
  mlsa-kansasii draft was merged into it).
- **Overview of all results:** `python3 repos/kansasii-docs/bin/make_summary.py` writes
  `output/SUMMARY.html` (manifests, figure index).
- **Git conventions:** `immensekansasii/GIT.md`.

## Conventions

- Scripts are numbered by the order they are called (`01_...`, `02_...`).
- Isolates are keyed by `PROBENNUMMER`; the link table is `data/imm/screening_map_link.csv`, the
  results table `data/imm/screening_map_results.csv`.
- Paths in scripts, sbatch files and docs are literal `/shares/sander.imm.uzh/MM/kansasii/...`;
  Python and shell code that honours `KANSASII_ROOT` says so in its header. If the project moves,
  `grep -r /shares/sander.imm.uzh/MM/kansasii repos` finds every place to change.
- SLURM job logs go to `output/<name>/logs/` (set by `#SBATCH --output`; the directory must
  exist before `sbatch`). `run_downstream.sh` logs to `runs/downstream-<date>/`.
- Real runs go through `sbatch`, not the login node (it is shared and can stall).
- Each result directory gets a `MANIFEST.txt` (script, commit, date, inputs) written by
  `repos/kansasii-docs/bin/write_manifest.sh`; see [docs/PROVENANCE.md](docs/PROVENANCE.md).
