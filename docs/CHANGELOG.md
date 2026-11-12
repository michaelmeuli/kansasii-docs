# Changelog

Notable changes to data tables and outputs, newest first.

## 2026-11-12 (stale-output check)
- All `MANIFEST*.txt` under `output/` compared with repo HEADs and input dates. Rerun, content unchanged (only the manifests are new): `output/kansasii-ridom/results/` (`submit_all.sbatch`, all 36 files byte-identical; the manifest named a commit older than the 11-08 distance tables), `output/gyrA-refalign/results/public_reads/hsp65_*` (`submit_hsp65_reads.sbatch`; the old manifest was from a dirty tree and older than its inputs), `output/immensekansasii/results/iTOL/mkan329/` (`07_generate_itol_species_labels.sh -m samples -p mkan329_`; labels and colour strip identical, the copied `screening_map_results.csv` is now the 11-12 table).
- `output/hsp65-refalign/results/figures/hsp65_identity_margin.{png,pdf}` redrawn with `03_figure.py` from the `reads.tsv` of 11-03: png byte-identical to the one of 11-01.
- `output/SUMMARY.html` regenerated (was from 11-03).
- **Not refreshed:** `output/hsp65-refalign/results/blast/` (10-16, older than `nonmatching_reads.fa` of 11-03; sends reads to NCBI), `output/immensekansasii/results/imm/` (legacy copy of `data/imm` with the old results table, written by no script), `output/immensekansasii/results/iTOL/mkan329_patients/` (superseded by `mkan329_patients171/`). Files before the rerun: `scratch/stale_refresh_before_20261112/`.

## 2026-11-12 (results table rebuilt: no MIC values for Mkan329-186)
- `screening_map_results.csv` (`data/imm/` and `output/immensekansasii/results/`) rebuilt with `06_screening_map_results.py`. The table dated from 2026-11-03, one day before kansasii-mic dropped Mkan329-186, and still carried its 13 MIC values. Now: the 39 MIC cells of 186 (`*_mic`, `*_modified_z`, `*_clsi_category`) are empty, 77 isolates with MIC data (was 78). The `*_modified_z` values of the other 76 isolates changed, as they are computed without 186. No other cell changed; `excluded` of 186 stays false (genome clean).
- `output/immensekansasii/results/iTOL/mkan329_patients171/itol_1_ast_dots.txt` regenerated (`12_generate_itol_ast.py`, env `biopython`): Mkan329-186 has no dots; tree, species ring and labels are identical. Resistant isolates per drug: CIP 13 -> 12, DOX 21 -> 20, ETO 2 -> 1, INH 1 -> 0, RIF 2 -> 1. `midpoint-rooted-tree.{pdf,svg}` were exported from iTOL again the same day (`data/imm/`, copied to that dir): 1,015 circles in the svg instead of 1,028 (13 dots of 186 gone, 5 of them filled). **Not redone:** `mkan329_patients/` (875-column tree).
- Manuscript: Figure 1 replaced by the new svg (`data/imm/midpoint-rooted-tree.svg`, embedded as svg as before); streptomycin modified z-score of Mkan329-142/-143 in section 3.4 corrected from 4.27 to 4.20 (the old value came from the October table with 83 streptomycin MICs).

## 2026-11-12 (docs: MIC exclusion rule, MLSA no-call count)
- `SPECIES.md`, `WORKFLOW.md`: the MIC exclusion rule is `excluded` = true plus `MANUAL_EXCLUSIONS` (Mkan329-186), as in `EXCLUSIONS.md`, not `contamination_flag` alone. "Only 035 has MIC data" was wrong: 7 of the 8 isolates had MIC data (010, 021, 035, 055, 106, 184, 186; `output/kansasii-mic/results/excluded_isolates.csv`); 113 has none.
- `SPECIES.md`, `EXCLUSIONS.md`: complex isolates without an MLSA call corrected from 67 of 177 to 68 of 175 (5 contaminated isolates left out, not 3). The species table was recounted and is unchanged. Docs only, nothing rerun.

