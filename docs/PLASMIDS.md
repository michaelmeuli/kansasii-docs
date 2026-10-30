# Plasmid exclusion

Plasmid replicons are kept out of the core-genome target sets. State as of 2026-10-29.

## Ridom SeqSphere+ (Target Definer)

`data/imm/ridom-kansasii-plasmids.csv` lists the *M. kansasii* assemblies whose plasmids were excluded by the Ridom Target Definer
(per the project lead; the file itself is an NCBI Genome export and carries no record of that step). Semicolon-delimited, all fields quoted,
22 columns (NCBI Genome columns: Plasmid Accession(s), Strain, Status, Size, Scaffolds, Genes, Assembly, Replicons, ...).

| Plasmid accession(s) | Strain | Status | Assembly | Size (Mb) | Scaffolds |
|---|---|---|---|---|---|
| NC_022654.1 (pMK12478) | ATCC 12478 | CompleteGenome | GCA_000157895.2 | 6.58 | 2 |
| NZ_CP089219.1 | FDAARGOS_1614 | CompleteGenome | GCA_021183705.1 | 6.45 | 2 |
| NZ_CP089217.1 | FDAARGOS_1615 | CompleteGenome | GCA_021183685.1 | 6.46 | 2 |
| NZ_CP084365.1, NZ_CP084366.1 | FDAARGOS_1534 | Chromosome | GCA_020341475.1 | 6.70 | 3 |
| NZ_CP089232.1 | FDAARGOS_1616 | Chromosome | GCA_021183865.1 | 6.62 | 2 |

Check (2026-10-29): the 305 locus tags on NC_022654.1 in the ATCC 12478 `genomic.gff` have **no overlap** with the 1,406 `MKAN_RS` target
columns of `data/imm/ridom-comparison-table-mkan329.csv`. The four FDAARGOS plasmids have no local sequence, so they were not checked.

## kansasii-cgmlst (chewBBACA)

- Step 00 (`scripts/00_prepare_inputs.py`) calls `strip_plasmids()` (`scripts/common.py`: drops contigs whose FASTA header contains "plasmid")
  on the **7 GTDB reference genomes only**. In practice that removes pMK12478 (NC_022654.1); it is the only labelled plasmid among them.
- The 175 cohort assemblies are linked as they are, **without** plasmid stripping.
- The 117 kb contig `NZ_UPHU01000002.1` of the pseudokansasii reference MK142 (GCF_900566075.1) is unlabelled and kept on purpose.
- Check (2026-10-29): none of the 3,646 loci in `output/kansasii-cgmlst/results/cgmlst/t0.95/cgMLSTschema95.txt` lies on `NZ_UPHU01000002.1` (106 CDS in the
  schema coordinates) or on NC_022654.1. Core loci come from 7 references: 2,134 from ATCC 12478, the rest from the other six.
- The FDAARGOS plasmids in the CSV are not part of the cgMLST inputs (only ATCC 12478, as reference GCF_000157895.3, is in
  `output/kansasii-cgmlst/results/samples.tsv`; the four FDAARGOS assemblies are not).
