#!/usr/bin/env python3
import sys, os, subprocess
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-s', help='the sequencing summary file produced by Albacore or Guppy')
parser.add_argument('-q', help='the sequencing reads in fastq')
parser.add_argument('-f5', help='the fast5 folder')
parser.add_argument('-o', help='an output folder')
parser.add_argument('-t', help='threads (default=16)')
parser.add_argument('-m', help='set True for mutli-fast5')
args = parser.parse_args()

threads=16
argv=sys.argv
if '-s' in argv:
    indexfile=argv[argv.index('-s')+1]
    indexfile=os.path.abspath(indexfile)
if '-q' in argv:
    fqfile=argv[argv.index('-q')+1]
    fqfile=os.path.abspath(fqfile)
if '-f5' in argv:
    f5dir=argv[argv.index('-f5')+1]
    f5dir=os.path.abspath(f5dir)
if '-o' in argv:
    outdir=argv[argv.index('-o')+1]
    outdir=os.path.abspath(outdir)
    if not os.path.exists(outdir):
        os.mkdir(outdir)
if '-t' in argv:
    threads=argv[argv.index('-t')+1]
script='binf5.py'
if '-m' in argv:
    script='binf5m.py'
else:
    script='binf5.py'
   

dualbcs='/opt/nanoMLST/nanoMLST/dualbcs.fa'

#To map sequencing reads to the dual-barcode sequences using minimpa2:
comm='minimap2 {0} {1} -k7 -A1 -m42 -w1 -t {3} > {2}/out.paf'.format(dualbcs,fqfile,outdir,threads)
print (comm)
subprocess.getoutput(comm)

#To generate demultiplexed reads using getbcfa.py:
comm='getbcfq.py -m {0}/out.paf -i {1} -o {0}/outfq'.format(outdir,fqfile)
print (comm)
subprocess.getoutput(comm)

#To bin fast5 files into dual-barcode folders using binf5.py:
comm='{4} -i {0}/outfq -o {0}/binf5 -ss {1} -f5 {2} -t {3}'.format(outdir,indexfile,f5dir,threads,script)
print (comm)
subprocess.getoutput(comm)

#To generate consensus sequences using runcons.py:
comm='runcons.py {0}/outfq {0}/binf5'.format(outdir)
print (comm)
subprocess.getoutput(comm)

#To perform MLST analysis using runtyping.py:
os.chdir(outdir)
os.mkdir('mlst')
os.chdir('mlst')
comm='runtyping.py {0}/outfq mlst_list.txt > log.txt'.format(outdir)
print (comm)
subprocess.getoutput(comm)

comm='cat {0}/mlst/mlst_list.txt'.format(outdir)
print (comm)
stdout=subprocess.getoutput(comm)
print (stdout)



