# Changelog

Notable changes to data tables and outputs, newest first.

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
