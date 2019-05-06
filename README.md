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