## 2026-11-10 (tree figure redrawn)
- `data/imm/midpoint-rooted-tree.{pdf,svg}` replaced by the iTOL export of the 171-isolate tree (copy in `output/immensekansasii/results/iTOL/mkan329_patients171/`); the older render of the 875-column tree stays in `mkan329_patients/`. The svg shows the whole tree. The pdf was exported zoomed in and is cut off below the middle of the tree: export it again.
- Manuscript: Figure 1 replaced, sections 2.1 and 3.2, the caption, the limitation and the F6 path now describe the 171-isolate tree.

## 2026-11-10 (171-isolate tree in output)
- New `output/immensekansasii/results/iTOL/mkan329_patients171/`: core-SNP tree of the 171 clinical isolates alone (287,242 columns) with midpoint-rooted Newick and iTOL files, copied from the review's scratch dir; `README.md` and `make_tree.sbatch` in the dir. `mkan329_patients/` and `data/imm/midpoint-rooted-tree.{pdf,svg}` (875-column tree) are unchanged; the figure still has to be exported from iTOL by hand.

## 2026-11-09 (code review, core-SNP tree)
- Review of all repos: `mypy --strict` clean in all 11, `pytest` green (kansasii-mic 50, kansasii-cgmlst 10, kansasii-ridom 21, immensekansasii 12), every shell file parses, vendored `kansasii_paths` in sync. Changes only in `immensekansasii` (`modules/kansasii_phylo.nf`, `main.nf`, the two profiles) and in the docs. No result table was regenerated.
- **Finding: the `mkan329` tree (Figure "midpoint-rooted tree") rests on 875 SNP columns.** The snippy db holds six non-complex samples (controls Mkan329-126, -127, -129, -130, -131 and the *M. avium* isolate -184) that align 0.3-5 % of the ATCC 12478 reference, and `snippy-core` keeps only positions aligned in every sample. Rerun on the same db for the 171 clinical complex isolates only: 287,242 columns. In the 875-column core 2,539 of 14,535 isolate pairs are identical, in the 287,242-column core 11 (Mkan329-040 vs -005: 0 against 14,890 differences). Short or zero branches of the current figure are therefore not evidence of identity. Check outputs: `scratch/phylo_review_20261109/` (`all186/`, `patients171/`; iTOL inputs for a redrawn figure in `patients171/iTOL/`). The figure in `output/` and `data/imm/` was not replaced.
- **Finding: a failed tree step left an old tree in place.** `kansasii_snippy_core` / `kansasii_tree` failures were ignored by the profile's `errorStrategy`, so `runs/public_PRJNA1078897` still shows a 50-tip tree from 2026-10-20 although the db has 243 samples (SRR28038343 has no aligned base, `snp-sites` found no SNPs). The public trees are not used downstream.
- `kansasii_phylo.nf` fixes: new `--kansasii_min_aligned_fraction` (default 0 = leave out only empty or incomplete sample dirs; 0.3 keeps a run to the complex), per-sample table `kansasii_complex_core.samples.tsv` and `kansasii_complex_core.txt` published, the previous `kansasii_phylogeny/` is removed when a run starts, the db copy is renamed into place, `-resume` reruns `snippy-core` and the tree exactly when the db changed, IQ-TREE has a fixed seed and 2 h x attempt, and the step no longer depends on GTDB-Tk (it never used the species). Tested with a 4-sample harness (`scratch/phylo_review_20261109/nf_test/`): empty sample left out, unchanged `-resume` cached, deleted sample dir triggers a rebuild. Details: `WORKFLOW.md` 2d.

## 2026-11-04 (kansasii-mic: Mkan329-186 excluded)
- kansasii-mic drops Mkan329-186 (TNR 2020500010) via `MANUAL_EXCLUSIONS`: 'nicht rein' in `kansasii_list_JC.xlsx`, although CheckM is clean (0.68 %). Reran `output/kansasii-mic/results/`: MHK 78 -> 77 isolates (1,013 -> 1,000 rows), MGIT 66 -> 65 (1,218 -> 1,206 rows), isolates tested by both 18 -> 17. Other repos (cgMLST, MST, AMR screen) still include it. The same file also marks 2022500349 and 2022335425 'nicht rein'; not excluded.

