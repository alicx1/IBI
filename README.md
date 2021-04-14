# IBI

#Réalisé dans le cadre d'un projet d'étude à l'Université de Paris-Saclay
#UE: IBI
#Réalisé par: KAMOUN Alicx, KOMARA Mohamed Ba et LAKHEL Amine
#Sous la supervision de Mme. POUYET Fanny
#2020-2021
###### A FAIRE Avant de lancer le script:
##Lien du projet qu'on a utilisé: https://www.ebi.ac.uk/ena/browser/view/PRJEB24932
#Quelques traitements pour le fichier de génome de référence
Mettre le genome de reference ici
refGen = "S288C_reference_genome_R64-2-1_20150113/S288C_reference_sequence_R64-2-1_20150113.fsa"
copier le fichier .fsa et le renommer en .fasta
refGenFasta = "S288C_reference_genome_R64-2-1_20150113/S288C_reference_sequence_R64-2-1_20150113.fasta"
####
Placer le fichier intervals.list dans files/intervals.list
Installer certains logiciels:
Installer BioConda avec:   curl -O https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
                            sh Miniconda3-latest-Linux-x86_64.sh
 Installer vcfTools avec: sudo apt install vcftools
 Installer java8 avec: sudo apt install openjdk-8-jdk
 Installer gatk avec: conda install -c bioconda gatk4
 Install the other missing like this
##############################################
