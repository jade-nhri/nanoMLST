#!/usr/bin/env python3
import os, sys
import subprocess
import shutil
import pandas as pd
import numpy as np
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-i', help='the path to a folder containing demultiplexed fastq')
parser.add_argument('-o', help='an output folder')
parser.add_argument('-ss', help='the path to sequencing_summary.txt')
parser.add_argument('-f5', help='the path to raw fast5')
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
if '-f5' in argv:
    rawf5dir=argv[argv.index('-f5')+1]

inpath=os.path.abspath(inpath)
outpath=os.path.abspath(outpath)
seq_sum=os.path.abspath(seq_sum)
rawf5dir=os.path.abspath(rawf5dir)


print (inpath)
print (outpath)
print (seq_sum)
print (rawf5dir)

if not os.path.exists(outpath):
    os.mkdir(outpath)

cwd=os.getcwd()
cwd=os.path.abspath(cwd)

rs=4000

copiedfiles=set()

if not os.path.exists(outpath+'/filelist.txt'):
    fw=open(outpath+'/filelist.txt','w')
    for dirpath, dirname, files in os.walk(rawf5dir):
        #print (dirpath)
        #print (dirname)
        fileset=set(files)
        copyingset=fileset.difference(copiedfiles)
        #print ('copyingset:'+str(len(copyingset)))
        count=0
        for f5file in copyingset:
            if (f5file.endswith(".fast5")):
                count+=1
                copiedfiles.add(f5file)
                fw.write(os.path.join(dirpath,f5file)+'\n')
    fw.close()

bcs=[x for x in os.listdir(inpath) if 'NB' in x and 'txt' in x]
print (bcs)
df=pd.read_table(seq_sum)
df=df[['filename','read_id']]
fl=pd.read_table(outpath+'/filelist.txt',names=['filepath'])
print (fl)

fl=fl[~fl['filepath'].str.contains("/._")]
print (fl)


fl['filename']=''
def add_filename(row):
    if pd.notnull(row['filepath']):
        row['filename']=os.path.split(row['filepath'])[-1]
    return row

if not os.path.exists(outpath+'/dfoffp'):
    fl=fl.apply(add_filename,axis=1)
    fl.to_csv(outpath+'/dfoffp',index=False,sep='\t')
    print (fl)
else:
    fl=pd.read_table(outpath+'/dfoffp')
    print (fl)

#print (df)
for bc in bcs:
    print (bc)
    readID=pd.read_csv(inpath+'/'+bc,squeeze=True,header=None)
    os.chdir(outpath)
    bcdir=bc.replace('.txt','')
    if not os.path.exists(bcdir):
        os.mkdir(bcdir)
    os.chdir(bcdir)
    comm='rm * -r'
    subprocess.getoutput(comm)

    fw=open('temp.sh','w')
    #print (readID)
    df1=df.set_index('read_id')
    dfset=df1.loc[readID.values]
    dfset1=dfset.set_index('filename')
    print (dfset1)
    df2=dfset1.join(fl.set_index('filename'))
    print (df2)
    f5name=df2['filepath'].values.tolist()
    print (len(f5name)) 
    print (type(f5name))
    
    rc=0
    for path in f5name:
        path=''.join(path)
        #print (ID)
        a=path
        #print (a)
        #comm="grep '/{0}' {1}/filelist.txt".format(ID,outpath)
        #print (comm)
        #a=subprocess.getoutput(comm)
        #print (a)
        rc+=1
        dirn=str(int(rc/rs))
        tmp=rc%rs
        if tmp < rs:
            b='cp {0} {1}/{2}/{3}'.format(a,outpath,bcdir,dirn)
            fw.write('{0}\n'.format(b))
    fw.close()
    for i in range(0,int(rc/rs)+1):
        if not os.path.exists(str(i)):
            os.mkdir(str(i))
        #print ('running temp.sh...')
    subprocess.call('parallel --jobs {0} --no-notice < {1}/{2}/temp.sh'.format(threads,outpath,bcdir), shell=True)
    #subprocess.call('rm {0}/{1}/temp.sh -rf'.format(outpath,bcdir),shell=True)

  