## 2026-11-03 (MST exports)
- `kansasii-ridom/config/expected_exports.tsv`: the per-subset MST row (`ridom-mst-{subset}-mkan329.svg`) is replaced by the three whole-complex figures that exist (`ridom-mst-{species,cluster,species-and-cluster}.svg` in `data/imm/`), so `00_check_exports.py` no longer reports them MISSING (UNCHECKED: presence only). Files not renamed. `RIDOM.md` and the ridom README updated.

## 2026-11-03 (docs review)
- Documentation check of all `.md` files: fixed stale script names (`LIT.md`, hsp65 article), added `env_ridom` to the env list, corrected the Ridom export count (5, not 12) and the status of the MST figures in `RIDOM.md` / `kansasii-ridom/README.md`.
- Public samples with CheckM contamination above 5 % are now left out of gyrA-refalign (all gyrA results) and hsp65-refalign step 05 (`excluded_contaminated.tsv` in each); 29 public samples without a CheckM result are kept. Counts are in the two READMEs.
- New `docs/REPRODUCE.md`: ordered commands to reproduce the whole project.

## 2026-11-03 (shared cutoffs)
- New `kansasii-docs/templates/kansasii_cutoffs.py`: CLSI *M. kansasii* breakpoints, non-CLSI thresholds (EMB 8, INH 8, ETO 0.6, STR 16, CFZ 2 mg/L) and drug codes in one place. Vendored unchanged into `kansasii-mic/src/kansasii_mic/` and `immensekansasii/scripts/`; `repos/check_sync.sh` flags drift and `--fix` restores it. `kansasii_mic.breakpoints` and `12_generate_itol_ast.py` import it instead of keeping their own tables. The tree script's output is unchanged (it still has no clofazimine ring). kansasii-mic now also classifies Ethionamid (0.6 mg/L) and Streptomycin (16 mg/L) against these non-CLSI thresholds (they were left out before), so its MHK/MGIT overview tables gain those two drugs on the next run; `output/kansasii-mic/results/` has not been rerun.

## 2026-11-02 (rrs labels)
- `kansasii-amr-marker-screen/config/markers.tsv`: rrs rows relabelled after reading Wang 2019, Shrestha 2020 and Finken 1993 (`data/papers/`): "530 loop (positions 903-906)" is now "912 region (positions 903-906)"; "1401/1402 cluster II" is now "positions 1401/1402 (streptomycin link unverified)". Citekeys for the two rrs streptomycin rows are now verified. Details in `docs/REFERENCES.md`.
- `output/kansasii-amr-marker-screen/results/{assembly,bam}/work/report/` regenerated with `submit_amr_reannot.sbatch` (job 7970915, commit `1e664bf`, `MANIFEST.txt` in `results/assembly/`). Compared with the previous run: same row counts and same unplaced markers; only the two renamed `marker` labels differ (`marker_calls.tsv` 184 / 186 rows each in assembly / bam; `marker_calls.pass.tsv` 149 / 174). The `mut_with_mic.tsv` before/after was not compared. Neither renamed marker has a MUT call, so no downstream MIC table changed.

## 2026-11-02 (rename)
- `data/imm/ridom-comparison-table-mkan329.csv` renamed to `ridom-comparison-table.csv` (content unchanged). References updated in `kansasii-ridom/scripts/03_scheme.py`, `04_qc.py` and in `kansasii-docs/docs/{DATAFLOW,PLASMIDS,RIDOM}.md`. Older changelog entries and the RIDOM.md export history keep the old name, as it was current then.

## 2026-10-30 (Ridom archive with M055)
- `kansasii-ridom/scripts/01_export_ridom.py` (`sbatch submit_export.sbatch`) writes `output/kansasii-ridom/ridom_assemblies.{tar.gz,zip}`: the earlier Ridom input of `kansasii-cgmlst` (181) plus Mkan329-055 = 182 genomes, so Ridom can give a good-target value for M055 (needed to switch `excluded` to Ridom). References are taken unstripped from `GTDB_REPRESENTATIVES` (Ridom removes plasmids). `kansasii-cgmlst` step 10 and its archive are superseded.

