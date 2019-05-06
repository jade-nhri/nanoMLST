#!/usr/bin/env python3
import sys, os, subprocess
import pandas as pd
import numpy as np
import io,gzip
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-m', help='the paf file produced by minimap2')
parser.add_argument('-i', help='the reads in fastq')
parser.add_argument('-o', help='an output folder')
args = parser.parse_args()

argv=sys.argv
if '-m' in argv:
    mappingfile=argv[argv.index('-m')+1]
if '-i' in argv:
    fqfile=argv[argv.index('-i')+1]
if '-o' in argv:
    outdir=argv[argv.index('-o')+1]


mappingfile=os.path.abspath(mappingfile)
fqfile=os.path.abspath(fqfile)

if not os.path.exists(outdir):
    os.mkdir(outdir)
outdir=os.path.abspath(outdir)

#print (mappingfile)
#print (fqfile)
#print (outdir)
cwd=os.getcwd()
cwd=os.path.abspath(cwd)
#print (cwd)

d=dict()
if '.gz' in fqfile:
    print ('Reading fq in gz...')
    f=io.TextIOWrapper(gzip.open(fqfile,'r'))

else:
    f=open(fqfile)


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

#df=pd.read_table(mappingfile)

df=pd.read_table(mappingfile,names=['Qname','Qlen','Qstart','Qend','strand','Tname','Tlen','Tstart','Tend','Nmatch','Alen','MQ1','MQ2','MQ3','MQ4','MQ5','MQ6'])
#print(df)
df=df.drop_duplicates('Qname')
#print(df)
unibarcode = np.unique(df[['Tname']].values)
print (unibarcode)


os.chdir(outdir)
for bc in unibarcode:
    dfset=df[df['Tname']==bc]
    readID=dfset['Qname'].values
    Nseq=len(readID)
    #print ('{0}\t{1}\n'.format(bc,Nseq))
    if Nseq>=300:
        print (bc)
        print (Nseq)
        fw=open(bc+'.fq','w')
        fwi=open(bc+'.txt','w')
        for ID in readID:
            if ID in d.keys():
                fw.write('@'+ID+'\n')
                fw.write(d[ID][1]+'\n')
                fw.write('+'+'\n')
                fw.write(d[ID][2]+'\n')
                fwi.write(ID+'\n')
            else:
                print (ID)
        fw.close()
        fwi.close()
