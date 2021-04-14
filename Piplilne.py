#Réalisé dans le cadre d'un projet d'étude à l'Université de Paris-Saclay
#UE: IBI
#Réalisé par: KAMOUN Alicx, KOMARA Mohamed Ba et LAKHEL Amine
#Sous la supervision de Mme. POUYET Fanny
#2020-2021

import wget
import csv
import os
import hashlib
import subprocess as sp
path = os.getcwd()

CHECK_DL =  1 #Télécharger les fichiers fastQ et check md5
CHECK_CREATEGVCF = 1 #Créer le .sam .bam .bamSorted et .bamMarked puis créer le GVCF
CHECK_CLEAN = 1 #Supprime le fichier .sam, .bam et .bamSorted
CHECK_GENOMEREF = 1 #Indexation du génome de refèrence
CHECK_CREATEVCF = 1 #Créer la base de donnée et la table des VCF
CHECK_SNP_ANNOTATION = 1 #Filtrer les SNP puis créer le fichier annotation
CHECK_AFTER_SCRIPTR = 0 #Faire la suite des commandes après avoir utilisé le scriptR

###### A FAIRE Avant de lancer le script:#################################
##Lien du projet qu'on a utilisé: https://www.ebi.ac.uk/ena/browser/view/PRJEB24932
#Quelques traitements pour le fichier de génome de référence
# Mettre le genome de reference ici
refGen = "S288C_reference_genome_R64-2-1_20150113/S288C_reference_sequence_R64-2-1_20150113.fsa"
#copier le fichier .fsa et le renommer en .fasta
refGenFasta = "S288C_reference_genome_R64-2-1_20150113/S288C_reference_sequence_R64-2-1_20150113.fasta"
####
# Placer le fichier intervals.list dans files/intervals.list
##############################################

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
        #Téléchargement du fastq
        if (CHECK_DL == 1):
            download_sample(tmpFastQ[0], tmpHash[0], "files/"+row[4])
            download_sample(tmpFastQ[1], tmpHash[1], "files/"+row[4])
        
        #Fichiers fastq
        echantillon = row[4]
        fastqName1 = tmpFastQ[0].rsplit('/', 1)[-1]
        fastqName2 = tmpFastQ[1].rsplit('/', 1)[-1]
        file1= "files/"+echantillon+"/"+fastqName1
        file2= "files/"+echantillon+"/"+fastqName2
        
        #Etapes de création du GVCF
        if (CHECK_CREATEGVCF == 1):

            #BWA mem
            samFile = "files/"+ echantillon + "/out.sam"
            os.system("bwa mem -R '@RG\\tID:"+echantillon+"\\tSM:"+echantillon+"_sample' "+refGen+" "+file1+" "+file2+ "> "+samFile)

            #Samtools
            bamFile = "files/"+ echantillon + "/out.bam"
            os.system("samtools view "+ samFile +" -o " + bamFile)

            bamFileSorted = "files/"+ echantillon + "/outSorted.bam"
            os.system("samtools sort " + bamFile+ " -o " + bamFileSorted)
            
            os.system("samtools flagstat "+ bamFileSorted)

            bamFileMarked = "files/"+ echantillon + "/outMarked.bam"
            os.system("gatk MarkDuplicatesSpark -I " + bamFileSorted + " -O " + bamFileMarked)
            
            bamFileMarked = "files/"+ echantillon + "/outMarked.bam"
            outGVCF = "files/GVCF/"+ echantillon + ".g.vcf.gz"
            os.system("gatk --java-options '-Xmx4g' HaplotypeCaller \
            -R "+ refGenFasta +" \
            -I "+ bamFileMarked +" \
            -O "+ outGVCF +" \
            -ERC GVCF "
            )
        
        #clean
        if(CHECK_CLEAN == 1):
            os.system("rm "+ samFile)
            os.system("rm "+ bamFile)
            os.system("rm "+ bamFileSorted)
        
    else:
        #Téléchargement du fichier fastq
        if (CHECK_DL == 1):
            download_sample(row[3], row[2], "files/"+row[4])

        #Fichiers fastq
        echantillon = row[4]
        fastqName = row[3].rsplit('/', 1)[-1]
        file = "files/"+echantillon+"/"+fastqName
        
        #Etapes de création du GVCF
        if (CHECK_CREATEGVCF == 1):
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
            
            bamFileMarked = "files/"+ echantillon + "/outMarked.bam"
            outGVCF = "files/GVCF/"+ echantillon + ".g.vcf.gz"
            os.system("gatk --java-options '-Xmx4g' HaplotypeCaller \
            -R "+ refGenFasta +" \
            -I "+ bamFileSorted +" \
            -O "+ outGVCF +" \
            -ERC GVCF "
            )
        
        #clean
        if(CHECK_CLEAN == 1):
            os.system("rm "+ samFile)
            os.system("rm "+ bamFile)
            os.system("rm "+ bamFileMarked)

