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
| `repos/` | 10 git repos (table below) and `check_sync.sh` (link to `kansasii-docs/bin/check_sync.sh`) | active |
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
| `kansasii-mic` | MIC outlier analysis (MHK and MGIT) | `submit_mic.sbatch` (`scripts/01_run_analysis.py`) |
| `mlsa-kansasii` | species-complex differentiation by MLSA, Sanger and reference alignment | `submit_*.sbatch` (`scripts/04-10_*.py`) |
| `hsp65-refalign` | checks that hsp65 reference alignment of the Sanger reads gives the genome species; atypical hsp65 in project and public assemblies | `submit_validate/korean_check/public.sbatch` |
| `gyrA-refalign` | gyrA from assemblies vs 72 public genomes: persicum-like/other species, project and public separate | `submit_gyrA.sbatch` |
| `kansasii-amr-marker-screen` | literature AMR-marker screen on assemblies and reads | `submit_amr*.sbatch` |
| `kansasii-mst` | core-SNP minimum spanning tree figures | `submit_all.sbatch` |
| `kansasii-cgmlst` | chewBBACA cgMLST scheme and Ridom-style MST | `submit_all.sbatch` |
| `sanger-microsynth` | routine: fetch Microsynth Sanger results by mail, identify, report | `submit_fetch_analyse.sbatch` |
| `kansasii-docs` | this index, data flow, provenance, shared constants (`templates/`), `bin/` helpers | `bin/check_sync.sh`, `bin/make_summary.py`, `bin/make_atypical_table.py` |

Check for uncommitted or unpushed work in all repos: `bash repos/check_sync.sh`.
The same script flags `.gitattributes` drift from `templates/gitattributes` (the shared
canonical copy; `--fix` restores it), `.vscode/settings.json` drift from
`templates/vscode-settings.json` (same `--fix`), `kansasii_paths.py` drift from `templates/kansasii_paths.py`, `.gitignore`
lines missing from `templates/gitignore`, a missing `README.md`/`CLAUDE.md`/`environment.yml`, sbatch files that are not
root-level `submit_*.sbatch`, a literal project root in code, and CRLF files. `bin/install_hooks.sh` installs a
pre-commit guard in every repo that blocks commits while `.gitattributes` differs; re-run
it after a fresh clone.

## Where to read next

- **Run order and every script's inputs/outputs:** `repos/immensekansasii/WORKFLOW.md`.
- **Which file feeds which repo (with diagram):** [docs/DATAFLOW.md](docs/DATAFLOW.md).
- **Which samples are excluded, and why:** [docs/EXCLUSIONS.md](docs/EXCLUSIONS.md).
- **Samples with an atypical gyrA or hsp65 (project and public):** [docs/ATYPICAL.md](docs/ATYPICAL.md); the table is
  `output/atypical_samples/atypical_samples.tsv`.
- **Sequence and literature references of the AMR marker screen (accessions, checksums, BibTeX):** [docs/REFERENCES.md](docs/REFERENCES.md), [docs/references.bib](docs/references.bib).
- **Code copied between repos (refalign, sanger_io, kansasii_paths):** [docs/VENDORED.md](docs/VENDORED.md).
- **Run everything after the pipeline:** `bash repos/immensekansasii/scripts/run_downstream.sh --dry-run`.
- **Samples, species, public data:** `immensekansasii/{SAMPLES,SPECIES,PROJECTS}.md`.
- **Draft article:** `hsp65-refalign/article/hsp65_differentiates_kansasii_complex.md` (the earlier
  mlsa-kansasii draft was merged into it).
- **Overview of all results:** `python3 repos/kansasii-docs/bin/make_summary.py` writes
  `output/SUMMARY.html` (manifests, figure index).
- **Git conventions:** `immensekansasii/GIT.md`.

## Repo layout

Every code repo has the same skeleton (`bash repos/check_sync.sh` checks the parts that can be checked):

