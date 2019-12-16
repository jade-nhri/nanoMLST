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
parser.add_argument('-f5', help='the path to raw fast5, which contains multi-fast5 files')
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
if '-f5' in argv:
    rawf5dir=argv[argv.index('-f5')+1]

inpath=os.path.abspath(inpath)
outpath=os.path.abspath(outpath)
rawf5dir=os.path.abspath(rawf5dir)


print (inpath)
print (outpath)
print (rawf5dir)

if not os.path.exists(outpath):
    os.mkdir(outpath)

cwd=os.getcwd()
cwd=os.path.abspath(cwd)

os.chdir(inpath)
print (os.getcwd())
bcs=[x for x in os.listdir(inpath) if 'NB' in x and 'txt' in x]
for bc in bcs:
    print (bc)
    comm="sed -i '1iread_id' "+bc
    subprocess.getoutput(comm)
    bcdir=bc.replace('.txt','')
    comm='filter_reads --recursive --multi --workers {0} {1} {2}/{3} {4}'.format(threads,rawf5dir,outpath,bcdir,bc)
    print (comm)
    subprocess.getoutput(comm)
os.chdir(cwd)