## 2026-10-30 (kansasii-ridom)
- New repo `kansasii-ridom` (reads the Ridom exports, `scripts/00_check_exports.py` checks them against the 12 expected exports). New shared constant `OUT_RIDOM` in `templates/kansasii_paths.{py,sh}` (vendored copies synced in every repo). First check: `ridom-comparison-table-mkan329.csv` lacks 33 of 175 pool isolates (M055, M067-M098), `ridom-clusters.csv` is complete (181), the other 27 expected files are missing. Conda env `env_ridom` (environment.yml) is not built yet.

## 2026-10-30 (Ridom)
- Ridom SeqSphere+ is the source of truth for cgMLST, MST and clusters and for the final report. `kansasii-mst` and `kansasii-cgmlst` are marked obsolete (README/CLAUDE.md banners, `kansasii-docs/README.md`); outputs kept, nothing deleted. New `docs/RIDOM.md`: rules for GUI exports in `data/imm/ridom-*`, list of the 12 exports still needed, gaps (SNP distances have no Ridom equivalent), remaining dependencies (`excluded` still reads kansasii-cgmlst `sample_qc.tsv`). Found: `ridom-comparison-table-mkan329.csv` has 149 of 181 isolates (M067-M098 missing).

## 2026-10-30 (rename)
- `output/arm` renamed to `output/amr` (the temporary compat symlink `output/arm -> amr` was removed the same day); `kansasii-amr-marker-screen` scripts renamed `submit_arm*.sbatch` -> `submit_amr*.sbatch`, `run_arm*.sh` -> `run_amr*.sh`, `ARM_DIR` -> `AMR_DIR`. `output/amr_bam/refs` symlink repointed. Entries below and old logs keep the old name; column `arm_mut` of `screening_map_results.csv` is now `amr_mut` (header renamed in `data/imm`, `output/` and `output/imm` copies; flag `--arm-calls` is now `--amr-calls`).

## 2026-10-30
- `screening_map_results.csv` gains 4 columns at the end from `data/imm/ridom-clusters.csv`: `ridom_perc_good_targets`, `ridom_genome_size_mb`, `ridom_species`, `ridom_mst_cluster` (empty = no MST cluster). Joined in `immensekansasii/scripts/06_screening_map_results.py` on the Ridom sample name (Mkan329-NNN -> MNNN, controls by safe label); 174/186 isolates matched, the 7 GCF reference genomes of the Ridom file are not in the table.

## 2026-10-29
- New `docs/REFERENCES.md` and `docs/references.bib` (23 papers): sequence references (accessions, lengths, sequence checksums) and the literature behind each marker of `kansasii-amr-marker-screen`; 7 marker rows still have no source. New `kansasii-amr-marker-screen/scripts/verify_refs.sh` re-fetches the 9 numbering references from NCBI and checks the target coordinates against the GFF (all pass); table in `config/seq_refs.tsv`. `config/markers.tsv` gains a `citekey` column (BibTeX key; `proposed:` = candidate source, abstract read only); 9 more papers added to the bib for the unsourced rows.
- New figure `data/imm/midpoint-rooted-tree.{pdf,svg}` (copy in `output/iTOL/mkan329_patients/`): iTOL export of the midpoint-rooted patient tree with AST dots and species ring; made by hand, documented in `DATAFLOW.md` and `immensekansasii/WORKFLOW.md`.
- New `docs/PLASMIDS.md`: plasmids excluded from the Ridom targets (`data/imm/ridom-kansasii-plasmids.csv`) and from the kansasii-cgmlst scheme.
- `make_atypical_table.py` also writes `output/atypical_samples/ATYPICAL_SAMPLES.docx` (same tables as the .md, landscape A4; needs python-docx, so run it in `env_mlsa`).
- `kansasii-cgmlst/scripts/10_export_ridom.py` now also writes `output/ridom_assemblies.zip` (same files and layout as the tarball; verified against it).
- Deleted the stale `output/ridom/` (hand-made symlinks incl. `Mkan329-055`/`-184`, no references, unrenamed controls) and `output/ridom.zip`
  (a zip of it). The Ridom export is only `ridom_assemblies.tar.gz` / `.zip`.

