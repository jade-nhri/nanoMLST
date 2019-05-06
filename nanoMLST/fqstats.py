#!/usr/bin/env python3

import sys
import numpy as np
import io, gzip
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('reads', help='reads in fastq/fq/fq.gz')
args = parser.parse_args()

infile=sys.argv[1]
slen=[]
d=dict()
if '.gz' in infile:
    print ('Reading file in gz...')
    f=io.TextIOWrapper(gzip.open(infile,'r'))
else:
    f=open(infile)

while True:
    h=f.readline()
    if not h: break
    h=h.replace('\n','')
    rID=h.split()[0]
    rID=rID.replace('@','')
    seq=f.readline().replace('\n','')
    qh=f.readline().replace('\n','')
    qual=f.readline().replace('\n','')
    d[rID]=[]
    d[rID].append(h)
    d[rID].append(seq)
    d[rID].append(qual)
    slen.append(len(seq))
f.close()
print ('Number of reads: {0}'.format(len(slen)))
print ('Total bases: {0} bp'.format(np.sum(slen)))
print ('Mean length: {:0.2f} bp'.format(np.mean(slen)))
print ('Max length:{0} '.format(np.max(slen)))
print ('Min length:{0} '.format(np.min(slen)))
