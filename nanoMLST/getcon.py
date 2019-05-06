#!/usr/bin/env python3
import os,sys,time
import subprocess

fast5dir=sys.argv[1]
infile=sys.argv[2]
outfile=sys.argv[3]
label=sys.argv[4]

threads=32
argv=sys.argv
if '-t' in argv:
    threads=argv[argv.index('-t')+1]


myTime=time.strftime('%m-%d %H:%M:%S',time.localtime(time.time()))
print (myTime)

comm='cp {0} draft.fa'.format(infile)
print (comm)
subprocess.getoutput(comm)

print(os.getcwd())

if label=='1':
    comm='nanopolish index -d {0} reads.fastq'.format(fast5dir)
    print (comm)
    stdout=subprocess.getoutput(comm)

comm='minimap2 -x map-ont -a -t {1} draft.fa reads.fastq.index | samtools sort -o reads.sorted{0}.bam -T reads.tmp -'.format(label,threads)
print (comm)
stdout=subprocess.getoutput(comm)
#print (stdout)

comm='samtools index reads.sorted{0}.bam'.format(label)
print (comm)
stdout=subprocess.getoutput(comm)



comm='python /opt/nanopolish/scripts/nanopolish_makerange.py draft.fa | parallel --results nanopolish.results'+label+' -P 8 \
nanopolish variants --methylation-aware dcm,dam --consensus -o plished'+label+'.{1}.vcf -w {1} -r reads.fastq -b reads.sorted'+label+'.bam -g draft.fa -t 8 --min-candidate-frequency 0.5'
print (comm)
stdout=subprocess.getoutput(comm)

comm="grep -i 'error' nanopolish.results{0}/1/*/stderr".format(label)
stdout=subprocess.getoutput(comm)
if stdout=="":
    comm='nanopolish vcf2fasta -g draft.fa plished{0}.*.vcf > {1}'.format(label,outfile)
    print (comm)
    stdout=subprocess.getoutput(comm)
else:
    seq=stdout.split('\n')
    for i in seq:
        seqout=i.split("/")[2]
        print (seqout)
        comm='nanopolish variants --methylation-aware dcm,dam --consensus -o  plished{0}.{1}.vcf -w '.format(label,seqout)+'"'+'{0}.vcf'.format(seqout)+'"'+' -r reads.fastq -b reads.sorted{0}.bam -g draft.fa -t 8 --min-candidate-frequency 0.5'.format(label)
        print ('    '+comm)
        subprocess.getoutput(comm)
    comm='nanopolish vcf2fasta -g draft.fa plished{0}.*.vcf > {1}'.format(label,outfile)
    print (comm)
    subprocess.getoutput(comm)

comm='rm plished*'
print (comm)
stdout=subprocess.getoutput(comm)

comm='rm draft.fa*'
print (comm)
stdout=subprocess.getoutput(comm)

comm='rm nanopolish.results* -rf'
print (comm)
stdout=subprocess.getoutput(comm)

myTime=time.strftime('%m-%d %H:%M:%S',time.localtime(time.time()))
print (myTime)

