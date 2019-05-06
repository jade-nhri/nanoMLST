# nanoMLST
Accurate multilocus sequence typing using Oxford Nanopore MinION with dual-barcode approach to multiplex large numbers of samples

**To run with Docker**

``git clone https://github.com/jade-nhri/nanoMLST.git``

``cd nanoMLST``

``docker build -t "nanomlst:v1" ./``

``docker run -h nanomlst --name nanomlst -t -i -v /:/MyData nanomlst:v1 /bin/bash``
