# References for the AMR marker screen

Sources of every sequence and every literature marker used by `kansasii-amr-marker-screen`, so that each can be checked.
Bibliography: [references.bib](references.bib) (BibTeX, one entry per cited paper; import into Zotero with *File > Import*). Citekeys below are the BibTeX keys.
Sequence checks: `bash repos/kansasii-amr-marker-screen/scripts/verify_refs.sh` (re-fetches from NCBI, compares; last run 2026-10-29, ALL PASS).

## A. Sequences

### A1. Genome the targets are taken from

*M. kansasii* ATCC 12478, RefSeq GCF_000157895.3 (ASM15789v2), chromosome NC_022663.1. Genome paper: `wang2015insights`. Coordinates are resolved from the RefSeq GFF by `scripts/02_make_targets.py` (`output/kansasii-amr-marker-screen/results/assembly/work/targets.resolved.tsv`); `verify_refs.sh` checks locus tag and coordinates against the GFF.

| Gene | Locus tag | Start-end (strand) | Length bp | Numbering reference |
|---|---|---|---|---|
| rpoB | MKAN_RS18590 | 4266307-4269828 (+) | 3522 | MTB_RPOB_PROT |
| rrl | MKAN_RS06030 | 1411557-1414663 (-) | 3107 | ECOLI_23S_NT |
| rrs | MKAN_RS06035 | 1414940-1416470 (-) | 1531 | ECOLI_16S_NT |
| gyrA | MKAN_RS14160 | 3247943-3251716 (+) | 3774 | MAV_GYRA_PROT |
| gyrB | MKAN_RS14150 | 3244876-3246903 (+) | 2028 | MTB_GYRB_PROT |
| rplC | MKAN_RS18755 | 4304285-4304938 (+) | 654 | MTB_RPLC_PROT |
| rplD | MKAN_RS18760 | 4304938-4305615 (+) | 678 | MTB_RPLD_PROT |
| rpsL | MKAN_RS18645 | 4281907-4282281 (+) | 375 | MTB_RPSL_PROT |
| gid | MKAN_RS14110 | 3235545-3236291 (-) | 747 | MTB_GIDB_PROT |
| tap | MKAN_RS06465 | 1513979-1515235 (+) | 1257 | NONE |
| folP_c1 | MKAN_RS06725 | 1572427-1573323 (-) | 897 | NONE |
| folP_c2 (copy 2) | MKAN_RS11850 | 2747005-2747847 (-) | 843 | NONE |
| folC | MKAN_RS05145 | 1207118-1208560 (-) | 1443 | NONE |
| dfrA | MKAN_RS23945 | 5533621-5534106 (+) | 486 | NONE |
| thyA | MKAN_RS23940 | 5532824-5533624 (+) | 801 | NONE |
| nucS | MKAN_RS06000 | 1404711-1405382 (-) | 672 | NONE |

Not found in the ATCC 12478 GFF: whiB7, eis (`output/kansasii-amr-marker-screen/results/assembly/work/targets.missing.txt`). `erm` is looked for by homology only.

### A2. Numbering references (external sequences)

Published markers use *E. coli* rRNA or *M. tuberculosis* / *M. avium* protein numbering; the pipeline transfers them by alignment. Files are in `output/kansasii-amr-marker-screen/results/assembly/refs/`, listed in `config/seq_refs.tsv`.

