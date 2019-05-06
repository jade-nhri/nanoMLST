FROM ubuntu:16.04


RUN apt-get update && apt-get install -y \
    wget dos2unix \
    python3 \
    python3-pip \
    python3-setuptools \
    python3-dev \
    cmake curl git
RUN pip3 install networkx
RUN pip3 install pandas
RUN pip3 install pyfastaq
RUN pip3 install biopython


#samtools 1.7
ADD https://github.com/samtools/samtools/releases/download/1.7/samtools-1.7.tar.bz2 /opt
RUN apt-get update && apt-get install -y \
    libncurses-dev \
    apt-file \
    liblzma-dev \
    libz-dev \
    libbz2-dev \
    vim parallel
WORKDIR /opt
RUN tar -xjf /opt/samtools-1.7.tar.bz2
WORKDIR /opt/samtools-1.7
RUN make && make install
WORKDIR /

#nanopolish latest
RUN apt-get update && apt-get install -y python-pip python-dev python-biopython build-essential python-matplotlib
WORKDIR /opt
RUN git clone --recursive https://github.com/jts/nanopolish.git
WORKDIR /opt/nanopolish
RUN make
WORKDIR /


#Minimap2, miniasm
#2.11-r797

WORKDIR /opt
RUN curl -L https://github.com/lh3/minimap2/releases/download/v2.11/minimap2-2.11_x64-linux.tar.bz2  | tar -jxvf -
RUN mv minimap2-2.*/ minimap2
RUN git clone https://github.com/lh3/miniasm
WORKDIR /opt/miniasm
RUN make
WORKDIR /

#Racon latest

WORKDIR /opt
RUN git clone --recursive https://github.com/isovic/racon.git
WORKDIR /opt/racon
RUN mkdir build
WORKDIR /opt/racon/build
RUN cmake -DCMAKE_BUILD_TYPE=Release .. && make
WORKDIR /


#set path
ENV PATH $PATH:/opt:/opt/nanoMLST/nanoMLST:/opt/nanopolish:/opt/minimap2/:/opt/miniasm:/opt/racon/build/bin