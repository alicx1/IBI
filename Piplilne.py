import wget
import csv
import os
import hashlib
import subprocess as sp
path = os.getcwd()


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
#sp.call(['wget', '-O', nameTsv, url])
print("\n TSV file downloaded\n")


#Open the TSV fil using csv
tsv_file = open("./" + nameTsv)
read_tsv = csv.reader(tsv_file, delimiter="\t")
next(read_tsv)  # skip the headers
refGen = "S288C_reference_genome_R64-2-1_20150113/S288C_reference_sequence_R64-2-1_20150113.fsa"
#copier le fsa et le renomer en fasta
refGenFasta = "S288C_reference_genome_R64-2-1_20150113/S288C_reference_sequence_R64-2-1_20150113.fasta"


if not os.path.isdir('files'): os.mkdir('files')
for row in read_tsv:
  if row[2]: #if the file is not empty
    pathFile = path + "/files/" + row[4]
    if not os.path.isdir(pathFile): os.mkdir(pathFile)
    if ';' in row[3]:
        tmpFastQ = row[3].split(';')
        tmpHash= row[2].split(';')
        #Téléchargement du fastq
        #download_sample(tmpFastQ[0], tmpHash[0], "files/"+row[4])
        #download_sample(tmpFastQ[1], tmpHash[1], "files/"+row[4])
        

        #Fichiers fastq
        echantillon = row[4]
        fastqName1 = tmpFastQ[0].rsplit('/', 1)[-1]
        fastqName2 = tmpFastQ[1].rsplit('/', 1)[-1]
        file1= "files/"+echantillon+"/"+fastqName1
        file2= "files/"+echantillon+"/"+fastqName2
        '''
        print(file1 + " \n" + file2)

        #BWA mem
        samFile = "files/"+ echantillon + "/out.sam"
        os.system("bwa mem -R '@RG\\tID:"+echantillon+"\\tSM:"+echantillon+"_sample' "+refGen+" "+file1+" "+file2+ "> "+samFile)

        #Samtools
        bamFile = "files/"+ echantillon + "/out.bam"
        os.system("samtools view "+ samFile +" -o " + bamFile)

        bamFileSorted = "files/"+ echantillon + "/outSorted.bam"
        os.system("samtools sort " + bamFile+ " -o " + bamFileSorted)
        
        os.system("samtools flagstat "+ bamFileSorted)

        #bamFileMarked = "files/"+ echantillon + "/outMarked.bam"
        os.system("gatk MarkDuplicatesSpark -I " + bamFileSorted + " -O " + bamFileMarked)
        '''
        bamFileMarked = "files/"+ echantillon + "/outMarked.bam"
        outGVCF = "files/GVCF/"+ echantillon + ".g.vcf.gz"
        os.system("gatk --java-options '-Xmx4g' HaplotypeCaller \
        -R "+ refGenFasta +" \
        -I "+ bamFileMarked +" \
        -O "+ outGVCF +" \
        -ERC GVCF "
        )
        '''
        #clean
        os.system("rm "+ samFile)
        os.system("rm "+ bamFile)
        os.system("rm "+ bamFileMarked)
        '''
    else: #download_sample(row[3], row[2], "files/"+row[4])

        #Fichiers fastq
        echantillon = row[4]
        fastqName = row[3].rsplit('/', 1)[-1]
        file = "files/"+echantillon+"/"+fastqName

        print(file + " \n")
        '''
        #BWA mem
        samFile = "files/"+ echantillon + "/out.sam"
        os.system("bwa mem -R '@RG\\tID:"+echantillon+"\\tSM:"+echantillon+"_sample' "+refGen+" "+file+ "> "+samFile)

        
        #Samtools
        bamFile = "files/"+ echantillon + "/out.bam"
        os.system("samtools view "+ samFile +" -o " + bamFile)

        bamFileSorted = "files/"+ echantillon + "/outSorted.bam"
        os.system("samtools sort " + bamFile+ " -o " + bamFileSorted)
        
        os.system("samtools flagstat "+ bamFileSorted)

        bamFileMarked = "files/"+ echantillon + "/outMarked.bam"
        os.system("gatk MarkDuplicatesSpark -I " + bamFileSorted + " -O " + bamFileMarked)
        '''
        bamFileMarked = "files/"+ echantillon + "/outMarked.bam"
        outGVCF = "files/GVCF/"+ echantillon + ".g.vcf.gz"
        os.system("gatk --java-options '-Xmx4g' HaplotypeCaller \
        -R "+ refGenFasta +" \
        -I "+ bamFileMarked +" \
        -O "+ outGVCF +" \
        -ERC GVCF "
        )
        '''
        #clean
        os.system("rm "+ samFile)
        os.system("rm "+ bamFile)
        os.system("rm "+ bamFileMarked)
        '''

'''

###https://www.ebi.ac.uk/ena/browser/view/PRJEB24932
#bwa mem ref.fa read1.fq read2.fq > aln-pe.sam
#bwa index S288C_reference_sequence_R64-2-1_20150113.fsa 
#bwa mem -R '@RG\tID:echantillon\tPL:ILLUMINA' S288C_reference_genome_R64-2-1_20150113/S288C_reference_sequence_R64-2-1_20150113.fsa files/UFMG-CM-Y215/ERR2299966_1.fastq.gz files/UFMG-CM-Y215/ERR2299966_2.fastq.gz > res.sam
#refGen = "S288C_reference_genome_R64-2-1_20150113/S288C_reference_sequence_R64-2-1_20150113.fsa"
file1 = "files/UFMG-CM-Y223/ERR2299967_1.fastq.gz"
file2 = "files/UFMG-CM-Y223/ERR2299967_2.fastq.gz"
#sp.call(['bwa', 'index', refGen])
#sp.call(['bwa', 'index', file1])
#sp.call(['bwa', 'index', file2])

echantillon = "UFMG-CM-Y223"
#SAMheader = '@RG\\tID:'+ echantillon +'\\tPL:ILLUMINA\\tPI:0\\tSM:'+ echantillon
#print (heaader)
os.system("bwa mem -R '@RG\\tID:"+echantillon+"\\tSM:"+echantillon+"_sample' "+refGen+" "+file1+" "+file2+ "> out2.sam")
#laisser le bam sorted pour plus tard
os.system("samtools view out2.sam -o out2.bam")
os.system("samtools sort out2.bam -o outSorted2.bam")
os.system("samtools flagstat outSorted2.bam")
os.system("gatk MarkDuplicatesSpark -I outSorted2.bam -O outMarked2.bam")
os.system("samtools faidx "+ refGen)
os.system("gatk CreateSequenceDictionary -R " + refGen)
#copier le fsa et le renomer en fasta
refGenFasta = "S288C_reference_genome_R64-2-1_20150113/S288C_reference_sequence_R64-2-1_20150113.fasta"
#os.system("samtools faidx "+ refGenFasta)
#os.system("gatk CreateSequenceDictionary -R " + refGenFasta)
os.system("gatk --java-options '-Xmx4g' HaplotypeCaller \
   -R "+ refGenFasta +" \
   -I outMarked2.bam \
   -O output2.g.vcf.gz \
   -ERC GVCF "
   )
   '''