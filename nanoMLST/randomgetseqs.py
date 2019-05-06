#!/usr/bin/env python3
import os, sys
import subprocess
import shutil
import pandas as pd
import numpy as np
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-i', help='the path to the folder containing demultiplexed reads')
parser.add_argument('-o', help='an output folder')
parser.add_argument('-ss', help='the path to sequencing_summary.txt')
parser.add_argument('-n', help='number of reads')
parser.add_argument('-t', help='threads (default=16)')
args = parser.parse_args()
threads=16

argv=sys.argv

if '-t' in argv:
    threads=argv[argv.index('-t')+1]
if '-i' in argv:
    inpath=argv[argv.index('-i')+1]
if '-o' in argv:
    outpath=argv[argv.index('-o')+1]
if '-ss' in argv:
    seq_sum=argv[argv.index('-ss')+1]
if '-n' in argv:
    seqnum=int(argv[argv.index('-n')+1])

inpath=os.path.abspath(inpath)
outpath=os.path.abspath(outpath)
seq_sum=os.path.abspath(seq_sum)

print (inpath)
print (outpath)
print (seq_sum)
print (seqnum)

if not os.path.exists(outpath):
    os.mkdir(outpath)

readID=[]
bcs=[x for x in os.listdir(inpath) if 'BC' in x and 'fq' in x]
for bc in sorted(bcs):
    print (bc)

    f=open(os.path.join(inpath,bc))
    d=dict()
    while True:
        h=f.readline()
        if not h: break
        h=h.replace('\n','')
        #print (h)
        rID=h.split()[0]
        rID=rID.replace('@','')
        #print (rID)
        seq=f.readline().replace('\n','')
        qh=f.readline().replace('\n','')
        qual=f.readline().replace('\n','')
        d[rID]=[]
        d[rID].append(h)
        d[rID].append(seq)
        d[rID].append(qual)
    f.close()
    fw=open(os.path.join(outpath,bc),'w')
    bctxt=bc.replace('.fq','.txt')
    fwtxt=open(os.path.join(outpath,bctxt),'w')
    k=0
    for ID in d.keys():
        if k<seqnum:
            k+=1
            readID.append(ID)
            fw.write(d[ID][0]+'\n')
            fw.write(d[ID][1]+'\n')
            fw.write('+'+'\n')
            fw.write(d[ID][2]+'\n')
            fwtxt.write(ID+'\n')
        if k>=seqnum:
            fw.close()
            fwtxt.close()
            break

df=pd.read_table(seq_sum)
df=df.drop_duplicates('read_id')
df=df[df['mean_qscore_template']>=7]
df1=df.set_index('read_id')
dfset=df1.loc[readID]
print (dfset)
dfset.to_csv(os.path.join(outpath,'sequencing_summary_filtered.txt'),sep='\t')


