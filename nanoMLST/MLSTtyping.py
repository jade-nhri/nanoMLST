#!/usr/bin/env python3
import sys,os
import subprocess
import pandas as pd
from Bio.Seq import Seq
from Bio.Alphabet import generic_dna

infile=sys.argv[1]
infile=os.path.abspath(infile)

download=False
if '--updating' in sys.argv:
    download=True

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


def marker (infile,download):
    d=dict()
    if download==True:
        if os.path.exists(infile+".tfa"):
            subprocess.getoutput('rm '+infile+".tfa")
        getf="wget https://pubmlst.org/data/alleles/saureus/"+infile+".tfa"
        print (getf)
        subprocess.getoutput(getf)
        subprocess.getoutput("rm saureus.txt")
        print ("wget https://pubmlst.org/data/profiles/saureus.txt")
        subprocess.getoutput("wget https://pubmlst.org/data/profiles/saureus.txt")
    if not os.path.exists(infile+".tfa"):
        getf="wget https://pubmlst.org/data/alleles/saureus/"+infile+".tfa"
        print (getf)
        subprocess.getoutput(getf)
    if not os.path.exists("saureus.txt"):
        print ("wget https://pubmlst.org/data/profiles/saureus.txt")
        subprocess.getoutput("wget https://pubmlst.org/data/profiles/saureus.txt")
   
    if not os.path.exists(infile+'_f.tfa'):
        f=open(infile+'.tfa')
        fw=open(infile+'_f.tfa','w')
        fw1=open(infile+'_excluded.tfa','w')
        with f as fp:
             for name, seq in read_fasta(fp):
                 name=name.replace('>','')
                 #d[name]=seq
                 coding_dna=Seq(seq,generic_dna)
                 if "*" not in coding_dna.translate():
                     d[name]=seq
                     fw.write('>'+name+'\n')
                     fw.write(seq+'\n')
                 else:
                     fw1.write('>'+name+'\n')
                     fw1.write(seq+'\n')
        fw1.close()
        fw.close()
        f.close()
    if os.path.exists(infile+'_f.tfa'):
        f=open(infile+'_f.tfa')
        with f as fp:
            for name, seq in read_fasta(fp):
                name=name.replace('>','')
                d[name]=seq
        f.close()
    return (d)

def typing (name,fa,gene):
    for key, value in gene.items():
        if value in fa[name]:
            return (key)

def processgap (query,subject):
    gappos=0
    k=3
    if '-' in query:
        for i in range(len(query)):
            if '-AA' in query[i:i+3] or 'AA-' in query[i:i+3]:
                gappos=i
                if subject[gappos:gappos+3]=='AAA':
                    print ("   gap in query:"+query[gappos-k:gappos+3+k]+"==>"+subject[gappos-k:gappos+3+k])
                    query=query.replace(query[gappos-k:gappos+3+k],subject[gappos-k:gappos+3+k])

            if '-TT' in query[i:i+3] or 'TT-' in query[i:i+3]:
                gappos=i
                if subject[gappos:gappos+3]=='TTT':
                    print ("   gap in query:"+query[gappos-k:gappos+3+k]+"==>"+subject[gappos-k:gappos+3+k])
                    query=query.replace(query[gappos-k:gappos+3+k],subject[gappos-k:gappos+3+k])
            if '-CC' in query[i:i+3] or 'CC-' in query[i:i+3]:
                gappos=i
                if subject[gappos:gappos+3]=='CCC':
                    print ("   gap in query:"+query[gappos-k:gappos+3+k]+"==>"+subject[gappos-k:gappos+3+k])
                    query=query.replace(query[gappos-k:gappos+3+k],subject[gappos-k:gappos+3+k])
            if '-GG' in query[i:i+3] or 'GG-' in query[i:i+3]:
                gappos=i
                if subject[gappos:gappos+3]=='GGG':
                    print ("   gap in query:"+query[gappos-k:gappos+3+k]+"==>"+subject[gappos-k:gappos+3+k])
                    query=query.replace(query[gappos-k:gappos+3+k],subject[gappos-k:gappos+3+k])
    if '-' in subject:
        for i in range(len(subject)):
            if '-AA' in subject[i:i+3] or 'AA-' in subject[i:i+3]:
                gappos=i
                if query[gappos:gappos+3]=='AAA':
                    print ("   gap in subject:"+query[gappos-k:gappos+3+k]+"==>"+subject[gappos-k:gappos+3+k].replace('-',''))
                    query=query.replace(query[gappos-k:gappos+3+k],subject[gappos-k:gappos+3+k].replace('-',''))
                    subject=subject.replace(subject[gappos-k:gappos+3+k],subject[gappos-k:gappos+3+k].replace('-',''))
            if '-TT' in subject[i:i+3] or 'TT-' in subject[i:i+3]:
                gappos=i
                if query[gappos:gappos+3]=='TTT':
                    print ("   gap in subject:"+query[gappos-k:gappos+3+k]+"==>"+subject[gappos-k:gappos+3+k].replace('-',''))
                    query=query.replace(query[gappos-k:gappos+3+k],subject[gappos-k:gappos+3+k].replace('-',''))
                    subject=subject.replace(subject[gappos-k:gappos+3+k],subject[gappos-k:gappos+3+k].replace('-',''))
            if '-CC' in subject[i:i+3] or 'CC-' in subject[i:i+3]:
                gappos=i
                if query[gappos:gappos+3]=='CCC':
                    print ("   gap in subject:"+query[gappos-k:gappos+3+k]+"==>"+subject[gappos-k:gappos+3+k].replace('-',''))
                    query=query.replace(query[gappos-k:gappos+3+k],subject[gappos-k:gappos+3+k].replace('-',''))
                    subject=subject.replace(subject[gappos-k:gappos+3+k],subject[gappos-k:gappos+3+k].replace('-',''))
            if '-GG' in subject[i:i+3] or 'GG-' in subject[i:i+3]:
                gappos=i
                if query[gappos:gappos+3]=='GGG':
                    print ("   gap in subject:"+query[gappos-k:gappos+3+k]+"==>"+subject[gappos-k:gappos+3+k].replace('-',''))
                    query=query.replace(query[gappos-k:gappos+3+k],subject[gappos-k:gappos+3+k].replace('-',''))
                    subject=subject.replace(subject[gappos-k:gappos+3+k],subject[gappos-k:gappos+3+k].replace('-',''))

    return (query)


def correct (fafile,gene):
    comm="makeblastdb -in {0}_f.tfa -dbtype nucl".format(gene)
    subprocess.getoutput(comm)
    comm="blastn -query {0} -db {1}_f.tfa -out temp.result -max_target_seqs 10 -num_threads 1 -outfmt '7 qseqid stitle qlen slen length qstart qend sstart send pident evalue qseq sseq'".format(infile,gene)
    subprocess.getoutput(comm)
    f=open('temp.result')

    my_dict=dict()
    qseq=[]
    sseq=[]
    for i in f:
        if '#' in i:continue
        tmp=i.split()
        qseq.append(tmp[11])
        sseq.append(tmp[12])
    f.close()
    gappos=0
    k=5
    
    query=[]
    for j in range(10):
        query.append(processgap(qseq[j],sseq[j]))
    #print (query)
    #print (set(query))
    n=[]
    for i in query:
        n.append(query.count(i))
    maxn=max(n)
    print (maxn)
    for i in query:
        if query.count(i)==maxn:
            repquery=i
            break
   # print ([i for i in query if query.count(i) >5])
    #print (list(set(query))[0])
    #return (list(set(query))[0])
    return (repquery)
    

if download==True:
    d1=marker('arcC',True)
    d2=marker('aroE',True)
    d3=marker('glpF',True)
    d4=marker('gmk',True)
    d5=marker('pta',True)
    d6=marker('tpi',True)
    d7=marker('yqiL',True)
else:
    d1=marker('arcC',False)
    d2=marker('aroE',False)
    d3=marker('glpF',False)
    d4=marker('gmk',False)
    d5=marker('pta',False)
    d6=marker('tpi',False)
    d7=marker('yqiL',False)


f=open(infile)
d=dict()
with f as fp:
    for name, seq in read_fasta(fp):
        name=name.replace('>','')
        d[name]=seq
f.close()

type1=typing('arc',d,d1)
if type1==None:
   print ('Correcting arc seqquence')
   d['arc']= correct(infile,'arcC')
   type1=typing('arc',d,d1)

type2=typing('aro',d,d2)
if type2==None:
   print ('Correcting aro sequence')
   d['aro']= correct(infile,'aroE')
   type2=typing('aro',d,d2)

type3=typing('glp',d,d3)
if type3==None:
   print ('Correcting glp sequence')
   d['glp']= correct(infile,'glpF')
   type3=typing('glp',d,d3)

type4=typing('gmk',d,d4)
if type4==None:
   print ('Correcting gmk sequence')
   d['gmk']= correct(infile,'gmk')
   type4=typing('gmk',d,d4)

type5=typing('pta',d,d5)
if type5==None:
   print ('Correcting pta sequence')
   d['pta']= correct(infile,'pta')
   type5=typing('pta',d,d5)

type6=typing('tpi',d,d6)
if type6==None:
   print ('Correcting tpi sequence')
   d['tpi']= correct(infile,'tpi')
   type6=typing('tpi',d,d6)

type7=typing('yqi',d,d7)
if type7==None:
   print ('Correcting yqi sequence')
   d['yqi']= correct(infile,'yqiL')
   type7=typing('yqi',d,d7)

print (type1)
print (type2)
print (type3)
print (type4)
print (type5)
print (type6)
print (type7)

if type1!=None and type2!=None and type3!=None and type4!=None and type5!=None and type6!=None and type7!=None:
    out=type1+','+type2+','+type3+','+type4+','+type5+','+type6+','+type7
    print (out)

    df=pd.read_table('saureus.txt')
    mlst=dict()
    for i in df.index:
        comb='arcC_'+str(df.iloc[i,1])+',aroE_'+str(df.iloc[i,2])+',glpF_'+str(df.iloc[i,3])+',gmk_'+str(df.iloc[i,4])+',pta_'+str(df.iloc[i,5])+',tpi_'+str(df.iloc[i,6])+',yqiL_'+str(df.iloc[i,7])
        mlst[comb]=df.iloc[i,0]

    if out not in mlst.keys():
        print ('New MLST type!')
    else:
        print (mlst[out])

else:
    print ("MLST fail")


