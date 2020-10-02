# Quality Assurance and Quality Control Pipeline

Quality assurance/quality control tool that also provides basic information about genome assembly quality as well as annotation of contigs using Prokka. Provides basic information regarding antimicrobial resistance determinants detected using the Comprehensive Antimicrobial Resistance Database (CARD) as well as plasmids using Plasmidfinder. Complimentary to usage with (https://github.com/wshropshire/flye_hybrid_assembly_pipeline). 

## Author

[William Shropshire](https://twitter.com/The_Real_Shrops)


## Dependencies

* java (≥ 13.0.2)
* Prokka (≥ 1.14.5)
* BEDtools (≥ 2.29.2)
* perl (≥ 5.28.0)
* bbmap (≥ 38.79)
* seqtk (≥ 1.3)
* snp-sites (≥ 2.5.1)
* snippy (≥ 4.6.0)
* vt 
* abricate (≥ 0.9.8)
* mlst (≥ 2.18.1)
* emboss (≥ 6.6.0)
* ncbi-blast+ (≥ 2.10.0)
* Python (≥ 3.6.0)
* Prodigal (≥ 2.6.3)
* Minimap2 (≥ 2.17-r974)
* bwa (≥ 0.7.17)
* SAMtools (≥ 1.10)
* Parallel (≥ 201807022)
* BCFtools (≥ 1.10.2)
* htslib (≥ 1.10.2)

Versions above have been tested. Older or newer versions may work, but could create conflicts. Suggestion is to create a virtual environment with these dependencies. Many dependencies are included in containerized downloads of other pipelines (e.g. `snippy`).

Make sure that get_fata_stats.pl perl script is in pathway (provided in db).

## Input

Required input are: 
(1) out-directory (**outdir**) 
(2) contigs from genome assembler
(3) ONT long-reads (either gzip or non-compressed files will work)
(4) Interleaved paired-end short-reads (either gzip or non-compressed files will work)
(5) Sample name

Note that you can interleave short-read data using the `bbmap` tool `reformat.sh`. For racon to work properly, make sure there are underscores in lieu of white-space in headers of short-read fastq files by using the `underscore=t` option in `reformat.sh`


## Usage

Usage with Flye assembler:
```
$python3 qa_qc_tool.py -s SampleName -o outDir -t 2 -c assembly.fasta -l longReads.fastq.gz -pe PEIL.fastq.gz 
```

## Output

A number of different qc/qa metrics along with coverage per contig