#Indexation du genome de référence
if (CHECK_GENOMEREF == 1):
    sp.call(['bwa', 'index', refGen])
    os.system("samtools faidx "+ refGen)
    os.system("gatk CreateSequenceDictionary -R " + refGen)
    #copier le fsa et le renomer en fasta
    os.system("samtools faidx "+ refGenFasta)
    os.system("gatk CreateSequenceDictionary -R " + refGenFasta)


#Création de la database et de la table des VCF
if (CHECK_CREATEVCF == 1):
    #Création de la liste de gvcf pour l'utiliser avec genomicsDBImport
    commandeV = ''
    listFiles = os.listdir('files/GVCF')
    for x in listFiles:
        if not(".tbi" in x):
            commandeV += '-V files/GVCF/' + x + ' \\\n'

    os.system("gatk --java-options \"-Xmx4g -Xms4g -DGATK_STACKTRACE_ON_USER_EXCEPTION=true\" GenomicsDBImport \
        " + commandeV + 
        "--genomicsdb-workspace-path my_database2 \
        -L files/intervals.list"
    )

    os.system("gatk --java-options '-Xmx4g' GenotypeGVCFs \
    -R "+ refGenFasta +" \
    -V gendb://my_database2 \
    -O table.vcf.gz"
    )

if (CHECK_SNP_ANNOTATION == 1):
    #Création de la table des SNP
    os.system("gatk SelectVariants \
    -R "+ refGenFasta +" \
    -V table.vcf.gz \
    --select-type-to-include SNP \
    -O table_raw.vcf.gz "
    )

    #Création des annotations
    os.system("bcftools query -f '%CHROM\t%POS\t%QD\t%FS\t%MQ\t%MQRankSum\t%ReadPosRankSum\t%SOR\n' table_raw.vcf.gz >> table_raw_annotations")

# On utilise le scriptR afin de créer des courbes et avoir la valeur des filtres qu'on rentrea dans la fonction ci dessous

if (CHECK_AFTER_SCRIPTR = 1):
    #Ne marche pas pour des raisons qu'on ignore
    os.system("gatk VariantFiltration \
    -R "+ refGenFasta +" \
    -V table_raw.vcf.gz \
    -filter "QD < 0" --filter-name "QD" \
    -filter "SOR < 0" --filter-name "SOR" \
    -filter "FS > 0" --filter-name "FS" \
    -filter "MQ < 0" --filter-name "MQ" \
    -filter "MQRankSum < 0" --filter-name "MQRankSum" \
    -filter "ReadPosRankSum < 0" --filter-name "ReadPosRankSum" \
    -O table_filtered.vcf.gz"
    )

    #Marche
    os.system("vcftools --gzvcf table_filtered.vcf.gz --remove-filtered-all --recode --stdout | gzip -c > table_PASS.vcf.gz")

    #bcftools query à faire