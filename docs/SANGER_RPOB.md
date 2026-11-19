# rpoB regions in the routine Sanger file names

Which rpoB region a routine Sanger read covers, and how a parser tells them apart from the file name alone. Most important:
**NTM species identification (rpoB-2573f/3337r)** vs. **Mtb rifampicin resistance (RRDR, TR1/TR2b)**.
Source: `data/sanger/seq_mol_routine/` (all subfolders), state 2026-11-19.
Rules and tables: `bin/sanger_rpob.py` (regenerate with `python3 bin/sanger_rpob.py`; `--list` prints region, sequence check and
path for every file). Primer sequences: `cosmic-seq/docs/PRIMERS.md`; lab numbers: [SANGER_LABNUMBERS.md](SANGER_LABNUMBERS.md).

## Regions

| Region | Purpose | Handbook | Primers | Product (H37Rv) | Tokens in the file name |
|---|---|---|---|---|---|
| **NTM: 2573f/3337r** | species ID of NTM | 32.43504 | rpoB-2573f / rpoB-3337r | 761 bp | `2573f` (also `2573_f`, `2573-f`, `2572f`, `2575f`, `573f`, `258f`), `3337r`, `337r`, `MycoR2`; `rpoBs`, `rpoB-S`, `rpoB-S.`, `rpoBS`, `rpo_BS`; often only `F`/`R` or nothing |
| **Mtb: RRDR 81 bp** | rifampicin resistance | 32.43612 | TR1 / TR2b | 411 bp | `TR1`, `TR2b` (also `TR2`, `TR12b`, `TR26`, `TR1F`, `TR2bR`), `81bp`, `81 bp`, `rpoB81`, `81core`, `mut`, `Mutation`, `rpoBc` |
| Mtb: Xpert region | sequencing of GeneXpert MTB/RIF results | NZM 21 | rpoB-F1, -F2 / rpoB-R, -R2 | 146–192 bp | `rpoB-F1`, `-F2`, `-R2`, `GeneXpert`; a bare `rpoB-R` next to F1/F2 of the same lab number |
| Mtb: 5' region | rifampicin, outside the RRDR | 32.43619 | Tb176-f / Tb176-r | 365 bp | `Tb176_f`, `Tb176-r`, `TB176r` (no "rpoB" in the name) |
| NTM: M. abscessus | rpoB of *M. abscessus* | – | MAB F / R | ~360 bp read | `rpoB_MAB_F`, `_MAB_R` (2015 only) |
| NTM: M. marinum | rpoB of *M. marinum* | "10-rpoB für M. marinum" | RPO F / R | ~330 bp read | `M.marinum_RPO_F`, `_RPO_R` (2015 only) |
| other genus | not mycobacterial | – | rpoB-univ-FW, Strepto F/R, GrpoB1/2 | | `univ`, `Strep`, `Strepto`, `GrpoB` |

The `S` in `rpoBs` / `rpoB-S` marks the NTM species-ID assay ("Spezies"); it never means the RRDR.
"Mtb" names the assay, not the organism: TR1/TR2b is sometimes run on NTM (`M.avium_ATCC_TR1`, tbe lab numbers 500xxx).

## Parser rules

1. **Cut the name down to its marker part.** Remove the extension (`.ab1`, `.seq`, `.fasta`), `_Peaktraced`, the run suffix
   `_YYYY-MM-DD_hh-mm-ss_A01` (before 2009: `_YYYY-MM-DD_NN_A01`) and the leading lab number (10 digits, or older forms such as
   `176104-08`, `2010_500249`). Skip `~$*`, `*.phd.1` and `Thumbs.db`.
2. **Never match digits inside the lab number.** A bare `81` hits `2026338109 rpoB_rpoB-2573f`; match it as `(?<!\d)81(?!\d)`.
   For the same reason `Tb176` must not be followed by a digit (`tb176518_...` is lab number 176518).
3. **Select the files by** `rpo|TR\s?\d|81\s?bp|Tb176(?!\d)`: TR1/TR2b reads are often named without "rpoB"
   (`2023186001_TR1_...`).
4. **First match wins, in this order:**

   | # | Region | Rule on the marker part (case-insensitive) |
   |---|---|---|
   | 1 | other genus | `strep\|univ\|GrpoB` |
   | 2 | NTM: M. abscessus | `MAB` |
   | 3 | NTM: M. marinum | `marinum` |
   | 4 | Mtb: 5' region | `Tb176(?!\d)` |
   | 5 | Mtb: Xpert region | `genexpert\|rpoB-?[FR]\d(?!\d)` |
   | 6 | Mtb: RRDR 81 bp | `(?<!\d)81(?!\d)\|TR\s?\d\|core\|mut\|rpoBc` |
   | 7 | NTM: 2573f/3337r | `25[67][2-5]\|573f\|258f\|3?337r\|myco` |
   | 8 | NTM: no primer in name | anything else (`rpoB`, `rpob`, `rpoBs`, `rpoB_F`, `rpoB_R`, `rpoB_seq`, `10ul`, `wdh` …) |

   The Mtb rules come before the NTM rules because names carry both kinds of token: `rpoB_R_TR2b` and `rpoB 81 r_TR2b` are RRDR,
   not the NTM reverse read.
5. **Default to NTM.** A name without a primer token is the NTM species-ID assay: 334 of the 336 such reads with sequence have
   no Mtb RRDR, and the reads are ~730 bp, as for 2573f/3337r.