## 2026-10-25
- **Repo layout and constants unified (all repos).** `templates/kansasii_paths.{py,sh}` define every shared path with one name; each repo vendors the
  Python file (checked by `check_sync.sh`). Renames: `GTDB_MLSA_ROOT`/`GTDB_GENOMES` -> `GTDB_COMPLEX_GENOMES`, `REFERENCES`/`GTDB_REPS` ->
  `GTDB_REPRESENTATIVES`, `REFERENCES_HSP65` -> `HSP65_AMPLICONS`, `SCREENING_MAP` -> `SCREENING_MAP_LINK`, `SCREENING_RESULTS` ->
  `SCREENING_MAP_RESULTS`, `SCREENING_MAP_TNR_COLUMNS` -> `TNR_COLUMNS`, `RES` -> `ASSEMBLIES`, `REF_FASTA/REF_GFF` -> `ATCC12478_FASTA/GFF`,
  `OUT` -> `OUTPUT`. Scripts take these paths as flags (`--gtdb-representatives`, `--hsp65-amplicons`, `--complex-genomes`, ...).
  Every repo reads `data/imm/screening_map_{link,results}.csv` (hsp65-refalign, gyrA-refalign, kansasii-amr-marker-screen read the `output/` copy before).
- Files moved: numbered entry scripts are in `scripts/` everywhere (hsp65-refalign, gyrA-refalign, kansasii-amr-marker-screen, sanger-microsynth
  `main1/main2` -> `01_fetch_mail.py`/`02_analyse_report.py`, mlsa-kansasii programs -> `scripts/04..10`, kansasii-mic `run_analysis.py` ->
  `01_run_analysis.py`); `run_all.sbatch` -> `submit_all.sbatch` (mst, cgmlst); sbatch files only at the repo root; amr tables in `config/`;
  mlsa `*_excluded` programs -> `--exclude-atypical`; conda env `kansasii_mic` -> `env_mic`.
- kansasii-cgmlst reads the cohort assemblies and the mlst type from the pipeline results (`ASSEMBLIES`) instead of the hand-made `output/ridom/`
  symlinks and `manifest.tsv`; the Ridom tarball has `output/ridom_assemblies.MANIFEST.txt`.
- hsp65-refalign: the Korean-type check wrote its manifest to a directory `korean_check/` that never held outputs; it is now
  `MANIFEST_korean_type_check.txt` next to the outputs. `submit_public.sbatch persicum` runs the in-silico hsp65 on all GTDB-persicum samples.
- `run_downstream.sh` now covers hsp65-refalign, gyrA-refalign, both cgMLST phases, the atypical-sample table and SUMMARY.html; whole chain rerun
  2026-10-25 (log `runs/downstream-20261025/`). Outputs of before the rerun: `output-old/pre-rerun_2026-10-25.tar.gz`, `pre-rerun_runs-cgmlst_2026-10-25.tar.gz`.
- New `docs/ATYPICAL.md` + `output/atypical_samples/` (samples with an atypical gyrA or hsp65, project and public), `docs/VENDORED.md`.
- Fixed strict-typing errors in `immensekansasii/scripts/06` and `10` (they had been unchecked).

## 2026-10-24
- `screening_map_results.csv`: `excluded` is now also true for non-complex clinical samples (`LABEL` empty, GTDB species outside the
  complex): NR 184 (*M. avium*). Non-complex control strains (NR 126, 127, 129, 130, 131) are unchanged. cgMLST/MST sample counts are
  unchanged (they already dropped 184 as "not in complex"); kansasii-amr-marker-screen keeps reporting it as `non_complex(avium)`.
  Full regeneration also refreshed `arm_mut` of NR 10, 21 and 55 (`rrs-A514C` -> empty, from the current `output/arm`).
  `output/imm/screening_map_results.csv` (2026-10-20) is an older copy and was not updated.
- New `docs/EXCLUSIONS.md`: which samples are excluded from which analysis, and why.

## 2026-10-23
- mlsa-kansasii programs renamed (dirs, scripts, `output/mlsa/` folders; file names inside unchanged): `main1_locus_discovery` -> `locus_discovery`,
  `main2_sanger_differentiation` -> `sanger_mlsa`, `main3_reference_alignment` -> `sanger_refalign` (+ `_hsp65_amplicons`, `_hsp65_iupac`),
  `main4_hsp65_vs_wgs` -> `sanger_vs_wgs`; `_excluded` suffixes kept. Columns of `sanger_vs_wgs/sanger_vs_wgs.tsv` renamed likewise
  (`main2_*` -> `sanger_mlsa_*`, `main3_*` -> `sanger_refalign_*`). Entries below use the old names.

