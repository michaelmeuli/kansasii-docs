# Reproducing the whole project

The commands to run, in order, to rebuild every result from the raw inputs on the s3it cluster. This file is
only the order and the commands; the reasons, options and checks are in `WORKFLOW.md`
(run order, the source of truth if the two disagree) and [DATAFLOW.md](DATAFLOW.md) (which file feeds which repo).
Code blocks use the full path and can be pasted as they are; only `<placeholders>` need filling in.

Time: step 4 (the pipeline) is the only long one (days of CPU). Step 5 is cheap and deterministic; rerun
it whenever the link table, the pipeline runs or the MIC inputs change.

Real runs go through `sbatch`/`srun`, not the shared login node. Run each block on a compute node
(`srun --pty -n 1 -c 6 --time=01:00:00 --mem=16G bash -l`) or submit it, unless it only prints or submits.

## 0. Inputs that cannot be regenerated

These must exist before anything runs. They come from the lab, the sequencing centre or Ridom, not from code.

| Path | Content |
|---|---|
| `data/imm/screening_map_{project,strains,ast,ast_jc,ngs_jc,ngs_mm}.csv` | screening map sources (uploaded from local, see WORKFLOW.md section 4) |
| `data/imm/mic.csv` | MIC table (MHK and MGIT) |
| `data/illumina/Mkan329/reads/kansasii/`, `reads/kansasii_jc/` | delivered paired-end fastq (NR 1-133 and NR 134-186) |
| `data/sanger/` | Sanger `.ab1` files |
| `data/imm/ridom-*` | Ridom SeqSphere+ GUI exports (manual, step 6) |
| `data/papers/`, `data/protocols/` | literature and lab protocols (documentation only) |

## 1. Clone and set up

```bash
export KANSASII_ROOT=/shares/sander.imm.uzh/MM/kansasii
cd $KANSASII_ROOT/repos
for r in immensekansasii mlsa-kansasii kansasii-mic hsp65-refalign gyrA-refalign kansasii-amr-marker-screen \
         kansasii-ridom kansasii-cgmlst kansasii-mst sanger-microsynth kansasii-docs; do
  [ -d $r ] || git clone git@github.com:michaelmeuli/$r.git
done
git -C immensekansasii checkout kansasii        # IMMENSE pipeline branch used by the project
ln -sfn $KANSASII_ROOT/repos/kansasii-docs/bin/check_sync.sh check_sync.sh
bash kansasii-docs/bin/install_hooks.sh         # pre-commit guard in every repo (re-run after a fresh clone)
```

Conda environments (one per repo; `hsp65-refalign`, `gyrA-refalign` and the `kansasii-docs` scripts share `env_mlsa`):

```bash
cd $KANSASII_ROOT/repos
conda env create -f immensekansasii/environment.yml                  # env_immense (nextflow, datasets CLI)
conda env create -f kansasii-mic/environment.yml                     # env_mic
conda env create -f mlsa-kansasii/environment.yml                    # env_mlsa
conda env create -f kansasii-amr-marker-screen/environment.yml       # env_amr
conda env create -f kansasii-ridom/environment.yml                   # env_ridom
conda env create -f kansasii-cgmlst/environment.yml                  # env_cgmlst (only for sample_qc.tsv)
conda env create -f kansasii-mst/environment.yml                     # env_mst (optional: not used for the report)
conda env create -f sanger-microsynth/environment.yml                # env_sanger_ms (routine only)
conda create -n biopython -c conda-forge biopython                   # used by 12_generate_itol_ast.py
```

Pipeline databases and containers (once; the full notes with every download are in
`immensekansasii/scripts/install_notes.txt`, target `/shares/sander.imm.uzh/software/pipelines/IMMense/IMMense_dependencies/`):

```bash
cd $KANSASII_ROOT/repos/immensekansasii
bash Singularity/pull_singularity_img.sh /shares/sander.imm.uzh/software/pipelines/IMMense/IMMense_dependencies/containers
# then MetaPhlAn4, BUSCO (bacteria_odb12, mycobacterium_odb12), GTDB-Tk r232 and the 16S db as in install_notes.txt
```