6. **Known exceptions:**
   - Bare `rpoB-R` in the August 2018 GeneXpert runs (2018338854, 2018338876, 2018339379) is the Xpert reverse primer. The
     script assigns it to the Xpert region when the same folder holds F1/F2/R2 or GeneXpert files of the same lab number.
   - `1_rpoB_s_MF` / `1_rpoB_s_MR2` (2009-12-17) contain the RRDR although the name says `rpoB_s`. Not covered by a rule.

## Sequence check

The name rules can be checked against the reads: an Mtb RRDR read contains `CACAAGCGCCGACTGTC`, `CTGTCGGCGCTGGGG` or
`CCGCTGTCGGGGTTGAC` (codons ~516–531, either strand). NTM RRDRs differ from these, so a miss is expected when the isolate is
not Mtb. A parser can use this to flag names that disagree with the sequence; it should not override the name.

| Region | Files | ab1 | seq | fasta | Reads with RRDR | Without | Empty (< 100 bp) |
|---|---|---|---|---|---|---|---|
| other genus | 44 | 22 | 17 | 5 | 0 | 20 | 2 |
| NTM: M. abscessus (MAB) | 20 | 10 | 10 | 0 | 0 | 10 | 0 |
| NTM: M. marinum (RPO_F/R) | 6 | 3 | 3 | 0 | 0 | 3 | 0 |
| Mtb: 5' region (Tb176) | 26 | 13 | 11 | 2 | 0 | 13 | 0 |
| Mtb: Xpert region (F1/F2/R2) | 28 | 14 | 14 | 0 | 7 | 7 | 0 |
| Mtb: RRDR 81 bp (TR1/TR2b) | 1130 | 565 | 535 | 30 | 472 | 69 | 24 |
| NTM: 2573f/3337r | 4539 | 2278 | 1826 | 435 | 0 | 2077 | 184 |
| NTM: no primer in name | 730 | 365 | 359 | 6 | 2 | 334 | 29 |

Total: 6,523 rpoB reads. Read checks are on `.seq`/`.fasta` only (`.ab1` is binary).

- **No NTM-named read with a primer token contains the Mtb RRDR** (0 of 2,077); the two bare-name hits are the 2009 `MF`/`MR2` exception.
- **472 of 541 RRDR reads (87%) contain it.** The 69 without: 22 tbe (500xxx, probably NTM isolates), the rest mostly 2010–2012
  repeats (`wdh`) and weak reads.
- Xpert reads are short (~230 bp) and the motifs lie close to their ends, so only half are hit.

## Naming over time

| Years | Pattern | Example |
|---|---|---|
| 2006–2010 | lab number anywhere, many typos | `rpob_177538_3337r_...`, `179342rpob_573f_...`, `rpoBseq_gr_180784_...` |
| 2011–2022 | `YYYY<6 digits>_rpoB[-S\|s]_<primer>_<run date/time>_<well>` | `2016339219_rpoB_2573f_2016-09-22_14-50-52_D07.seq` |
| 2023– | `YYYY<6 digits> rpoB[ note]_<primer>`, primer after the last `_`; subfolders `Kultur/`, `Kulturen/`, `NZM/` | `2025500747 rpoB_rpoB-2573f.ab1`, `2025342747 rpoB 81 r_TR2b.fasta` |

Files per year and region (`python3 bin/sanger_rpob.py`):

| Year | other genus | MAB | marinum | Tb176 | Xpert | RRDR (TR) | NTM 2573f/3337r | NTM no primer |
|---|---|---|---|---|---|---|---|---|
| 2006 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 |
| 2007 | 0 | 0 | 0 | 0 | 0 | 0 | 24 | 42 |
| 2008 | 0 | 0 | 0 | 0 | 0 | 0 | 76 | 88 |
| 2009 | 0 | 0 | 0 | 0 | 0 | 22 | 156 | 38 |
| 2010 | 0 | 0 | 0 | 0 | 0 | 44 | 122 | 54 |
| 2011 | 28 | 0 | 0 | 0 | 0 | 150 | 276 | 38 |
| 2012 | 6 | 0 | 0 | 0 | 0 | 96 | 252 | 34 |
| 2013 | 0 | 0 | 0 | 4 | 0 | 130 | 220 | 4 |
| 2014 | 0 | 0 | 0 | 0 | 0 | 128 | 396 | 14 |
| 2015 | 0 | 20 | 6 | 10 | 0 | 224 | 404 | 24 |
| 2016 | 0 | 0 | 0 | 0 | 0 | 78 | 420 | 26 |
| 2017 | 0 | 0 | 0 | 0 | 0 | 44 | 310 | 8 |
| 2018 | 0 | 0 | 0 | 4 | 28 | 32 | 220 | 10 |
| 2019 | 0 | 0 | 0 | 0 | 0 | 70 | 208 | 60 |
| 2020 | 0 | 0 | 0 | 0 | 0 | 8 | 204 | 92 |
| 2021 | 0 | 0 | 0 | 0 | 0 | 20 | 204 | 78 |
| 2022 | 0 | 0 | 0 | 4 | 0 | 20 | 146 | 80 |
| 2023 | 10 | 0 | 0 | 0 | 0 | 12 | 166 | 27 |
| 2024 | 0 | 0 | 0 | 4 | 0 | 32 | 257 | 12 |
| 2025 | 0 | 0 | 0 | 0 | 0 | 4 | 296 | 0 |
| 2026 | 0 | 0 | 0 | 0 | 0 | 16 | 182 | 0 |

Year = run date in the file name, else the year folder.