```
README.md  CLAUDE.md  environment.yml  pyproject.toml (mypy --strict)  .gitignore  .gitattributes  .vscode/settings.json
<package>/        importable code (mlsa, sanger_ms, hsp65_refalign, gyrA_refalign, src/kansasii_mic); holds kansasii_paths.py
scripts/          numbered entry points NN_name.{py,sh} in call order; kansasii_paths.py here if there is no package
submit_<name>.sbatch   one per job, always at the repo root; log in output/<name>/logs/ via #SBATCH --output
config/           small tab-separated inputs of the analysis (kansasii-amr-marker-screen only)
tests/            pytest (kansasii-mic, kansasii-cgmlst, immensekansasii)
```

Conda environments are `env_<short name>`: `env_immense`, `env_mic`, `env_mlsa` (also hsp65-refalign, gyrA-refalign, kansasii-docs
bin scripts), `env_amr`, `env_cgmlst`, `env_mst`, `env_sanger_ms`; `env_typecheck` holds mypy. `immensekansasii` keeps the upstream
IMMENSE layout (`main.nf`, `modules/`, `bin/`) next to its project `scripts/`. `kansasii-docs` has `bin/`, `docs/`, `templates/`.

## Conventions

- Scripts are numbered by the order they are called (`01_...`, `02_...`).
- Isolates are keyed by `PROBENNUMMER`; the link table is `data/imm/screening_map_link.csv`, the
  results table `data/imm/screening_map_results.csv` (`output/` holds copies for download only).
- **One name per path.** `templates/kansasii_paths.py` (Python) and `templates/kansasii_paths.sh` (shell) define every shared path and
  list once, with the same names: `ROOT`, `DATA`, `RUNS`, `OUTPUT_ROOT`, `GTDB_DIR`, `GTDB_REPRESENTATIVES`, `GTDB_COMPLEX_GENOMES`,
  `HSP65_AMPLICONS`, `GYRA_REFERENCES`, `ATCC12478_FASTA`, `SCREENING_MAP_LINK`, `SCREENING_MAP_RESULTS`, `SANGER_LINK_DIR`,
  `ASSEMBLIES`, `public_assemblies(project)`, `PUBLIC_PROJECTS`, `SPECIES`, `SPECIES_COLORS`, `COMPLEX`, `REFERENCE_STRAINS`,
  `TNR_COLUMNS`, ... Each repo vendors the Python file unchanged next to its code; shell scripts and sbatch files `source` the shell file from
  kansasii-docs. A repo's own result directory is `OUTPUT = OUTPUT_ROOT / "<name>"`. Edit the template, never a copy
  (`bash repos/check_sync.sh --fix` restores the copies).
- **Paths are flags, not constants in the logic.** A script that reads one of these paths takes it as a flag whose default is the
  constant, e.g. `--gtdb-representatives`, `--hsp65-amplicons`, `--complex-genomes`, `--assemblies`, `--screening-map-results`, `--out`.
  So a different reference set or table needs no code change.
- The literal root `/shares/sander.imm.uzh/MM/kansasii` appears only in the bootstrap line `source "${KANSASII_ROOT:-/shares/.../kansasii}/repos/
  kansasii-docs/templates/kansasii_paths.sh"` of shell/sbatch files, in `#SBATCH --output=` lines (Slurm cannot expand variables there),
  in docs (so code blocks can be pasted) and as the fallback of `kansasii_paths.py`. `grep -rn /shares/sander.imm.uzh/MM/kansasii repos`
  lists them; moving the project means editing those and `KANSASII_ROOT`.
- SLURM job logs go to `output/<name>/logs/` (set by `#SBATCH --output`; the directory must
  exist before `sbatch`; `run_downstream.sh` creates them). `run_downstream.sh` logs to `runs/downstream-<date>/`.
- Real runs go through `sbatch`, not the login node (it is shared and can stall).
- Each result directory gets a `MANIFEST.txt` (script, commit, date, inputs) written by
  `repos/kansasii-docs/bin/write_manifest.sh`; a second job writing into the same directory uses `MANIFEST_NAME=MANIFEST_<job>.txt`,
  loose files in `output/` use `<file>.MANIFEST.txt`; see [docs/PROVENANCE.md](docs/PROVENANCE.md).
