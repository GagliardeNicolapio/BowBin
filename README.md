# BowBin

## Tools
`conda config --add channels bioconda`

`conda create -n BowBin cutadapt`

`conda install -c bioconda fastqc`

`conda install trim-galore`

**SRA Toolkit:** [https://github.com/ncbi/sra-tools](https://github.com/ncbi/sra-tools)

`conda install -c bioconda cd-hit`

`conda install -c bioconda seqtk`

`conda install -c bioconda fastq-join`

## Commands
1. Download file fastq: `fasterq-dump ERR5084065 --split-files --skip-technical`
2. Adapter removal and read quality trimming: `trim_galore --paired fileR1.fastq fileR2.fastq`
3. Joins two paired-end reads on the overlapping ends: `fastq-join ERR5084066_1_val_1.fq ERR5084066_2_val_2.fq -o ERR66-join.fq` 
