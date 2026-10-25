# Identifiers: why one thing has several numbers

The same strain, genome or sequencing run is known under different numbers in different places. Some are
labels for the same object, some are labels for related but different objects. This note sorts out which is which,
using the *M. kansasii* complex data of this project (mostly *M. ostraviense*, which shows nearly every case).

Sources of the examples: `data/lit/gtdb/gtdb232/` (GTDB r232 tables), type-strain
designations from LPSN, `data/imm/screening_map_*.csv` (lab numbers), `data/illumina/public/*/metadata.tsv` (SRA).

## 1. The one rule

> An identifier names **one kind of object**. Two numbers are only interchangeable if they name the same kind of object.

The kinds of object that get confused:

| Object | What it is | Identifier examples |
|---|---|---|
| Organism / strain | the living culture | `ATCC 12478`, `241/15`, `Mkan329-181` |
| Physical sample | what was taken from the patient or the tube | lab `TNR`, `LNR`, BioSample `SAMN07196566` |
| Study | a group of samples and data, one submission | BioProject `PRJNA1048499` |
| Sequencing run | one pass of one library on one instrument | `SRR27048379` |
| Assembly | a genome reconstructed from reads, one version | `GCA_002705925.1` / `GCF_002705925.1` |
| Taxon / name | the species label | NCBI taxid `2738409`, GTDB `s__Mycobacterium ostraviense` |

A strain has many assemblies; an assembly comes from many runs; a run belongs to one sample. Going from strain to assembly is
one-to-many, so a "different number" is often correct.

## 2. Type strain: one strain, many culture-collection numbers

A type strain is deposited in several culture collections, and each gives it its own number. They are all the same strain
(same culture lineage), as long as the collections hold true subcultures. LPSN lists them together:

| Species | Type strain designations (LPSN, as noted in `04_get_mkc_type_strains.sh`) | Genome used here |
|---|---|---|
| *M. kansasii* | ATCC 12478 = CIP 104589 = DSM 44162 = JCM 6379 = NCTC 13024 (= CCUG 27787, see amr-marker-screen README) | GCF_000157895.3 |
| *M. persicum* | AFPC-000227 = CIP 111197 = DSM 104278 | GCF_002086675.1 |
| *M. pseudokansasii* | MK142 = CCUG 72128 = DSM 107152 | GCF_900566075.1 |
| *M. innocens* | MK13 = CCUG 72126 = DSM 107161 | GCF_900566055.1 |
| *M. attenuatum* | MK41 = CCUG 72127 = DSM 107153 | GCF_900566085.1 |
| *M. ostraviense* | 241/15 = DSM 110538 = ITM 501146 | GCF_002705925.1 |
| *M. gastri* | DSM 43505 = ATCC 15754 = CCUG 20995 = CIP 104530 = JCM 12407 | GCF_002102175.1 |

Points to keep straight:

- "Type strain" is a property of the **strain**, not of a genome. A genome is "from type material" only if it was sequenced from that strain.
- Sequencing a type strain in two labs gives two genomes that differ slightly (sub-culturing, assembly method). In our cgMLST
  control strains, NR 128 (ATCC 12478) differs from GCF_000157895.3 by 3 alleles and NR 133 (DSM 107152) from GCF_900566075.1 by 8
  (`kansasii-cgmlst/README.md`). Same strain, not identical sequence.
- Do not assume a genome named for a species is the type strain. The public *M. persicum* genome GCF_002086675.1 is AFPC-000227
  (the type strain), but the lab control NR 132 is DSM 104278. Per LPSN these are the same strain, yet they differ by 117 cgMLST
  alleles. The cgMLST README attributes this to the public genome being a different isolate of AFPC-000227. That is the
  README's explanation and I have not checked it against the genome record.
- The type strain is not always typical. ATCC 12478 carries rpsL K43R (streptomycin resistant), so using it as the "wild-type"
  reference reverses the polarity of that marker (`kansasii-amr-marker-screen/README.md`).

### *M. ostraviense* has three GTDB genomes

