from os import chdir
import time

#---------------------------------------------------------------------
#A RENSEIGNER

chemin= "G:/CPGE PTSI/TP2014/TP11 ameliorer les perf cin"
#entrer ci-dessus le chemin vers le répertoire où sont stockés vos fichiers : attention aux / ou \
# exemple : chemin= "G:/travail/SII"

fichierCSV= 'consignes.csv'
#entrer ci-dessus le nom du fichier csv (séparateur ;) où sont contenues les consignes de position successives des vérins

fichier_sortie= 'consignes.RES'
#entrer le nom que vous voulez pour le fichier de sortie, conserver l'extension .RES pour pouvoir l'ouvrir avec le logiciel STEWART

#le fichier base.RES doit être contenu dans le répertoire
#-------------------------------------------------------------------

chdir(chemin)

#lecture fichier csv
f = open(fichierCSV,'r',encoding = 'utf8')
cons=f.readlines()
f.close()

#stockage
tableau=[]
for ligne in cons:
    ligne=ligne.strip()
    ligne=ligne.split(';')
    tableau.append([ligne[1],ligne[2],ligne[3],ligne[4],ligne[5],ligne[6]])

#lecture fichier base
f = open('base.RES','r',encoding = 'utf8')
init=f.readlines()
f.close()

r=10
for p in range(1,101): # numero de la position
    for i in range(6):
     l_ver=init[r+i] #ligne r du fichier init
     l_ver=l_ver.split()
     l_ver[0]=' '+tableau[p+1][i] #1 ligne de titre sauter la position 0
     init[r+i]=l_ver[0]+'   '+ l_ver[1]+' '+l_ver[2]+' '+l_ver[3]+'\n'
    r=r+40

s = open(fichier_sortie,'w',encoding='utf8')
for ligne in init:
    s.write(ligne)
s.close()
 