| File | Accession | Organism | Length | sha256 (first 16, of sequence) | Numbers |
|---|---|---|---|---|---|
| ECOLI_16S_NT.fa | [J01695.2:1268-2809](https://www.ncbi.nlm.nih.gov/nuccore/J01695.2) | Escherichia coli K-12 rrnB (16S rRNA) | 1542 | 1f8ffcf20451bf64 | rrs |
| ECOLI_23S_NT.fa | [V00331.1](https://www.ncbi.nlm.nih.gov/nuccore/V00331.1) | Escherichia coli rrnB (23S rRNA) | 2904 | 8f67dcfd2237a8f4 | rrl |
| MTB_RPOB_PROT.fa | [NP_215181.1](https://www.ncbi.nlm.nih.gov/protein/NP_215181.1) | Mycobacterium tuberculosis H37Rv Rv0667 | 1172 | 29d096475f13a12f | rpoB |
| MTB_GYRB_PROT.fa | [NP_214519.2](https://www.ncbi.nlm.nih.gov/protein/NP_214519.2) | Mycobacterium tuberculosis H37Rv Rv0005 | 675 | 7c91220cb6f6e14d | gyrB |
| MTB_RPSL_PROT.fa | [NP_215196.1](https://www.ncbi.nlm.nih.gov/protein/NP_215196.1) | Mycobacterium tuberculosis H37Rv Rv0682 | 124 | e5d2cb63c540d8f1 | rpsL |
| MTB_GIDB_PROT.fa | [NP_218436.1](https://www.ncbi.nlm.nih.gov/protein/NP_218436.1) | Mycobacterium tuberculosis H37Rv Rv3919c | 224 | 4427073e0ff6dbe4 | gid |
| MTB_RPLC_PROT.fa | [NP_215215.1](https://www.ncbi.nlm.nih.gov/protein/NP_215215.1) | Mycobacterium tuberculosis H37Rv Rv0701 | 217 | 94fd82b3de4fb476 | rplC |
| MTB_RPLD_PROT.fa | [NP_215216.1](https://www.ncbi.nlm.nih.gov/protein/NP_215216.1) | Mycobacterium tuberculosis H37Rv Rv0702 | 223 | edcfee6467e0041e | rplD |
| MAV_GYRA_PROT.fa | [WP_011723278.1](https://www.ncbi.nlm.nih.gov/protein/WP_011723278.1) | Mycobacterium avium complex (MULTISPECIES) | 839 | d9be43bf383f147f | gyrA |

Caveats: `J01695.2:1268-2809` is the 16S feature cut out of the whole rrnB operon (7258 bp), so position 1 = *E. coli* 16S nt 1. `WP_011723278.1` is a non-redundant RefSeq protein shared by several MAC strains (MULTISPECIES), not one genome; it is used only for GyrA codon numbering (D95, A91).

### A3. Other species of the complex

Genomes are GTDB representatives (`$GTDB_REPRESENTATIVES/<accession>_query.fasta`), used by `03b_species_refs.sh` to show whether a variant is species-specific. *kansasii* is the ATCC 12478 record above.

| Species | Accession |
|---|---|
| persicum | [GCF_002086675.1](https://www.ncbi.nlm.nih.gov/datasets/genome/GCF_002086675.1/) |
| pseudokansasii | [GCF_900566075.1](https://www.ncbi.nlm.nih.gov/datasets/genome/GCF_900566075.1/) |
| innocens | [GCF_900566055.1](https://www.ncbi.nlm.nih.gov/datasets/genome/GCF_900566055.1/) |
| attenuatum | [GCF_900566085.1](https://www.ncbi.nlm.nih.gov/datasets/genome/GCF_900566085.1/) |
| ostraviense | [GCF_002705925.1](https://www.ncbi.nlm.nih.gov/datasets/genome/GCF_002705925.1/) |
| gastri | [GCF_002102175.1](https://www.ncbi.nlm.nih.gov/datasets/genome/GCF_002102175.1/) |

## B. Literature behind each marker

Generated from `config/markers.tsv` (`citekey` is derived from the DOI column, or the PMID in `notes` when the DOI is NA). "Species" is where the marker was observed; only *M. kansasii* evidence is direct.

| Gene | Marker | Species | Evidence | Citekey |
|---|---|---|---|---|
| rpoB | S450L_Mtb / S531L_Ecoli | M. kansasii | VALIDATED | `zhang2023drug` |
| rpoB | codon 531 (E. coli) | M. kansasii | VALIDATED | `klein2001rifampin` |
| rpoB | codon 526 (E. coli) | M. kansasii | VALIDATED | `klein2001rifampin` |
| rpoB | codon 513 (E. coli) | M. kansasii | VALIDATED | `klein2001rifampin` |
| rpoB | codon 516 (E. coli) | M. kansasii | VALIDATED | `yoshida2006detection` |
| rpoB | RRDR scan window | all mycobacteria | REGION | `andre2017consensus` |
| rpoB | RRDR scan window | M. kansasii | VALIDATED | `klein2001rifampin` |
| rrl | A2058G | M. abscessus,MAC,M. chelonae | VALIDATED_OTHER_NTM | `shallom2015real` |
| rrl | A2058C | M. abscessus,MAC | VALIDATED_OTHER_NTM | `shallom2015real` |
| rrl | A2058T | NTM | VALIDATED_OTHER_NTM | `mougari2017genotype` |
| rrl | A2059G | M. abscessus,MAC | VALIDATED_OTHER_NTM | `shallom2015real` |
| rrl | A2059C | NTM | VALIDATED_OTHER_NTM | `mougari2017genotype` |
| rrl | A2057C | NTM | VALIDATED_OTHER_NTM | `mougari2017genotype` |
| rrl | A2266C (study coords) | M. kansasii | VALIDATED_N1 | `bakula2018drug` |
| rrl | peptidyl transferase domain V | all | REGION | `mougari2017genotype` |
| rrl | MABC species polymorphisms G2191A,T2221C | M. abscessus | DO_NOT_CALL | `li2018preliminary` |
| rrl | MAC polymorphisms G2140A,G2210C,C2217G,T2238C,T2322C,T2404C,A2406G | MAC | DO_NOT_CALL | `li2018preliminary` |
| erm | erm homolog present/full-length | M. abscessus | VALIDATED_OTHER_SPECIES | `rajagopalan2025luciferase` |
| erm | erm(41) T28C | M. abscessus | VALIDATED_OTHER_SPECIES | `sharma2020real` |
| rrs | A1408G | M. abscessus,MAC,M. chelonae | VALIDATED_OTHER_NTM | `mougari2017genotype` |
| rrs | helix 44 scan window | NTM | REGION | `mougari2017genotype` |
| eis | eis/eis2 present or overexpressed | M. abscessus | VALIDATED_OTHER_SPECIES | `selchow2022apramycin` |
| whiB7 | loss/gain of function; 5' uORF variants | M. abscessus,M. tuberculosis | VALIDATED_OTHER_SPECIES | `poulton2024beyond` |
| rpsL | K43R | M. tuberculosis | VALIDATED_OTHER_SPECIES | `shafipour2022mutations` |
| rpsL | K88R | M. tuberculosis | VALIDATED_OTHER_SPECIES | **none** |
| rrs | 530 loop (positions 903-906) | M. tuberculosis | VALIDATED_OTHER_SPECIES | **none** |
| rrs | A514C | M. tuberculosis | VALIDATED_OTHER_SPECIES | `wang2019roles` |
| rrs | positions 512,513,516 | M. tuberculosis | VALIDATED_OTHER_SPECIES | **none** |
| rrs | 1401/1402 cluster II | M. tuberculosis | VALIDATED_OTHER_SPECIES | **none** |
| rrs | A128G (study coords) | M. kansasii | SUGGESTIVE_N1 | `bakula2018drug` |
| gid | any frameshift / nonsense / truncation | M. tuberculosis | VALIDATED_OTHER_SPECIES | `shafipour2022mutations` |
| gid | E92D | M. tuberculosis | VALIDATED_OTHER_SPECIES | `shafipour2022mutations` |
| gid | R20P | M. tuberculosis | VALIDATED_OTHER_SPECIES | `shafipour2022mutations` |
| gid | A205A (synonymous) | M. tuberculosis | DO_NOT_CALL | **none** |
| whiB7 | loss/gain of function | M. tuberculosis | SCREENED_NEGATIVE | `shafipour2022mutations` |
| gyrA | D95G | M. avium | VALIDATED_OTHER_NTM | `thapa2023characterization` |
| gyrA | D95Y | M. avium | VALIDATED_OTHER_NTM | `thapa2023characterization` |
| gyrA | D95A | M. avium | VALIDATED_OTHER_NTM | `thapa2023characterization` |
| gyrA | A91V | M. avium | VALIDATED_OTHER_NTM | `thapa2023characterization` |
| gyrA | QRDR scan window | all | REGION | `thapa2023characterization` |
| gyrB | codon 389 | M. simiae | SUGGESTIVE | `daneshfar2022drug` |
| gyrB | codon 444 | M. simiae | SUGGESTIVE | `daneshfar2022drug` |
| gyrB | codon 571 | M. simiae | SUGGESTIVE | `daneshfar2022drug` |
| gyrA | MAC GyrA Thr96 / GyrB Thr522 | MAC | DO_NOT_CALL | `yamaba2019moxifloxacin` |
| gyrA | MABC GyrA S83A, GyrB K447R, GyrB S464N | M. abscessus | DO_NOT_CALL | `chen2015detection` |
| gyrA | NO mutation in 17 CIP-R M. kansasii | M. kansasii | NEGATIVE_FINDING | `bakula2018drug` |
| rplC | C154R | M. tuberculosis | VALIDATED_OTHER_SPECIES | `mcneil2017vitro` |
| rplD | R126H | M. tuberculosis | VALIDATED_OTHER_SPECIES | `zong2018vitro` |
| rrl | domain V | M. tuberculosis | VALIDATED_OTHER_SPECIES | `mcneil2017vitro` |
| rplC | no correlation in RGM | rapidly growing mycobacteria | NEGATIVE_FINDING | `wen2021vitro` |
| doxycycline | NO VALIDATED MARKER | M. kansasii | GAP | **none** |
| sulfamethoxazole-trimethoprim | NO VALIDATED MARKER | M. kansasii | GAP | **none** |
| nucS | loss of function | M. abscessus | HYPERMUTATOR | `fressatticardoso2022noncanonical` |

## C. Gaps and points to check

Rows with no literature source in `markers.tsv`:

- rpsL: K88R (streptomycin)
- rrs: 530 loop (positions 903-906) (streptomycin)
- rrs: positions 512,513,516 (streptomycin)
- rrs: 1401/1402 cluster II (streptomycin)
- gid: A205A (synonymous) (streptomycin)
- NA: NO VALIDATED MARKER (doxycycline)
- NA: NO VALIDATED MARKER (sulfamethoxazole-trimethoprim)

### Proposed sources for the unsourced rows (in the `citekey` column of `markers.tsv` with a `proposed:` prefix)

Found by PubMed search 2026-10-29; abstracts read, full texts not. All but the last two rows are *M. tuberculosis*.

| Row | Proposed citekey | What the abstract supports |
|---|---|---|
| rpsL K88R | `hlaing2017mutations`, `khosravi2017frequency` | Lys88Arg (and Lys88Thr) in STR-R isolates; 3 of 32 in the Iranian series |
| gid A205A | `sun2016characterization`, `jagielski2014screening`, `wang2019roles` | E92D (a276c) + A205A (a615g) co-occur and mark the Beijing lineage |
| rrs 512-516 / 903-906 (530 loop and 912 region) | `finken1993molecular`, `cooksey1996characterization`, `shrestha2020molecular` | STR resistance from rrs changes in the 530 pseudoknot and 912 loop; exact positions are not in the abstracts, check the full texts |
| doxycycline GAP | `li2023vitro` | poor in vitro activity of six tetracyclines incl. doxycycline against *M. kansasii*, MIC90 >= 8; supports the 96% resistance, no mechanism |
| SXT GAP | `liu2015role` | folP1/folP2 expression changes SMX/TMP MIC in *M. smegmatis*/Mtb; mechanism only, no *M. kansasii* marker |

No source found for rrs 1401/1402 as a streptomycin marker. Positions 1401/1402 are the usual aminoglycoside/capreomycin positions in *M. tuberculosis* (to be confirmed), so the row label may need rechecking. Likewise 903-906 sits in the 912 region, not the 530 loop that the row name says.

No marker rows at all (genes extracted but not screened): tap, folP (2 copies), folC, dfrA, thyA. Their only link to resistance is the drug name in `config/targets.tsv`.

Points to verify when citing:

- `shafipour2022mutations` is PMID 36209173, so the PMID in the R20P note and the DOI of the rpsL/gid/whiB7 rows are the same paper. It is an *M. tuberculosis* study (15 STR-R isolates), not *M. kansasii*.
- `wang2019roles` (PMID 31934102, A514C) is also *M. tuberculosis*; the marker note says "Hebei series".
- `selchow2022apramycin` (*M. abscessus*) is the source for eis; its title is about apramycin, so confirm the eis statement in the text before quoting.
- `li2018preliminary` was not resolvable through doi.org; its entry is taken from PubMed (PMID 29773092). `yoshida2006detection`, `wang2019roles`, `chen2015detection` have no DOI in this file (PubMed record only).
- The rpoB S450L row cites `zhang2023drug` (a Shanghai study); the notes call it S454L, the *M. kansasii* numbering in that paper.
- Bibliographic fields come from Crossref/PubMed on 2026-10-29 and were not hand-checked beyond title/year against the marker rows.