| Assembly | Strain / name | BioSample | Level | Origin | Note |
|---|---|---|---|---|---|
| GCF_002705925.1 | **241/15** | SAMN07196566 | scaffold, 200 contigs | Karvina, Czech Republic | GTDB representative; NCBI: "assembly from type material" |
| GCF_021183725.1 | FDAARGOS_1613 | SAMN23242882 | complete genome | Braunschweig, Germany | US FDA, same species, not the type |
| GCF_001632895.1 | 1010001458 (assembly name `Mkan_typeIV_1.0`) | SAMN04599333 | scaffold, 187 contigs | Germany, tap water | University of Lodz; the assembly name suggests it was first treated as *kansasii* "type IV" |

Same species, three strains, three BioSamples, three assemblies. None of these numbers can stand in for another.

## 3. Genome accession numbers

`GCF_002705925.1` has three parts:

- **GCA_ vs GCF_.** `GCA_` is GenBank (INSDC archive, what the submitter deposited). `GCF_` is RefSeq (NCBI's re-annotated copy).
  The digits are the same, so `GCA_002705925.1` and `GCF_002705925.1` are the same assembly in two databases. Annotation
  and gene names (`MKAN_RS00015`, `NZ_` contigs) differ: RefSeq uses `NZ_` / `_RS` locus tags.
- **The number after the dot is the version.** `GCF_000157895.3` and `GCA_000157895.2` are not the same string. The assembly was
  re-processed, so versions differ, and GenBank and RefSeq version numbers are independent. `04_get_mkc_type_strains.sh`
  pins `GCA_000157895.2` for ATCC 12478 while the pipelines use `GCF_000157895.3`.
  Same digits plus a different version means "same submission, possibly changed sequence or annotation". Record the version.
- **GTDB adds `RS_` / `GB_`** (RefSeq or GenBank source) in front: `RS_GCF_002705925.1`. Strip it before comparing with NCBI.

Different accession families are not interchangeable:

| Prefix | Kind | Example |
|---|---|---|
| `GCA_` / `GCF_` | whole assembly | GCF_002705925.1 |
| `NKRE01000001.1` / `NZ_NKRE01000001.1` | one contig or scaffold | contig 1 of that assembly |
| `NKRE00000000.1` | the WGS project (all contigs of the assembly) | master record |
| `CP019883.1` | complete replicon (chromosome or plasmid) | ATCC 12478 chromosome record |
| `ASM270592v1` | assembly name, free text | name only, can repeat |
| `LAUMK13`, `HU_Myco_2024.1` | submitter's assembly name | not unique |

Note `GCF_040687845.1` (`HU_Myco_2024.1`) in the GTDB table: a second assembly of the same BioSample `SAMN02603596` as ATCC 12478,
but not the GTDB representative. Same strain, same sample, different assembly, different accession.

## 4. GTDB vs NCBI/other databases

GTDB and NCBI both keep genomes and species names, but they do not agree about either.

| | NCBI (RefSeq / Taxonomy) | GTDB |
|---|---|---|
| Species identity | taxon with a taxid (*M. ostraviense* = 2738409), name as submitted or curated | genome-based clusters (95% ANI); name inherited from the type genome or a representative |
| Which genomes count | any submitted assembly | quality-filtered assemblies; one **representative** per species cluster |
| Names | LPSN/ICNP-style, ids stable | can differ (placeholders, suffixes, split or merged genera); r226 and r232 differ in places |
| Type material | `ncbi_type_material_designation` per assembly | `gtdb_type_designation`, decided separately |
| Release | continuous | numbered releases (r226, r232), representatives can change between them |

What this means in practice:

- A genome's NCBI organism name can be wrong or out of date, and the GTDB name can differ from it. That is a **taxonomy** difference,
  not an accession problem. Always report the GTDB release (`r232`) with the name.
- The **type-material flag differs for the same genome.** In our r232 extract GCF_002705925.1 (241/15) is "assembly from type
  material" in NCBI, but the GTDB type-strain table
  (`kansasii_complex_type_strains.tsv`) lists six complex species and *M. ostraviense* is not one of them. GTDB therefore does
  not mark 241/15 as type strain of species there. I have not looked into why (it may be that GTDB's designation list has not
  caught up with a species described in 2020). The genome is still the GTDB representative, so using it as reference is fine.
- The representative can be replaced between releases (compare the r226 and r232 type-strain tables). Pin the accession, not "the GTDB representative".
- Other tools use their own numbering. MetaPhlAn4 reports species-level genome bins (SGBs, `mpa_vJan25_CHOCOPhlAnSGB`) and its
  own species names. GTDB-Tk, MetaPhlAn, hsp65 and 16S can each give a different species for one sample. Example: Mkan329-035
  is GTDB-Tk *kansasii* (ANI 99.66 to GCF_000157895.3), MetaPhlAn *ostraviense* and hsp65 *ostraviense*, because it is a mixed
  culture (see `immensekansasii/SPECIES.md`). Each tool reports one of the two species present.
- 16S cannot separate kansasii, ostraviense and gastri (identical sequences, see `mlsa-kansasii/LIT.md`), so a 16S "match" gives
  no information about which of the species is present.

## 5. The lab's numbers vs the public ones (using *M. ostraviense*)

For the one *M. ostraviense* isolate of the cohort the following numbers all refer to **one isolate**:

| Number | Where | What it names |
|---|---|---|
| `Mkan329-181` | `PROBENNUMMER` in `screening_map*.csv`, project sample ID | the project's isolate ID (the project label; `M181` in the Ridom cgMLST table) |
| `3188826` | `LNR` | lab number, joins to `screening_map_strains.csv` (meaning of the abbreviation not documented here) |
| `2022500313` | `TNR` / `TNR_JC` | lab number carried by the Sanger hsp65 trace file `2022500313 hsp65_Tb-11.ab1` |
| `2023187867` | `NGS_JC` | number in the NGS column of the JC table (presumably the one the Illumina data are filed under; not verified) |
| `GCF_002705925.1` | public | the public ostraviense reference genome (241/15), **not** this isolate |

Observations in the tables (`screening_map_link.csv`, rows 35 and 181):

- For Mkan329-181 the TNR (2022500313) and the NGS number (2023187867) **differ**. Presumably the NGS sample was registered separately
  from the Sanger sample (not verified); both belong to the same isolate. Other isolates (e.g. 001, 002) have identical TNR and NGS entries,
  so the lab's numbering rules are not uniform, and the mapping tables exist to resolve this.
- Mkan329-035 has TNR 2024500472 and a separate `MHK` number 2024311213 (MHK appears to be the MIC-side number; `MHK_TNR_DIFFERS` is a column in the link table).
  One isolate, two numbers by purpose.
- The lab's isolate numbers are **not** type-strain or accession numbers. `Mkan329-181` is a clinical isolate that GTDB-Tk calls
  *ostraviense* (ANI 99.54 to GCF_002705925.1). It is the same *species* as strain 241/15, not the same *strain*.

Caveat: I could not extract the text of the PDF report you mention, so I do not know which number it shows for ostraviense. If it
shows one of the numbers above, the table tells you what it names. If it shows a number that is not in this table (for example a
DSM or collection number), compare it with the type-strain table in section 2: `DSM 110538` is the ostraviense type strain.

## 6. NGS numbering

Sequencing data pass through several steps, and each step has its own accession.
Example, one public run (`data/illumina/public/PRJNA1048499/metadata.tsv`):

```
PRJNA1048499   BioProject  the study (many samples)
 └─ SAMN38644550  BioSample (sample_accession)   the isolate "961343"
     ├─ SRS19726859 SRA sample (secondary_sample_accession)   same sample, SRA's own number
     └─ SRX22738342 SRA experiment   one library prep + one instrument model
         └─ SRR27048379 SRA run      one sequencing run, gives the FASTQ files
              ├─ SRR27048379_1.fastq.gz   read 1 (forward)
              └─ SRR27048379_2.fastq.gz   read 2 (reverse)
```

| Prefix | Meaning | Hierarchy |
|---|---|---|
| `PRJNA` / `PRJEB` / `PRJDB` | BioProject (NCBI / ENA / DDBJ) | top |
| `SAMN` / `SAMEA` / `SAMD` | BioSample (NCBI / ENA / DDBJ) | sample |
| `SRS` / `ERS` / `DRS` | SRA sample | same sample as the BioSample |
| `SRX` / `ERX` / `DRX` | experiment (library + platform) | child of sample |
| `SRR` / `ERR` / `DRR` | run | child of experiment |

Rules:

- **The prefix letter shows the database that issued the number** (`S` NCBI, `E` ENA, `D` DDBJ). The three databases exchange data
  (INSDC), so the same run is available as `SRR…` at NCBI and, with the same number, at ENA. Prefix matters for new deposits;
  a `SRR` stays `SRR`.
- **Run ≠ sample.** One BioSample can have several runs (re-sequencing, top-up, different platforms). Counting runs overcounts
  isolates; counting BioSamples gives isolates. Check `sample_accession` for duplicates before using public data as an isolate count.
- **Run ≠ file.** Paired-end reads give two FASTQ files per run (`_1`, `_2`). `read_count` in the SRA metadata counts read
  **pairs**, `base_count` bases (about 2 × read length × pairs). Single-end runs have one file.
- **Run ≠ assembly.** An assembly (`GCA_`) is made from the reads of one or more runs, and the link is not always recorded. A
  genome in GTDB does not tell you which `SRR` it was built from, and a `SRR` does not tell you whether an assembly exists.
- **Same number, different content.** Run accessions are immutable once public, but assembly accessions change by version
  (section 3), and a BioSample can be edited (species name, strain). Cached metadata can be stale.
- **Species names in SRA are submitter-assigned.** `scientific_name = Mycobacterium kansasii` on a run says what the submitter wrote,
  not what GTDB says. Several public "kansasii" runs are other complex species (this is why we re-classify them).
- **Library strategy matters.** `WGS` (genome), `AMPLICON` and `RNA-Seq` runs can sit in the same BioProject.

The lab's own numbers (`Mkan329-NNN`, TNR) play the role of a local BioSample. They only become public if the data are submitted
and receive `SAMN` / `SRR` numbers; until then there is no public number to match.

Other numbering used in the project:

- `NR 128` / `132` / `133`: lab control strains (ATCC 12478, DSM 104278, DSM 107152) sequenced with the cohort.
- Sanger: `<TNR> hsp65_Tb-11.ab1`, one trace per primer and sample, `_wdh` / `_12w` = repeat or re-run (see
  `sanger-microsynth/species_panel.md`). A Sanger trace is not an NGS run, and one isolate can have several traces.
- Ridom/cgMLST tables use `GCF_…` for public genomes and `M<number>` for lab isolates in the same column.

## 7. Same or not? Quick reference

| Pair of numbers | Same thing? |
|---|---|
| `ATCC 12478` and `DSM 44162` / `CIP 104589` / `NCTC 13024` | same strain (type strain), different collection |
| `ATCC 12478` and `GCF_000157895.3` | strain vs. a genome of it; the genome is a **copy** of that strain, not the strain |
| `GCA_002705925.1` and `GCF_002705925.1` | same assembly, GenBank vs RefSeq (annotation differs) |
| `GCF_000157895.3` and `GCF_000157895.2` | same submission, different version, sequence or annotation may differ |
| `RS_GCF_…` and `GCF_…` | same, GTDB prefix only |
| `GCF_002705925.1` and `GCF_021183725.1` | both *M. ostraviense*, different strains, different samples |
| `SAMN…` and `SRS…` | same sample, different database record |
| `SRX…` and `SRR…` | experiment contains the run; one experiment can have several runs |
| `SRR…` (run) and `GCA_…` (assembly) | different objects; no automatic link |
| `PRJNA…` and `SAMN…` | study vs sample; one project has many samples |
| `Mkan329-181` and `2022500313` | same isolate in this project, different lab registries |
| `2022500313` (TNR) and `2023187867` (NGS) | same isolate, different registration events (culture/Sanger vs NGS) |
| `Mkan329-181` and strain `241/15` | **different**: clinical isolate vs. type strain, same species |
| GTDB species name and NCBI organism name | usually the same, sometimes different; GTDB release matters |
| MetaPhlAn SGB and GTDB species | different clustering; names may disagree |
| NCBI "type material" and GTDB "type strain" | can disagree for the same genome (ostraviense 241/15 in r232) |

## 8. Practice for this project

1. Store the full accession **with version** (`GCF_002705925.1`), and the GTDB release next to any species name.
2. Keep one mapping table from isolate ID to every lab number and public accession (`screening_map_link.csv`) and extend that rather than
   renaming files.
3. Compare identifiers only within the same object type (section 1). Convert strain to genome through the BioSample, genome to
   reads through the BioSample or BioProject, never by name.
4. Count isolates with BioSamples, not runs; count genomes with assemblies, not contigs.
5. If a name or number "does not match", first ask which object type each one is, then whether a version or database release differs,
   and only then suspect a real discrepancy.
