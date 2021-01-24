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
    currentMd5 = hashlib.md5(open(pathFastQ,'rb').read()).hexdigest()
    if currentMd5 == md5: print("md5 correct \n")
    else: print("md5 incorrect \n")
        


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