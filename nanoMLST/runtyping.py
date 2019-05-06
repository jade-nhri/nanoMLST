#!/usr/bin/env python3
import os, subprocess
import sys
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('inpath', help='the path to run typing')
parser.add_argument('outfile', help='an output file')
args = parser.parse_args()

indir=sys.argv[1]
indir=os.path.abspath(indir)
outfile=sys.argv[2]

mydir=[x for x in os.listdir(indir) if os.path.isdir(indir+'/'+x) and 'NB' in x]
print (sorted(mydir))
fw=open(outfile,'w')
for i in sorted(mydir):
    comm='MLSTtyping.py {0}/{1}/{1}_final.fa'.format(indir,i)
    print (comm)
    stdout=subprocess.getoutput(comm)
    print (stdout)
    lines=stdout.splitlines()
    fw.write(i+'\t'+lines[-1]+'\n')
fw.close()

