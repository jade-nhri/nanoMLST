# nanoMLST
Accurate multilocus sequence typing using Oxford Nanopore MinION with dual-barcode approach to multiplex large numbers of samples

**To run with Docker**

``git clone https://github.com/jade-nhri/nanoMLST.git``

``cd nanoMLST``

``docker build -t "nanomlst:v1" ./``

``docker run -h nanomlst --name nanomlst -t -i -v /:/MyData nanomlst:v1 /bin/bash``

Installation
------------
**Installation from source**

``cd /opt``

``git clone https://github.com/jade-nhri/nanoMLST.git``

``cd nanoMLST/nanoMLST``

``chmod +x *.py``

``export PATH="$PATH:/opt/nanoMLST/nanoMLST/"``

## Dependencies

- [Albacore 2.3.1]
- [samtools 1.7](http://www.htslib.org/)
- [racon v1.3.1](https://github.com/isovic/racon)
- [minimap 2.11](https://github.com/lh3/minimap2)
- [nanopolish v0.10.2](https://github.com/jts/nanopolish)



 > Before installing these dependencies it may be required to install some
 > prerequisite libraries, best installed by a package manager. On Ubuntu
 > theses are:
 > * cmake
 > * liblzma-dev
 > * libbz2-dev
 > * libz-dev
 > * libncurses-dev
 > * make
 > * wget
 > * python3-all-dev
 > * parallel
 > * pandas
 > * pyfastaq

## Usage
To run Albacore:
``read_fast5_basecaller.py -f FLO-MIN106 -k SQK-LSK109 -t 100 -i fast5/ -r -s albacore2.3.1 -o fastq``
``cd albacore2.3.1/workspace/pass``
``cat fastq_runid*.fastq > all.fastq``

To run nanoMLST:
``getfastq.py -i sequencing_summary.txt -q all.fastq -o HQ10_1000_1m -g 1m -d 1000 -qmin 10 -lmin 1000``

``cd HQ10_1000_1m/``

``minimap2 ../dualbcs.fa reads.fastq -k7 -A1 -m42 -w1 > out.paf``

``getbcfq.py -m out.paf -i reads.fastq -o outfq > log_bin_fq``

``binf5.py -i outfq/ -o binf5 -ss sequencing_summary_filtered.txt -f5 ../fast5/ -t 100``

``runcons.py outfq/ binf5/ -t 100``

``mkdir mlst``

``cd mlst``

``runtyping.py ../outfq/ mlst_HQ10_1000_1m_list.txt > log_mlst_HQ10_1000_1m_list``

