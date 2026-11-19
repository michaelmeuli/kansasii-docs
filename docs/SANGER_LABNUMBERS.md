# Lab numbers in the routine Sanger file names

How the lab numbers (TNR, see [IDENTIFIERS.md](IDENTIFIERS.md)) at the start of the routine Sanger file names are built, and which number
range belongs to which workstation. Source: `data/sanger/seq_mol_routine/` (all subfolders), state 2026-11-19.
Tables: `bin/sanger_labnumbers.py` (regenerate with `python3 bin/sanger_labnumbers.py`).

## Structure

```
2014 500121 _clr_mclr_21r_2014-08-04_12-04-17_H05.ab1
^^^^ ^^^^^^  ^^^^^^^^^^^^ ^^^^^^^^^^^^^^^^^^^ ^^^
year counter marker/primer run date+time     well
     ^^^ workstation range (first 3 digits of the counter)
```

- **Year** (4 digits) + **counter** (6 digits). The counter starts again every year and rises month by month (checked against the run
  date in the file name). Its first digits mark the workstation.
- Known from the lab: **500 = tbe**, **33x / 34x = tbc**. Everything else below is read from the data and is an inference.
- Before 2011 most files carry a 6-digit number without year (`316446k_2010-...seq`, `126604_sn_5_...seq`).
- The separator is `_` until about 2022, a space later (`2025500258 LC1_Mbak14.fasta`).

Counts: 190,888 files (ab1 94,982, seq 81,067, fasta 12,880, scf 551, rest tgz/dll/docx/zip etc.); 129,543 start with
year + 6 digits; **38,088 unique lab numbers**.

## Number ranges

| Counter range | Workstation | Years | Sequenced lab numbers / year | Most frequent markers |
|---|---|---|---|---|
| 500001–500999 | **tbe** | 2011–2026 | 77 (2011) rising to 572 (2025) | rpoB, pncA, erm41, LC1–LC8 |
| 333000–343999 | **tbc** | 2016–2026 | 410–550 | MTB, LC1–LC4, rpoB, pncA, erm41 |
| 176000–185999 | probably tbc before 2016 | 2011–2015 | 455–690 | CT, LC, rpoB, erm41, inhA, katG |
| 186000–186xxx | separate small counter | 2007–2026 | 3–31 | ethA, pncA, embB, inhA, rrs, tlyA, atpE, rplC |
| 316000–316999, overflow 317xxx | unknown (markers K, P) | 2011–2026 | 1,213 (2014) falling to 92 (2026) | K, P, recA, bak2 |
| 120xxx–131xxx | bacteriology | 2011–2026 | 570–2,230 (all ranges together) | eub (16S), sn0/sn5, ATL, panf, parC, gyrA |
| 670xxx | pncA series | 2014–2016 | 17–82 | pncA, inhA |
| 100xxx, 650xxx | rare | 2013–2026 | < 30 | JAR, H; V25/V100 |

## Findings

- **tbe (500)**: the whole counter is 500001–500999, so at most 999 tbe numbers per year. 2024 reached **500978**, nearly the ceiling;
  2025 reached 500844.
- **tbc (33x/34x)**: not two workstations but one counter from ~333000 to ~343999, i.e. about 10,000 numbers a year of which ~450 are
  sequenced. 2026 is at 339280 (November).
- **176–185 → 333–343 in 2016**: until 2015 the same TB markers (CT, LC, rpoB, erm41) carry numbers 176xxx–185xxx that rise through the
  year like the tbc counter; the range stops in 2016 when 333xxx starts. Probably the earlier tbc range; **to confirm with the lab**.
- **186** is not the end of that range: it stays at 186001–186210 all year (only 186639 in 2016), with its own resistance gene panel.
- **317** is the overflow of 316: it appears only in 2012–2017, the years in which 316 passed 999.
- 316/317 volume fell from > 1,000 (2014–2016) to 92 (2026).

## Unique lab numbers per year

| year | 500 (tbe) | 333–343 (tbc) | 176–185 | 186 | 316/317 | 120–131 | 670 | 100 | 650 | other |
|---|---|---|---|---|---|---|---|---|---|---|
| 2008 | 4 | 0 | 3 | 2 | 1 | 3 | 0 | 0 | 0 | 0 |
| 2009 | 5 | 0 | 4 | 6 | 0 | 0 | 0 | 0 | 0 | 0 |
| 2010 | 2 | 0 | 15 | 6 | 3 | 3 | 0 | 0 | 0 | 3 |
| 2011 | 77 | 0 | 561 | 17 | 673 | 616 | 0 | 0 | 0 | 74 |
| 2012 | 93 | 0 | 455 | 10 | 752 | 604 | 0 | 0 | 0 | 38 |
| 2013 | 119 | 0 | 538 | 20 | 807 | 677 | 0 | 26 | 0 | 38 |
| 2014 | 156 | 1 | 661 | 31 | 1213 | 791 | 17 | 21 | 1 | 8 |
| 2015 | 147 | 0 | 691 | 17 | 1043 | 566 | 68 | 10 | 2 | 15 |
| 2016 | 223 | 441 | 1 | 15 | 1062 | 606 | 82 | 3 | 16 | 12 |
| 2017 | 298 | 456 | 3 | 7 | 663 | 721 | 0 | 1 | 9 | 7 |
| 2018 | 256 | 430 | 0 | 5 | 479 | 626 | 0 | 0 | 11 | 18 |
| 2019 | 258 | 554 | 0 | 8 | 411 | 881 | 0 | 0 | 4 | 9 |
| 2020 | 247 | 430 | 0 | 3 | 434 | 1767 | 0 | 0 | 6 | 20 |
| 2021 | 244 | 468 | 1 | 4 | 299 | 2234 | 0 | 0 | 1 | 19 |
| 2022 | 277 | 414 | 0 | 8 | 321 | 1403 | 0 | 0 | 0 | 8 |
| 2023 | 344 | 474 | 0 | 7 | 218 | 1876 | 0 | 0 | 3 | 15 |
| 2024 | 481 | 449 | 0 | 4 | 174 | 1197 | 0 | 0 | 6 | 16 |
| 2025 | 572 | 477 | 0 | 3 | 136 | 1153 | 0 | 0 | 8 | 8 |
| 2026 | 349 | 288 | 0 | 1 | 92 | 817 | 0 | 0 | 6 | 4 |

2026 is incomplete (state 2026-11-19). Per-year min/max of each counter: output of `bin/sanger_labnumbers.py`.

## Anomalies

- Impossible years: one number each with 2001, 2047 and 2051 (typos); 2005–2007 have a handful of numbers.
- `~$...` files are Office lock files, not traces.
- `2. M. genitalium_M.pneumoniae  Makrolidresistenz_Chinolonresistenz_ROUTINE/` is not mycobacterial work.
