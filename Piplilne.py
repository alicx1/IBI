import wget
import csv
import os

def download_sample(url, md5, name):
    print("Téléchargement du fichier\n", name)
    filename = wget.download(url)
    #md5 à check

'''
lien = input("Tapez le lien du projet: \n")
project = lien.rsplit('/', 1)[-1] #On recup la derniere partie de l'url càd le code du projet
print(project)
print('Début du téléchargement du fichier TSV') #On télécharge le fichier TSV en se basant sur le code du projet
url = 'https://www.ebi.ac.uk/ena/portal/api/filereport?accession='+ project +'&result=read_run&fields=fastq_md5,fastq_ftp,sample_title&format=tsv&download=true'
wget.download(url, './fichier.tsv')
print("\n")

'''
tsv_file = open("./fichier.tsv")
read_tsv = csv.reader(tsv_file, delimiter="\t")

for row in read_tsv:
  print(row)
  print('\n Téléchargement du fichier zip\n')
  if row[2]:
      if ';' in row[3]:
