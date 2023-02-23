# BowBin

## Tools
`conda config --add channels bioconda`

`conda create -n BowBin cutadapt`

`conda install -c bioconda fastqc`

`conda install trim-galore`

**SRA Toolkit:** [https://github.com/ncbi/sra-tools](https://github.com/ncbi/sra-tools)

`conda install -c bioconda cd-hit`
`conda install -c bioconda seqtk`

## Commands
1. Download file fastq: `fasterq-dump ERR5084065 --split-files --skip-technical`
2. Adapter removal and read quality trimming: `trim_galore --paired fileR1.fastq fileR2.fastq`
