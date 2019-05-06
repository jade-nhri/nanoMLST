#!/usr/bin/env python3
import os,sys,subprocess
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('inpath', help='the path to run consensus')
parser.add_argument('f5path', help='the path with fast5')
parser.add_argument('-t', help='threads (default=32)')
args = parser.parse_args()


indir=sys.argv[1]
indir=os.path.abspath(indir)

bf5dir=sys.argv[2]
bf5dir=os.path.abspath(bf5dir)

threads=32
argv=sys.argv
if '-t' in argv:
    threads=argv[argv.index('-t')+1]


myfile=[x for x in os.listdir(indir) if '.fq' in x]

print (sorted(myfile))

os.chdir(indir)
reffile='/opt/nanoMLST/nanoMLST/refs.fa'

for i in sorted(myfile):
    mydir=i.replace('.fq','')
    if (os.path.exists(mydir)):
        comm='rm -rf {0}'.format(mydir)
        print (comm)
        subprocess.getoutput(comm)
    os.mkdir(mydir)
    os.chdir(mydir)
    print (os.getcwd())
    comm='cp ../{0} ./reads.fastq'.format(i)
    print (comm)
    subprocess.getoutput(comm)

#racon1
    comm='cp {0} draft.fa'.format(reffile)
    subprocess.getoutput(comm)
    comm='minimap2 -x map-ont -t {0} draft.fa reads.fastq > mapreads.paf'.format(threads)
    print (comm)
    stdout=subprocess.getoutput(comm)
    #print (stdout)
    comm='racon -t {0} reads.fastq mapreads.paf draft.fa > racon.fa'.format(threads)
    print (comm)
    stdout=subprocess.getoutput(comm)
    #print (stdout)
# 
   
    comm='getcon.py {2}/{0} {3} {0}_1.fa 1 -t {1}'.format(mydir,threads,bf5dir,'racon.fa')
    print (comm)
    stdout=subprocess.getoutput(comm)
    print (stdout)
    comm="grep '>' {0}_1.fa | wc -l".format(mydir)
    N=subprocess.getoutput(comm)
    if int(N)<7:
        comm='getcon.py {2}/{0} {3} {0}_1.fa 1 -t {1}'.format(mydir,threads,bf5dir,'racon.fa')
        subprocess.getoutput(comm)
    
    
    comm='getcon.py {2}/{0} {0}_1.fa {0}_2.fa 2 -t {1}'.format(mydir,threads,bf5dir)
    print (comm)
    stdout=subprocess.getoutput(comm)
    print (stdout)
    comm="grep '>' {0}_2.fa | wc -l".format(mydir)
    N=subprocess.getoutput(comm)
    if int(N)<7:
        print ('repolishing\n')
        comm='getcon.py {2}/{0} {0}_1.fa {0}_2.fa 2 -t {1}'.format(mydir,threads,bf5dir)
        subprocess.getoutput(comm)

    
    if os.path.getsize(mydir+'_2.fa')==os.path.getsize(mydir+'_1.fa'):
            os.rename(mydir+'_2.fa',mydir+'_final.fa')

    if not os.path.exists(mydir+'_final.fa'):
        comm='minimap2 -x map-ont -t {1} {0} reads.fastq > mapreads.paf'.format('racon.fa',threads)
        print (comm)
        stdout=subprocess.getoutput(comm)
        comm='racon -t {1} reads.fastq mapreads.paf {0} > racon_1.fa'.format('racon.fa',threads)
        print (comm)
        stdout=subprocess.getoutput(comm)
        #print (stdout)

        comm='minimap2 -x map-ont -t {0} racon_1.fa reads.fastq > mapreads1.paf'.format(threads)
        print (comm)
        stdout=subprocess.getoutput(comm)
        #print (stdout)
        comm='racon -t {0} reads.fastq mapreads1.paf racon_1.fa > racon_2.fa'.format(threads)
        print (comm)
        stdout=subprocess.getoutput(comm)
        #print (stdout)
        
        comm='getcon.py {2}/{0} racon_2.fa {0}_3.fa 3 -t {1}'.format(mydir,threads,bf5dir)
        print (comm)
        stdout=subprocess.getoutput(comm)
        print (stdout)
        comm="grep '>' {0}_3.fa | wc -l".format(mydir)
        N=subprocess.getoutput(comm)
        if int(N)<7:
            print ('repolishing\n')
            comm='getcon.py {2}/{0} racon_2.fa {0}_3.fa 3 -t {1}'.format(mydir,threads,bf5dir)
            subprocess.getoutput(comm)
   
        for j in range (4,10):
            k=j-1
            comm='getcon.py {4}/{0} {0}_{2}.fa {0}_{1}.fa {1} -t {3}'.format(mydir,j,k,threads,bf5dir)
            print (comm)
            stdout=subprocess.getoutput(comm)
            print (stdout)
            comm="grep '>' {0}_{1}.fa | wc -l".format(mydir,j)
            N=subprocess.getoutput(comm)
            if int(N)<7:
                comm='getcon.py {4}/{0} {0}_{2}.fa {0}_{1}.fa {1} -t {3}'.format(mydir,j,k,threads,bf5dir)
                subprocess.getoutput(comm)

            if os.path.getsize(mydir+'_'+str(k)+'.fa')==os.path.getsize(mydir+'_'+str(j)+'.fa'):
               break
        os.rename(mydir+'_'+str(j)+'.fa',mydir+'_final.fa')

    os.chdir('..')