## 2026-10-21
- `screening_map_results.csv`: new columns `cgmlst_called_pct` (% of cgMLST95 loci called, kansasii-cgmlst `output/cgmlst/sample_qc.tsv`) and
  `excluded` (= contaminated or < 90 % called) after `contamination_flag`. kansasii-cgmlst (steps 08-10), kansasii-mst and
  kansasii-amr-marker-screen use `excluded`; additionally excluded: Mkan329-055 only (81.5 %, as in Ridom). hsp65-refalign and
  mlsa-kansasii main4 stay on `contamination_flag` (species-call validation).
- kansasii-cgmlst: plasmid contigs of the reference genomes (pMK12478 of ATCC 12478) are removed before seeding, PTF training and allele calling.
- mlsa-kansasii `93de64d`, sanger-microsynth `ce2c956`: `_COMP` in `refalign.py` now has the full IUPAC complement (reverse-strand
  hits with R/Y/K/M/S/W were not complemented). mlsa-kansasii also gets opt-in `--iupac` alignment; tested on 127 hsp65 reads, no call
  changes, so the default stays. New output `output/mlsa/main3_reference_alignment_hsp65_iupac/` (runs B-E and the consensus references).
  See mlsa-kansasii README, section "IUPAC-aware alignment".
- `output/mlsa/main3_reference_alignment_hsp65_iupac/F_consensus_k1_noatypical/`: IUPAC consensus without the 3 Korean kansasii genomes; persicum margin 2.85 -> 7.1+, i.e. the narrow persicum/kansasii margin comes from those genomes (README, "The margin to the second-best species").

## 2026-10-20
- `output/ridom_assemblies.tar.gz` rebuilt by the new `kansasii-cgmlst/scripts/10_export_ridom.py`: it now holds real FASTA files
  (the old archive, 8 KB, contained only symlinks into `runs/`), 175 cohort isolates named `M001` ..., the control strains
  `Mkan329-128/-132/-133` as `M_kansasii_ATCC_12478`, `M_persicum_DSM_104278`, `M_pseudokansasii_DSM_107152`, the 7 public
  references (`GCF_*`) and `ridom/metadata.tsv` (species as `M. kansasii` ...). Same cohort as kansasii-cgmlst (complex species only,
  not contaminated), so the non-complex isolates of `output/ridom/` are no longer in the archive.
- `output/ridom/` (183 -> 181 assemblies): `Mkan329-010` (7.67 %) and `-021` (7.76 %) removed (and their symlinks), now
  `contamination_flag` = contaminated because `--max-contamination` is 5 % (was documented as 10 %); `manifest.tsv` filtered accordingly
  (ST, CheckM, species unchanged and consistent with `screening_map_results.csv`). Excluded now: `-010`, `-021`, `-035`, `-106`, `-113`.
- `output/cgmlst/` slimmed from 380 MB to 45 MB: working state (genome symlinks, `schema*`, `cgmlst_schema`, `loci_reports`, `cds_coordinates.tsv`, `results_contigsInfo.tsv`, logs) moved to `runs/cgmlst/`; only result tables, `cgMLST.html`, `schema_report.html` and `mst/` remain. kansasii-cgmlst scripts updated.
- `output/ridom/` (185 -> 183 assemblies): removed `Mkan329-009-jc` and `Mkan329-056-jc` (originals kept);
  `manifest.tsv` and `output/ridom_assemblies.tar.gz` updated. `Mkan329-035`, `-106`, `-113` are
  deliberately not in the export: CheckM contamination > 10 % (113 %, 20 %, 61 %), the
  `contamination_flag` threshold of `06_screening_map_results.py`; kansasii-cgmlst excludes the same
  flagged isolates (`scripts/common.py`). No other isolate is above 7.8 %.
- `screening_map_results.csv`: new column `NGS_USED` after `NGS_MM` (`NGS_MM` if done, else `NGS_JC`);
  immensekansasii commit `3a8fb7f`. All four copies updated.
