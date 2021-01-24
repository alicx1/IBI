import wget
import csv
import os
import subprocess as sp
path = os.getcwd()

def download_sample(url, md5, dirName):
    print("Téléchargement du fichier\n", dirName)
    nameFastQ = "./" + dirName + "/" + url.rsplit('/', 1)[-1]
    sp.call(['wget', '-O', nameFastQ, url])

    #md5 à check plus tard


lien = input("Tapez le lien du projet: \n")
project = lien.rsplit('/', 1)[-1] #On recup la derniere partie de l'url càd le code du projet
print(project)
print('Début du téléchargement du fichier TSV') #On télécharge le fichier TSV en se basant sur le code du projet
url = 'https://www.ebi.ac.uk/ena/portal/api/filereport?accession='+ project +'&result=read_run&fields=fastq_md5,fastq_ftp,sample_title&format=tsv&download=true'
nameTsv = "FILE_"+project+".tsv"
sp.call(['wget', '-O', nameTsv, url])
print("\n TSV file downloaded\n")


#Open the TSV fil using csv
tsv_file = open("./" + nameTsv)
read_tsv = csv.reader(tsv_file, delimiter="\t")


if not os.path.isdir('files'): os.mkdir('files')
for row in read_tsv:
  #print(row)
  pathFile = path + "/files/" + row[4]
  if not os.path.isdir(pathFile): os.mkdir(pathFile)
  print('\n Téléchargement du fichier zip\n')
  if row[2]:
      if ';' in row[3]:
          tmpFastQ = row[3].split(';')
          tmpHash= row[2].split(';')
          download_sample(tmpFastQ[0], tmpHash[0], "files/"+row[4])



'''
try:
    os.mkdir(path2)
except OSError:
    print ("Creation of the directory %s failed" % path2)
else:
    print ("Successfully created the directory %s " % path2)
    '''