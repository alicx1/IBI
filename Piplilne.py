import wget
import csv
import os
import hashlib
import subprocess as sp
path = os.getcwd()
'''
def download_sample(url, md5, dirName):
    print("Téléchargement du fichier", dirName)
    fastqName = url.rsplit('/', 1)[-1]
    pathFastQ = path + "/" + dirName + "/" + fastqName

    #Downloading file then moving it
    if (not os.path.isfile(pathFastQ)): 
        sp.call(['wget', '-O', fastqName, url]) 
        currentPath = path + "/" + fastqName
        os.replace(currentPath, pathFastQ)
    
    
    #Checking md5
    if (os.path.isfile(pathFastQ)): 
        currentMd5 = hashlib.md5(open(pathFastQ,'rb').read()).hexdigest()
        if currentMd5 == md5: print("md5 correct for " + fastqName + "\n")
        else: print("md5 incorrect for " + fastqName + "\n")

    else: print("The file " + fastqName + " does not exist\n")
        


lien = input("Tapez le lien du projet: \n")
project = lien.rsplit('/', 1)[-1] #On recup la derniere partie de l'url càd le code du projet
print(project)
print('Début du téléchargement du fichier TSV') #On télécharge le fichier TSV en se basant sur le code du projet
url = 'https://www.ebi.ac.uk/ena/portal/api/filereport?accession='+ project +'&result=read_run&fields=fastq_md5,fastq_ftp,sample_alias&format=tsv&download=true'
nameTsv = "FILE_"+project+".tsv"
sp.call(['wget', '-O', nameTsv, url])
print("\n TSV file downloaded\n")


#Open the TSV fil using csv
tsv_file = open("./" + nameTsv)
read_tsv = csv.reader(tsv_file, delimiter="\t")
next(read_tsv)  # skip the headers


if not os.path.isdir('files'): os.mkdir('files')
for row in read_tsv:
  if row[2]: #if the file is not empty
    pathFile = path + "/files/" + row[4]
    if not os.path.isdir(pathFile): os.mkdir(pathFile)
    if ';' in row[3]:
        tmpFastQ = row[3].split(';')
        tmpHash= row[2].split(';')
        download_sample(tmpFastQ[0], tmpHash[0], "files/"+row[4])
        download_sample(tmpFastQ[1], tmpHash[1], "files/"+row[4])
    else: download_sample(row[3], row[2], "files/"+row[4])
    '''
#bwa mem ref.fa read1.fq read2.fq > aln-pe.sam
#bwa index S288C_reference_sequence_R64-2-1_20150113.fsa 
refGen = "S288C_reference_genome_R64-2-1_20150113/S288C_reference_sequence_R64-2-1_20150113.fsa"
file1 = "files/UFMG-CM-Y215/ERR2299966_1.fastq.gz"
file2 = "files/UFMG-CM-Y215/ERR2299966_2.fastq.gz"
#sp.call(['bwa', 'index', refGen])
#sp.call(['bwa', 'index', file1])
#sp.call(['bwa', 'index', file2])

echantillon = "UFMG-CM-Y215"
SAMheader = '@RG\\tID:'+ echantillon +'\\tPL:ILLUMINA\\tPI:0\\tSM:'+ echantillon
#print (heaader)
#os.system("bwa mem -R '@RG\\tID:"+echantillon+"' "+refGen+" "+file1+" "+file2+ "> out.sam") 
#os.system("samtools view out.sam -o out.bam")
#os.system("samtools sort out.bam -o outSorted.bam")
#os.system("samtools flagstat outSorted.bam")
os.system("gatk MarkDuplicatesSpark -I outSorted.bam -O outMarked.bam")
# a execeuter: export PATH="/mnt/c/Users/PC/Documents/L3/IBI/gatk-4.1.9.0:$PATH"

#bwa mem -R '@RG\tID:echantillon\tPL:ILLUMINA' S288C_reference_genome_R64-2-1_20150113/S288C_reference_sequence_R64-2-1_20150113.fsa files/UFMG-CM-Y215/ERR2299966_1.fastq.gz files/UFMG-CM-Y215/ERR2299966_2.fastq.gz > res.sam












