#!/usr/bin/env python3
import os, sys
import subprocess

def reverse_complement(seq):
    seq=seq.upper()
    complement = {'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A', 'K':'M','M':'K','R':'Y','Y':'R','S':'W','W':'W','B':'V','V':'B','H':'G','D':'C','X':'N','N':'N'}
    bases = list(seq)
    bases = bases[::-1]
    rc=[complement.get(base,base) for base in bases]
    bases = ''.join(rc)
    return bases
def read_fasta(fp):
    name, seq = None, []
    for line in fp:
        line = line.rstrip()
        if line.startswith(">"):
            if name: yield (name, ''.join(seq))
            name, seq = line, []
        else:
            seq.append(line)
    if name: yield (name, ''.join(seq))
    return seq,name

fw=open('dualbcs.fa','w')
f1=open('/opt/nanoMLST/nanoMLST/NB.fa')
with f1 as fp1:
    for name1, seq1 in read_fasta(fp1):
        #print (name1)
        f2=open('/opt/nanoMLST/nanoMLST/PB.fa')
        with f2 as fp2:
            for name2, seq2 in read_fasta(fp2):
                bc=name1.replace('>','')+name2.replace('>','')
                seq=reverse_complement(seq1)+'CAGCACCT'+seq2
                #print (bc)
                #print (seq)
                fw.write('>'+bc+'\n')
                fw.write(seq+'\n')
        f2.close()

f1.close()
fw.close()
