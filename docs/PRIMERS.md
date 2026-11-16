# Primers: what the Sanger reads used vs. what the lab protocols document

Checked 2026-11-16 against the 13 files in `data/protocols/`.

**Conclusion:** every primer used for the kansasii Sanger reads has its sequence written in a lab protocol.
Chapter 32.43304 gives the sequences of Mbak14 and Mbak259r, chapter 32.43325 those of IMM F and IMM R2.

## Primers used for the kansasii reads

Counts are the 680 `.ab1` files in `data/sanger/seq_kansasii`, assigned by the primer named in the file name.
Positions are on the *M. tuberculosis* H37Rv 16S rDNA (1537 bp) printed in 32.43303; every 16S primer matches
that sequence exactly. Primers of other targets have no position ("–").

| Primer | Target | Reads | Sequence 5'→3' | H37Rv 16S position | Protocol |
|---|---|---|---|---|---|
| TB-11 | hsp65, forward | 212 | ACCAACGATGGTGTGTCCAT | – | 32.43505 |
| TB-12w | hsp65, reverse (routine) | 99 | CTTGTCGAASCGCATACCCT | – | 32.43505 |
| TB-12 | hsp65, reverse (fallback) | 40 | CTTGTCGAACCGCATACCCT | – | 32.43505 |
| Mbak14 | 16S, sequencing primer | 75 named + 169 label only | GRGRTACTCGAGTGGCGAAC | 86–105, forward | 32.43304 |
| Mbak259r | 16S, reamplification and repeat sequencing | 10 | TTTCACGAACAACGCGACAA | 581–600, reverse | 32.43304 |
| Mbak264r | 16S, amplification | 4 | TGCACACAGGCCACAAGGGA | 1018–1037, reverse | 32.43522, 32.43304 |
| Mbak283f | 16S, amplification | 2 | GAGTTTGATCCTGGCTCAGGA | 12–32, forward | 32.43522, 32.43304 |
| rpoB-2573f / rpoB-3337r | rpoB | 5 | GGCAAGGTCACCCCGAAGGG / AGCGGCTGCTGGGTGATCATC | – | 32.43504 |
| Bact-1098s / Bact-1525a | 16S 3' end | 4 | CGCAACGAGCGCAACCC / AAGGAGGTGATCCARCC | 1089–1105, forward / 1518–1534, reverse | 32.43506 |
| 16-23S-ITS-1f / -2r | 16S-23S spacer | 2 | ACCTCCTTTCTAAGGAGCACC / GATGCTCGCAACCACTATCCA | – | 32.43606 |
| IMM F | 16S, amplification (direct detection assay) | 2 | TTAACACATGCAAGTCGAACGGAA | 51–74, forward | 32.43325 |

How the counts were made:

- Bare `11`, `12w` and `12` in hsp65 file names are counted as TB-11, TB-12w and TB-12 (103, 73 and 27 reads).
  The typo `tbii` (3 reads) is counted as TB-11.
- 169 16S reads carry only a label (`LC<n>`, `MTB`, `K`) and no primer name. They are assumed to be Mbak14,
  because 32.43103 and 32.43110 name it as the standard sequencing primer. The file names do not confirm this.
- Not in the table: 20 hsp65 reads that name both primers or none, 29 reads with only a `ct<n>` label, and 7
  reads whose names could not be assigned.

## 16S amplicons

Lengths on H37Rv, from the positions above:

| Primer pair | Protocol | Product | Length |
|---|---|---|---|
| IMM F + IMM R2 | 32.43325 (direct detection, LC480) | 51–616 | 566 bp |
| Mbak283f + Mbak264r | 32.43304 protocol 3, 32.43522 | 12–1037 | 1026 bp |
| Mbak283f + Mbak259r | 32.43304 protocol 4 (reamplification) | 12–600 | 589 bp |

All three products contain the Mbak14 site (86–105), so each can be sequenced with Mbak14. IMM R2 overlaps
Mbak259r by 11 nt (590–600).

## Other oligos in the protocols

- IMM R2, reverse primer of the direct detection assay (32.43325): `CAGTTAAGCCGTGAGATTTCACGAACA`, position
  590–616, reverse. No kansasii read is named after it.
- Probes of both LC480 assays (32.43522 and 32.43325, identical sequences): MTBs
  `FAM-AAAGCGCTTTAGCGGTGTGG-BHQ1` (206–225, forward), Gui610 `LC610-CGACAAACCACCTACGAGCTCTTTACGC-BBQ`
  (559–586, reverse).
- Drawn on the H37Rv 16S position map (32.43303) without a written sequence in any protocol: Mbak TB-705,
  Mbak TB-F, Mbak GE-F, Mbak GE-640. The positions drawn for Mbak14, Mbak259, Mbak264r, Mbak283f, IMM F,
  IMM R2, MTBs and Gui610 agree with the written sequences.

## Which protocol says what

| Protocol | Content relevant to primers |
|---|---|
| 32.43505 | hsp65 (65 kDa) sequencing: TB-11, TB-12w, TB-12 |
| 32.43304 | Genus amplification: protocol 3 = Mbak283f + Mbak264r, protocol 4 (reamplification) = Mbak283f + Mbak259r, sequencing with Mbak14, possibly Mbak259r |
| 32.43325 | LC480 direct detection from clinical material: IMM F, IMM R2, probes MTBs and Gui610; positive genus products are sequenced according to 32.43103 |
| 32.43522 | LC480 culture differentiation: Mbak283f, Mbak264r, probes MTBs and Gui610 |
| 32.43303 | Position map of primers and probes on the H37Rv 16S rDNA |
| 32.43103, 32.43110 | Algorithms; name the primers only |
| 32.43504 | rpoB sequencing |
| 32.43506 | 16S 3' end |
| 32.43606 | 16S-23S ITS (*M. fortuitum* group) |
| 32.46026 | ExoSAP clean-up and Microsynth ordering; no primer sequences |

## Use in the code

- Only TB-11, TB-12w and TB-12 are used as sequences, for the in-silico hsp65 PCR. `mlsa-kansasii/mlsa/protocols.py`
  parses them from 32.43505 and has the same values as fallback constants; `hsp65-refalign/hsp65_refalign/insilico.py`
  holds them as constants (see [VENDORED.md](VENDORED.md)). All are identical to the protocol.
- The 16S primers are used only as file-name patterns to recognise 16S reads (`mlsa/sanger_io.py`: Mbak14,
  Mbak259r, Mbak264r). No analysis depends on their sequences.
- `mlsa/sanger_io.py` has no pattern for IMM F, so the 2 reads named `IMMF` are not classified as 16S.