Check that all repos are clean and in sync (`--fix` restores the vendored shared files):

```bash
bash $KANSASII_ROOT/repos/check_sync.sh
```

## 2. Reference genomes (GTDB r232)

```bash
srun --pty -n 1 -c 6 --time=01:00:00 --mem=16G bash -l
conda activate env_immense
bash $KANSASII_ROOT/repos/immensekansasii/scripts/01_gtdb_mycobacteria_genomes.sh
```

Writes `data/gtdb_genomes/` and `output/immensekansasii/gtdb/gtdb232/` (representative lists, type strains).

## 3. Link table

```bash
conda activate env_mic
python $KANSASII_ROOT/repos/immensekansasii/scripts/02_screening_map_link.py
```

Writes `data/imm/screening_map_link.csv`. Everything below that reads isolates reads this table, so it is always built first.

## 4. IMMENSE pipeline runs (long)

`run_IMMENSE.sh` only submits a controller job and returns. Submit the next batch only after the previous one has finished
(`squeue -u $USER` shows no more `job_mkan329_*` / `nf-*` jobs): they share one run dir and one snippy db.
Each run has its own `runs/<run>/` and `--kansasii_snippy_db`; the db dir must exist (`mkdir -p`). The commands below build the tree as it is in the current results (all samples of the db; for `mkan329` that is an 875-column core alignment because of the six non-complex samples). Add `--kansasii_min_aligned_fraction 0.3` inside `-x "..."` to leave non-complex samples out of the tree (WORKFLOW.md 2d). The end results stay in
`runs/<run>/`, where every script reads them.

```bash
DB=/shares/sander.imm.uzh/software/pipelines/IMMense/IMMense_dependencies/databases/kansasii_complex
IMM=$KANSASII_ROOT/repos/immensekansasii
```

**4a. Reference tree of the 7 GTDB representatives** (`-t fasta`; builds the symlinks and submits the run):

```bash
bash $IMM/scripts/03_run_gtdb_tree.sh
```

**4b. Own isolates `mkan329`** (186 isolates: NR 1-133 from `reads/kansasii`, NR 134-186 from `reads/kansasii_jc`):

```bash
bash $IMM/scripts/04_mkan329_batches.sh          # test, b01..b04 (prints the commands below)
bash $IMM/scripts/05_mkan329_batch_jc.sh         # b05 (jc reads, NR 134-186); run AFTER 04, which deletes all bNN
bash $IMM/scripts/05_mkan329_batch_jc.sh -I "Mkan329-056 Mkan329-009" -x "" -s -jc -R mkan329_jc -o $KANSASII_ROOT/data/illumina/Mkan329/batches/b06   # b06
```

Pilot first (own run dir and db); check that all 3 isolates finish and the species calls are plausible:

```bash
mkdir -p $DB/mkan329_test $KANSASII_ROOT/runs/mkan329_test && cd $KANSASII_ROOT/runs/mkan329_test
bash $IMM/run_IMMENSE.sh -j job_mkan329_test -t fq_PE -r mkan329_test -x "--kansasii_snippy_db $DB/mkan329_test" \
     -i $KANSASII_ROOT/data/illumina/Mkan329/batches/test
```

Real run, one batch after the other (`b=b01`, then `b02`, `b03`, `b04`, `b05`, each only after the previous has finished):

```bash
mkdir -p $DB/mkan329 $KANSASII_ROOT/runs/mkan329 && cd $KANSASII_ROOT/runs/mkan329
b=b01
bash $IMM/run_IMMENSE.sh -j job_mkan329_$b -t fq_PE -r mkan329 -x "--kansasii_snippy_db $DB/mkan329" \
     -i $KANSASII_ROOT/data/illumina/Mkan329/batches/$b
```

The resequenced samples `b06` run separately (`runs/mkan329_jc`, db `mkan329_jc`; not used in the results table):

