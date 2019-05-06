#!/usr/bin/env python3
import sys, os, subprocess
import pandas as pd
import numpy as np
import io, gzip
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-i', help='the sequencing summary file')
parser.add_argument('-q', help='sequencing reads in fastq')
parser.add_argument('-o', help='an output folder')
parser.add_argument('-g', help='genome size')
parser.add_argument('-d', help='sequencing depth')
parser.add_argument('-qmin', help='minimum quality valure (default 7)')
parser.add_argument('-lmin', help='minimum sequence length (default 0 bp)')
args = parser.parse_args()

outdir='./'
genomesize=3000000
depth=40
mintotal=120000000

Lcutvalue=0
Qcutvalue=7

argv=sys.argv
if '-i' in argv:
    indexfile=argv[argv.index('-i')+1]
if '-q' in argv:
    fqfile=argv[argv.index('-q')+1]
if '-o' in argv:
    outdir=argv[argv.index('-o')+1]
if '-t' in argv:
    mintotal=int(argv[argv.index('-t')+1])
if '-g' in argv:
    temp=argv[argv.index('-g')+1]
    if 'm' in temp or 'k' in temp or 'M' in temp or 'K' in temp:
        if 'm' in temp or 'M' in temp:
            temp1=temp.replace('m','')
            genomesize=int(temp1.replace('M',''))*1000000
        if 'k' in temp or 'K' in temp:
            temp1=temp.replace('k','')
            genomesize=int(temp1.replace('K',''))*1000
    else:
        genomesize=int(temp)
if '-d' in argv:
    depth=int(argv[argv.index('-d')+1])
if '-qmin' in argv:
    Qcutvalue=float(argv[argv.index('-qmin')+1])
if '-lmin' in argv:
    Lcutvalue=int(argv[argv.index('-lmin')+1])

if '-g' in argv or '-d' in argv:
    mintotal=genomesize*depth


cwd=os.getcwd()
df=pd.read_table(indexfile)
df=df.drop_duplicates('read_id')
df=df[df['mean_qscore_template']>7]

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

if not os.path.exists(outdir):
    os.mkdir(outdir)
os.chdir(outdir)



#Default to get high-quality
if '-ll' not in argv:
    dfset=df[df['sequence_length_template']>=Lcutvalue]  #Only consider reads with mininmun length at Lcutvalue
    #To sort by quality
    dfset=dfset.sort_values(['mean_qscore_template'], ascending=False)
    print ('  Get high-quality reads...')

else:
    dfset=df[df['mean_qscore_template']>=Qcutvalue]  #Only consider reads with mininmun quality at Qcutvalue
    #To sort by length
    dfset=dfset.sort_values(['sequence_length_template'], ascending=False)
    print ('  Get long-length reads...')

sumbasesL=dfset['sequence_length_template'].cumsum()
lineidx=0
for i in sumbasesL.index:
    lineidx+=1
    total=int(sumbasesL.ix[i])
    if total > mintotal:
        tempi=i
        break

setdf=dfset.iloc[0:lineidx,:]
#print (setdf)
outindex=indexfile.replace('.txt','_filtered.txt')
setdf.to_csv(outindex,sep='\t')
comm='mv {0} ./'.format(outindex)
subprocess.getoutput(comm)

print ('  Get long read: {:,} bases'.format(total))

fw=open('reads.fastq','w')
for ID in setdf['read_id']:
    if ID in d:
        fw.write(d[ID][0]+'\n')
        fw.write(d[ID][1]+'\n')
        fw.write('+'+'\n')
        fw.write(d[ID][2]+'\n')
    else:
        print (ID)
fw.close()

os.chdir (cwd)
