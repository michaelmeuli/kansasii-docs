# Shell twin of templates/kansasii_paths.py: the same names for the same paths. Source it, do not execute it:
#   source "${KANSASII_ROOT:-/shares/sander.imm.uzh/MM/kansasii}/repos/kansasii-docs/templates/kansasii_paths.sh"
# Override the root with KANSASII_ROOT. Scripts read from DATA and RUNS; OUTPUT_ROOT receives results.
# (#SBATCH --output lines cannot expand variables: they keep the literal path output/<name>/logs/.)
ROOT=${KANSASII_ROOT:-/shares/sander.imm.uzh/MM/kansasii}
REPOS=$ROOT/repos
DATA=$ROOT/data
RUNS=$ROOT/runs
OUTPUT_ROOT=$ROOT/output
# One directory per repo below OUTPUT_ROOT, named exactly like the repo (results/, logs/, MANIFEST.txt inside).
OUT_AMR=$OUTPUT_ROOT/kansasii-amr-marker-screen
OUT_CGMLST=$OUTPUT_ROOT/kansasii-cgmlst
OUT_DOCS=$OUTPUT_ROOT/kansasii-docs
OUT_GWAS=$OUTPUT_ROOT/kansasii-gwas
OUT_MIC=$OUTPUT_ROOT/kansasii-mic
OUT_MST=$OUTPUT_ROOT/kansasii-mst
OUT_MLSA=$OUTPUT_ROOT/mlsa-kansasii
OUT_GYRA=$OUTPUT_ROOT/gyrA-refalign
OUT_HSP65=$OUTPUT_ROOT/hsp65-refalign
OUT_IMM=$OUTPUT_ROOT/immensekansasii
OUT_MICROSYNTH=$OUTPUT_ROOT/sanger-microsynth
MANIFEST_SCRIPT=$REPOS/kansasii-docs/bin/write_manifest.sh

GTDB_DIR=$DATA/gtdb_genomes/Mycobacteriaceae
NCBI_DATASET=$GTDB_DIR/ncbi_dataset/data
GTDB_REPRESENTATIVES=$GTDB_DIR/kansasii_complex_gtdb_representatives
GTDB_COMPLEX_GENOMES=$GTDB_DIR/mlsa-kansasii
HSP65_AMPLICONS=$GTDB_DIR/kansasii_complex_hsp65_amplicons
GYRA_REFERENCES=$GTDB_DIR/kansasii_complex_gyrA
GTDB_RELEASE=232
GTDB_METADATA_DIR=$DATA/immensekansasii/gtdb/gtdb$GTDB_RELEASE
GTDB_ACCESSIONS_DIR=$OUT_IMM/gtdb/gtdb$GTDB_RELEASE
ATCC12478_ACCESSION=GCF_000157895.3
ATCC12478_DIR=$NCBI_DATASET/$ATCC12478_ACCESSION
ATCC12478_FASTA=$ATCC12478_DIR/${ATCC12478_ACCESSION}_ASM15789v2_genomic.fna
ATCC12478_GFF=$ATCC12478_DIR/genomic.gff

IMM_DIR=$DATA/imm
MIC_CSV=$IMM_DIR/mic.csv
SCREENING_MAP_LINK=$IMM_DIR/screening_map_link.csv
SCREENING_MAP_RESULTS=$IMM_DIR/screening_map_results.csv
SCREENING_MAP_AST_JC=$IMM_DIR/screening_map_ast_jc.csv
SANGER_LINK_DIR=$DATA/sanger/seq_kansasii
ILLUMINA_DIR=$DATA/illumina
PUBLIC_READS=$ILLUMINA_DIR/public

ASSEMBLIES=$RUNS/mkan329/assembly/results
PUBLIC_PROJECTS=(PRJNA1078897 PRJNA1048499 PRJNA845115 PRJNA323639)
public_assemblies () { echo "$RUNS/public_$1/assembly/results"; }

# External software that is not part of the project (pipeline databases, container cache).
IMMENSE_DEPENDENCIES=/shares/sander.imm.uzh/software/pipelines/IMMense/IMMense_dependencies
IMMENSE_DB_ROOT=$IMMENSE_DEPENDENCIES/databases/kansasii_complex   # snippy databases per run
IMMENSE_CONTAINERS=$IMMENSE_DEPENDENCIES/containers