```bash
mkdir -p $DB/mkan329_jc $KANSASII_ROOT/runs/mkan329_jc && cd $KANSASII_ROOT/runs/mkan329_jc
bash $IMM/run_IMMENSE.sh -j job_mkan329_jc -t fq_PE -r mkan329_jc -x "--kansasii_snippy_db $DB/mkan329_jc" \
     -i $KANSASII_ROOT/data/illumina/Mkan329/batches/b06
```

**4c. Public reads** (four BioProjects; hundreds of GB, so the download is a job):

```bash
cd $IMM
P="PRJNA1078897 PRJNA1048499 PRJNA845115 PRJNA323639"
bash scripts/09_public_fetch_metadata.sh $P
sbatch --wrap "source \$(conda info --base)/etc/profile.d/conda.sh; conda activate env_mic; python scripts/10_public_select_and_download.py $P"
bash scripts/11_public_batches.sh PRJNA1078897      # per BioProject; prints the run_IMMENSE.sh commands (pilot first, then b01.. one after another)
```

Run the printed commands for each BioProject (run id `public_<BioProject>`, own snippy db).
The public BioProjects feed hsp65-refalign, gyrA-refalign and the AMR screen (step 6).

## 5. Downstream analyses (one command)

Everything after the pipeline runs (steps 2 and 6-14 of the "Run order" table in WORKFLOW.md): MIC analysis, MLSA, cgMLST QC, results table,
hsp65/gyrA reference alignment, iTOL files, samples report, AMR marker screen, atypical-sample table and `output/SUMMARY.html`
are submitted as a Slurm dependency chain.

```bash
bash $KANSASII_ROOT/repos/immensekansasii/scripts/run_downstream.sh --dry-run    # print the sbatch commands
bash $KANSASII_ROOT/repos/immensekansasii/scripts/run_downstream.sh              # submit (add --with-bam for the read-mapping AMR variant)
squeue -u $USER                                                                  # logs: runs/downstream-<date>/
```

What the chain runs, in dependency order (use this list to rerun a single step by hand; relative paths are under `repos/`, each repo's README has the flags):

| # | Step | Command |
|---|---|---|
| 1 | link table | `python immensekansasii/scripts/02_screening_map_link.py` (env_mic) |
| 2 | MIC analysis | `sbatch kansasii-mic/submit_mic.sbatch` |
| 3 | MLSA inputs | `mlsa-kansasii/scripts/01_download_filter_gtdb.sh`, `02_link_gtdb_kansasii_complex.sh`, `03_link_sanger_kansasii.sh` (env_mlsa) |
| 4 | MLSA programs | `sbatch mlsa-kansasii/submit_locus_discovery.sbatch`, `submit_locus_discovery_excluded.sbatch`, `scripts/06_make_hsp65_references.py`, `submit_sanger_mlsa.sbatch`, `submit_sanger_mlsa_excluded.sbatch`, `submit_sanger_refalign.sbatch`, `submit_hsp65_amplicon_alignment.sbatch`, `submit_genome_identity_check.sbatch` |
| 5 | cgMLST per-genome QC | `STEPS=00:01:02:03:04:05:06:07 sbatch --export=ALL kansasii-cgmlst/submit_all.sbatch` (only `sample_qc.tsv` is used) |
| 6 | **results table** | `python immensekansasii/scripts/06_screening_map_results.py` (env_mic; needs 2, 4, 5) |
| 7 | validation against the table | `sbatch mlsa-kansasii/submit_sanger_vs_wgs.sbatch`; `sbatch hsp65-refalign/submit_validate.sbatch`, `submit_korean_check.sbatch`, `submit_public.sbatch` (and `... persicum`); `sbatch gyrA-refalign/submit_gyrA.sbatch` |
| 8 | iTOL, samples report | `bash immensekansasii/scripts/07_generate_itol_species_labels.sh` (reference tree); `python immensekansasii/scripts/12_generate_itol_ast.py` (env `biopython`); `python immensekansasii/scripts/08_mkan329_samples_report.py` (from `immensekansasii/`) |
| 9 | AMR marker screen | `sbatch kansasii-amr-marker-screen/submit_amr.sbatch`, optional `submit_amr_bam.sbatch` (via `scripts/run_amr_bam.sh prepare/finish`), then `submit_amr_reannot.sbatch` |
| 10 | overview | `python kansasii-docs/bin/make_atypical_table.py; python kansasii-docs/bin/make_summary.py` (env_mlsa) |

Not in the chain: the pipeline runs (step 4), `kansasii-ridom` (step 6), `sanger-microsynth` (step 8), the NCBI BLAST of `hsp65-refalign/scripts/02_blast_reads.py`
(sends sequences out). `run_downstream.sh` also submits `kansasii-mst` and `kansasii-cgmlst` steps 08-09
(jobs `mst` and `cg2`); nothing depends on them and their outputs are not used for the report.

## 6. Ridom SeqSphere+ (source of truth for cgMLST, MST and clusters)

The typing results and the final report come from Ridom, which is operated in the GUI ([RIDOM.md](RIDOM.md)).

```bash
# 6a. genomes for Ridom: output/kansasii-ridom/ridom_assemblies.{tar.gz,zip} (175 isolates + 7 references)
sbatch $KANSASII_ROOT/repos/kansasii-ridom/submit_export.sbatch
```

6b. **Manual:** import the archive into SeqSphere+, run the cgMLST scheme and the MST, and export the tables to
`data/imm/ridom-<content>.<ext>` (do not edit them; the list of exports is in RIDOM.md).

```bash
# 6c. refresh the ridom_* columns of the results table (ridom-clusters.csv), then derive all tables of the report
python $KANSASII_ROOT/repos/immensekansasii/scripts/06_screening_map_results.py        # env_mic
sbatch $KANSASII_ROOT/repos/kansasii-ridom/submit_all.sbatch                            # output/kansasii-ridom/results/
```

## 7. Tree figure (manual)

`12_generate_itol_ast.py` (row 8 of the table in step 5) writes the iTOL files into `output/immensekansasii/results/iTOL/mkan329_patients171/`, from the 171-isolate tree in that directory. That tree is not made by the pipeline nor by `run_downstream.sh`: `sbatch immensekansasii/submit_patients171_tree.sbatch` makes it (see the `README.md` of the directory); rerun it when the snippy db or the `excluded` column changes, then rerun `12_generate_itol_ast.py`. Copy that directory to a laptop, upload
`kansasii_patients_midpoint.nwk` at <https://itol.embl.de>, drag in `itol_1_ast_dots.txt`, `itol_leaf_labels.txt` and last
`itol_2_species_ring.txt`, and export `data/imm/midpoint-rooted-tree.{pdf,svg}` by hand. Commands: WORKFLOW.md section 2c.

## 8. Routine: Sanger results by mail (independent)

Not part of the reproduction. It needs the mail account (`~/.config/sanger-microsynth/mail.env`, template `sanger-microsynth/mail.env.example`) and the
`mlsa-kansasii` hsp65 references from row 4 of the table in step 5.

```bash
sbatch $KANSASII_ROOT/repos/sanger-microsynth/submit_fetch_analyse.sbatch
```

## 9. Check the result

```bash
bash $KANSASII_ROOT/repos/check_sync.sh                       # repos clean, shared files in sync
python3 $KANSASII_ROOT/repos/kansasii-docs/bin/make_summary.py  # output/SUMMARY.html: manifests and figure index
```

Every result directory carries a `MANIFEST.txt` (script, commit, date, inputs; see [PROVENANCE.md](PROVENANCE.md)). Expected counts
after a full rerun: 186 rows in `screening_map_results.csv`, 186 with a species; 187 tips in the `mkan329` tree; pool of 175 and
`keep` cohort of 174 for Ridom ([EXCLUSIONS.md](EXCLUSIONS.md), [RIDOM.md](RIDOM.md)).

## Not reproducible by commands

- Files marked manual above: lab inputs (step 0), the Ridom GUI work (6b) and the iTOL figure (7).
