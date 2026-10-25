# Samples with an atypical gyrA or hsp65

Two marker genes decide how well the *M. kansasii* complex can be told apart by one locus: **gyrA** separates all seven species
(`mlsa-kansasii`, locus_discovery), **hsp65** (the routine Sanger target, 441 bp amplicon TB-11/TB-12(w)) does not (persicum and
kansasii are only 3 bases apart). A sample is called **atypical** here when one of these two genes disagrees with the species its
whole genome gives (GTDB-Tk / ANI), or is unlike every reference. This page lists every such sample, project isolates and public
data separately, says what is known about each and what is not.

**Source of truth:** `output/atypical_samples/atypical_samples.tsv` (one row per sample and flag, with strain, country and BioSample for
public samples) and `output/atypical_samples/ATYPICAL_SAMPLES.md` (the same as tables), written by
`kansasii-docs/bin/make_atypical_table.py` from the outputs of `hsp65-refalign` and `gyrA-refalign`. If this page and the table disagree,
the table wins. Figures below are from the run of 2026-10-25 (project: 186 rows of `screening_map_results.csv`, 178 Mkan329 isolates
after the reference strains 126-133; public: 1039 GTDB-complex samples of the four BioProjects).

## How atypical is decided

| Flag | Meaning | Severity |
|---|---|---|
| `hsp65_persicum_like` | genome is kansasii, hsp65 amplicon is closest to one of the three Korean-type kansasii genomes (the "atypical hsp65") or to persicum | major |
| `hsp65_other_species` | hsp65 amplicon (public: cut in silico from the assembly) or Sanger reads (project) are closest to another species than the genome | major |
| `gyrA_other_species` | gyrA is closest to another species than the genome (status `ok` or `ambiguous`) | major |
| `gyrA_divergent` | gyrA < 98 % identical to every reference (not a complex genome, or a new lineage) | major |
| `mixed_culture` | contaminated isolate (CheckM > 5 %) whose markers disagree | major |
| `gyrA_novel_haplotype` | gyrA identical to none of the 72 public genomes (closest named in `detail`); species call still agrees | minor |
| `gyrA_low_coverage` | assembly too fragmented to call gyrA (< 95 % of the 2514 bp probe placed) | minor |
| `hsp65_read_not_genome` | Sanger hsp65 read matches the isolate's own genome at < 90 %: the read is a co-amplified contaminant (*Rothia mucilaginosa*), the genome is clean | minor |

How the calls are made: hsp65-refalign README (reads and in-silico amplicons against the 72 per-genome amplicons; `ok` = >= 98 % identity
and >= 2 differences ahead of the next species); gyrA-refalign README (the persicum gyrA CDS laid over each assembly, same thresholds).
The 72 reference genomes are the public GTDB complex genomes (`GTDB_COMPLEX_GENOMES`).

## 1. Reference genomes: the three Korean *M. kansasii* with a persicum-like hsp65

GCF_002705785.1, GCF_002705825.1, GCF_002705865.1 (isolates K4, K14, K19, Samsung Medical Center, submitted by Borstel; `ATYPICAL_HSP65_GENOMES`).
They are *M. kansasii* sensu stricto: skani ANI 98.5-99.3 % to other kansasii and <= 93.95 % to every other species, identical to the type strain
at gyrA, gyrB, rpoB, recA, tuf, secA, 16S and ITS. Only hsp65 is atypical (11 SNPs in the 441 bp amplicon, persicum-like; Jagielski et al. 2019
call them hsp65 types Ib/IIb with WGS subtype I). The three are near-clonal (ANI 99.9-100), so effectively one lineage. Details:
`mlsa-kansasii/LIT.md`. They are kept in all reference sets, which is why a persicum read has a margin of only 2-3 to "kansasii"; the
`*_excluded` runs of mlsa-kansasii (`--exclude-atypical`) drop them as a sensitivity analysis. gyrA of all three is kansasii (leave-one-out
72/72 correct).

## 2. Project isolates (Mkan329-*)

**hsp65.** No uncontaminated kansasii isolate carries the Korean-type hsp65: of 122 kansasii isolates the closest the assembly amplicon comes to the Korean amplicon is
10 differences, and the farthest from the ATCC 12478 amplicon is 1 (`korean_type_check.tsv`). So the atypical lineage is **absent from the project**.
The Sanger hsp65 reads give 109 correct calls and 0 wrong among the 133 analysed isolates; 24 isolates have no call: 13 whose reads are a *Rothia mucilaginosa*
contaminant (`hsp65_read_not_genome`, genomes clean, CheckM <= 3.3 %), 11 whose traces are unusable or poor (details: hsp65-refalign README, `isolates.tsv`).

**gyrA.** gyrA agrees with the genome species in 171 of 171 callable uncontaminated isolates. No kansasii isolate is persicum-like at gyrA and all 28
persicum-like gyrA calls are genome-persicum. Exceptions and notes:

| Isolate | Genome | Finding | Reading |
|---|---|---|---|
| Mkan329-035 | kansasii | gyrA ostraviense, Sanger hsp65 ostraviense, assembly hsp65 closer to the Korean amplicon than to ATCC 12478 | **mixed culture** kansasii + ostraviense (CheckM contamination 113 %, `mlsa-kansasii/Mkan329-035_contamination.md`); excluded from analyses; not an atypical kansasii |
| Mkan329-184 | *M. avium* | gyrA divergent (89 % to persicum) | non-complex clinical sample, expected |
| Mkan329-010, -021, -113, -055 | persicum / kansasii | gyrA not callable (low coverage) | fragmented or contaminated assemblies (010, 021, 113 contaminated; 055 low cgMLST coverage) |
| 8 isolates with a gyrA haplotype that matches none of the 72 genomes | kansasii 050, 095, 161 (1 difference to GCA_002003585.1); persicum 009, 052, 058, 148; attenuatum 073 | `gyrA_novel_haplotype` | 1-7 differences to the closest genome, species call unchanged. Persicum and attenuatum have few reference genomes, so new haplotypes are expected |

## 3. Public data (four BioProjects, 1039 GTDB-complex samples)

**hsp65 (880 GTDB-kansasii assemblies, in silico).** 877 are closest to a typical kansasii reference with 0 differences. Three are not
(also in `immensekansasii/SPECIES.md`):

| Sample | BioProject | Origin | hsp65 | gyrA | Reading |
|---|---|---|---|---|---|
| SRR28038296 | PRJNA1078897 | Taiwan | closest the Korean-type genome GCF_002705785.1 (0 diffs), persicum 1 diff behind (`ambiguous`) | kansasii | the only **Korean-type hsp65 outside the three reference genomes** (1 of 880). Its rMLST profile has persicum-type alleles at S12 (176) and S7 (210) and typical kansasii ones at the other six genes, i.e. a mosaic: a persicum-derived region in a kansasii genome (not mapped) |
| SRR27048434 | PRJNA1048499 | | pseudokansasii (GCA_000524055.1, 0 diffs) | kansasii | GTDB-kansasii with a pseudokansasii hsp65; hsp65 is the only discordant gene, gyrA is kansasii. Sanger hsp65 would call it pseudokansasii |
| SRR27048675 | PRJNA1048499 | | attenuatum (GCA_002086865.1, 0 diffs) | kansasii | as above, attenuatum-like hsp65 |

For the 80 GTDB-persicum samples hsp65 was run separately (`output/hsp65_refalign/public_persicum/`, needed to judge the gyrA cases below).

**gyrA (1033 callable samples).** 1026 agree with the GTDB species. Seven disagree, **all in PRJNA1078897** (the Taiwan phylogeography study,
Emerg Infect Dis 2024, doi 10.3201/eid3008.240021):

| Sample | GTDB species | gyrA | Genome checks | Reading |
|---|---|---|---|---|
| SRR28038252 | persicum | kansasii | CheckM contamination 100 %, assembly 10.5 Mb | **mixed culture** (persicum + kansasii), explains the gyrA |
| SRR28038242 | persicum | kansasii | CheckM 0.45 %, MetaPhlAn persicum 99.8 %, ANI 99.5 % to persicum, ST 418 | clean persicum genome with kansasii gyrA |
| SRR28038316, -317, -318 | persicum | kansasii | CheckM 0.45 %, purity ~100 %, ANI 99.5 % to persicum, ST 418 | clean persicum genomes with kansasii gyrA: three samples of one batch carry the same pattern |
| SRR28038314, SRR28038483 | kansasii | persicum | CheckM 0.15 %, ANI 99.2 / 98.9 % to ATCC 12478 | clean kansasii genomes with a persicum gyrA; their hsp65 is kansasii (the 3-base persicum vs kansasii difference decides) |

The six clean ones (242, 316, 317, 318 persicum; 314, 483 kansasii) are **interspecies mosaics or recombinants** if the assemblies are right. CheckM and
MetaPhlAn argue against a mixed culture, but there was no read-level check (no mapping of the reads to both gyrA alleles) and no check whether the
region is related to the persicum-derived segment found in the project cohort by the GWAS work (`NC_022663.1:1,929,793-1,994,501`). This is **not
investigated further**; treat it as a lead.

Six public samples are too fragmented for gyrA (`gyrA_low_coverage`): SRR27048690 (PRJNA1048499), SRR12599239 and SRR12599307 (PRJNA323639), SRR19543410, -452, -482 (PRJNA845115).
Further, 77 public samples have a gyrA haplotype that matches none of the 72 genomes while the species call agrees (`gyrA_novel_haplotype`; 36 of them are kansasii:
880 samples, 31 haplotypes, 844 exact matches). They are listed in the table, not discussed here.

## What this means in practice

- A Sanger hsp65 call of persicum or kansasii is a 3-base decision and a Korean-type kansasii would be called persicum. Confirm those with **gyrA**
  (this is also what `sanger-microsynth` reports as "confirm with gyrA" when the closest reference is the atypical genome).
- In our cohort no isolate would have been misidentified by hsp65 because of an atypical lineage; the only discordant project sample is a mixed culture.
- In public data, discordance between gyrA/hsp65 and the genome species is rare (7 of 1033 for gyrA, 3 of 880 for hsp65 among kansasii) and concentrated in one
  BioProject, so use the genome (GTDB) species, not a marker, when assigning species to public data.

## Maintenance

Rerun `bash repos/immensekansasii/scripts/run_downstream.sh` (or the hsp65-refalign, gyrA-refalign and `make_atypical_table.py` steps) after new
isolates or public projects are added; update the numbers and the per-sample readings above. A new category needs an entry in
`make_atypical_table.py`, in the table "How atypical is decided" and in `README.md` of this repo.
