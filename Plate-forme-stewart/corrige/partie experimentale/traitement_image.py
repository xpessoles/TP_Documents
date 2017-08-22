# -*- coding: utf-8 -*-
"""
Created on Mon Jan 19 19:45:24 2015

@author: Viviane Reydellet
"""
import sys

sys.path.append('C:\Program Files (x86)\WinPython-64bit-2.7.5.1\python-2.7.5.amd64\Lib\site-packages')
#sys.path.append('C:\WinPython-32bit-2.7.8.2\python-2.7.8\Lib\site-packages')

import Tkinter as tk
import cv2
import fonctions_traitement as ft
import xlrd
from xlwt import Workbook






#-----------------------------------------------------------------------------
#A RENSEIGNER
#------------------------------------------------------------------------------
#donner ci-dessous le nom du fichier video au format .avi a traiter (ce fichier doit être dans le répertoire courant)
video_a_traiter="plateforme AMC.avi"

#donner ci-dessous le nom du fichier dans lequel seront stockés les résultats (fichier Excel)
fic = r"resultat_AMC.xls"











################################################################################
#definition des fonctions
#################################################################################
def affichage_traitement(im_b,hsv,diametre):
    '''resize et seuille l'image, affiche l'image initiale et le resultat'''
    im_b = cv2.resize(im_b,dsize=(0,0),fx=0.3,fy=0.3) #redimensionne à 324*576
    # frame=frame[0:540,0:960] #recadre
    im_seuil = ft.seuillage(im_b,hsv)
    im_c=im_b
    [im_c,x,y]=ft.cherche_forme(im_seuil,im_b)
    cv2.circle(im_c,(x,y),diametre,(0,255,0),1) #affiche le cercle réglable pour l'echelle
    cv2.imshow('image initiale',im_c)
    cv2.imshow('image seuillee',im_seuil)
    
#action est lancée à partir du moment où l'on touche à n'importe quelle scale, elle seuille l'image et affiche les images correspondantes
def action(f):
    '''lit les réglages effectués et seuille l'image en fonction'''
    #lecture des paramètres réglés
    global hsv
    global diametre
    hsv=[]
    for e in r:
        hsv.append(int(e.get()))
    diametre=int(d.get())
    affichage_traitement(im_base,hsv,diametre)
        
    
def passe():
    '''lit l'image suivante et affiche les 2 images initiales et seuillée'''
    global im_base
    global num_image
    ret,im_base=cap.read()
    num_image=num_image+1
    #texte0=canvas2.create_text(50, 50, text="image n° "+str(num_image), fill="blue")
    if ret:   
        affichage_traitement(im_base,hsv,diametre)
    else:
        revient()
    
def passe10():
    '''lit l'image suivante et affiche les 2 images initiales et seuillée'''
    global im_base
    global num_image
    for i in range(10):    
        ret,im_base=cap.read()
        num_image=num_image+10
    if ret:
        affichage_traitement(im_base,hsv,diametre)
    else:
        revient()

def revient():
    '''redemarre la lecture de la video au début'''
    global num_image
    global im_base
    global cap
    cap.release()
    cap = cv2.VideoCapture(video_a_traiter)
    ret,im_base=cap.read()
    affichage_traitement(im_base,hsv,diametre)
    num_image=1

def ecrit_excel(x,y,path):
    '''ecrit les listes x et y dans excel''' 
        
    # On créer un "classeur"
    classeur = Workbook()
    # On ajoute une feuille au classeur
    feuille = classeur.add_sheet("resultat_traitement")

    feuille.write(0, 0, 'x en mm')
    feuille.write(0, 1, 'y en mm')

    for i in range(len(x)):
        # Ecrire x dans la cellule à la ligne i et la colonne 0
        feuille.write(i+1, 0, x[i])
        # Ecrire y dans la cellule à la ligne 0 et la colonne 1
        feuille.write(i+1, 1, y[i])
    # Ecriture du classeur sur le disque
    classeur.save(path)
    print u"Fichier créé: {}".format(path)


def traitement_final():
    '''reprend la video au début, traite son ensemble et retourne le tableau des positions'''
    global cap
    global hsv
    global diametre
    global lx
    global ly
    cap.release()
    cv2.destroyAllWindows()
    
    lx=[]
    ly=[]
    #calcul de l'echelle: le grand cercle mesure en réalité 180mm, il est reconnu sur une image resizee à 0.3, ici x et y sont obtenus à partir d'une image de 0.5
    echelle=180/diametre*0.3/0.5
    
    cap = cv2.VideoCapture(video_a_traiter)
    ret, im = cap.read() #im a pour dimension 1920*1080
    while(ret):
        #print 'video ouverte'
        im = cv2.resize(im,dsize=(0,0),fx=0.5,fy=0.5) #redimensionne à 960*540
        im_seuillee = ft.seuillage(im,hsv)
        [im_c,x,y]=ft.cherche_forme(im_seuillee,im)
                
        lx.append(x*echelle)
        ly.append(y*echelle)        
        
        cv2.imshow('point reconnu',im_c)
        cv2.imshow('image seuillee',im_seuillee)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        ret, im = cap.read() #im a pour dimension 1920*1080
    cap.release()
    cv2.destroyAllWindows()
    ecrit_excel(lx,ly,fic)
    
    
    
    



  
#----------------------------------------------------------------------------------
#MAIN
#-----------------------------------------------------------------------------------

  
#lecture des valeurs de réglages précedentes et stockage dans init
anciennes_v=open("valeurs.txt",'r')
init=[]
for ligne in anciennes_v:
    init.append(int(float(ligne.strip())))
anciennes_v.close()

#lecture video
cap = cv2.VideoCapture(video_a_traiter)
ret, im_base = cap.read() #frame a pour dimension 1920*1080



num_image=1
hsv=[]
#initialisation de hsv
for i in range(6):
    hsv.append(init[i])

#initialisation de diametre
diametre=init[6]

#affichage premiere image
affichage_traitement(im_base,hsv,diametre)



#----------------------------------------------------------------------------------
#mise en place de l'interface graphique
#-----------------------------------------------------------------------------------
fenetre = tk.Tk() #fenetre
fenetre.title('reglages')

# frame1 pour mettre l'image à régler
Frame1 = tk.Frame(fenetre, borderwidth=2)
tk.Label(Frame1, text="Bien ouvrir les 3 fenetres en cliquant sur l'icone ""spyder""").pack()
Frame1.pack(padx=10, pady=10,side=tk.LEFT) #oadx et pad y taille du cadre autour

canvas = tk.Canvas(Frame1, width=80, height=80) #pour decaler le bouton vers le bas
canvas.pack()

Frame_bouton = tk.Frame(Frame1,  borderwidth=2)
Frame_bouton.pack(padx=5, pady=5)
#bouton pour passer à l'image suivante
bouton0=tk.Button(Frame_bouton, text="Passer à l'image suivante", command=passe)
bouton0.pack()
bouton1=tk.Button(Frame_bouton, text="Passer 10 images", command=passe10)
bouton1.pack()
bouton2=tk.Button(Frame_bouton, text="Revenir au debut de la video", command=revient)
bouton2.pack()

canvas2 = tk.Canvas(Frame1, width=80, height=80)
canvas2.pack()
Frame_bouton3 = tk.Frame(Frame1,  borderwidth=2)
Frame_bouton3.pack(padx=5, pady=5)
#texte0=canvas2.create_text(50, 50, text="image n° "+str(num_image), fill="blue")
bouton3=tk.Button(Frame_bouton3, text="Réaliser la reconnaissance", command=traitement_final)
bouton3.pack()

# frame 2 pour mettre les boutons de réglages
Frame2 = tk.Frame(fenetre, borderwidth=2)
Frame2.pack(padx=10, pady=10,side=tk.RIGHT)

# frame 3 dans frame 2
Frame3 = tk.Frame(Frame2,  borderwidth=2)
Frame3.pack(padx=5, pady=5)
Frame4 = tk.Frame(Frame2, borderwidth=2)
Frame4.pack(padx=5, pady=5)
Frame5 = tk.Frame(Frame2, borderwidth=2)
Frame5.pack(padx=5, pady=5)

#ajout de label
tk.Label(Frame3, text="Teinte").pack(padx=10,pady=10)
tk.Label(Frame4, text="Saturation").pack(padx=10, pady=10)
tk.Label(Frame5, text="Luminosité").pack(padx=10,pady=10)



#initialisation de la liste r
r=[0,0,0,0,0,0] #Hmin,Hamx,Smin,Smax,Vmin,Vmax

##curseurs HSV (6 curseurs)
frames=[Frame3,Frame3,Frame4,Frame4,Frame5,Frame5]
for i in range(6):
 r[i]= tk.DoubleVar()
 r[i].set(init[i])
 
 scale = tk.Scale(frames[i], to=255, variable=r[i],command=action)
 if (i%2)==0:
     scale.pack(side=tk.LEFT)
 else:
     scale.pack(side=tk.RIGHT)

# frame 6 dans frame 2
Frame6 = tk.Frame(Frame2,  borderwidth=2)
Frame6.pack(padx=5, pady=5, side=tk.BOTTOM)
tk.Label(Frame6, text="Diamètre grand cercle").pack(padx=10,pady=10)
d=tk.DoubleVar()
d.set(init[6])
scale = tk.Scale(Frame6, to=300, variable=d, orient=tk.HORIZONTAL,command=action)
scale.pack(side=tk.LEFT)


#photo = tk.PhotoImage(file="im.png")
#a = (im_base * 255).round().astype(np.uint64) 
#canvas_image.create_image(0, 0, anchor=tk.NW, image=a)
#cv2.imshow(Frame1,im_base)

#canvas_img_traitee = tk.Canvas(Frame1, width=480, height=270, background='yellow')
#canvas.pack()
#canvas_img_traitee.pack()


fenetre.mainloop() #affichage

cv2.destroyAllWindows()

#enregistrement des valeurs obtenues
f=open("valeurs.txt",'w')
for e in r:
    f.write(str(e.get())+"\n")
f.write(str(d.get())+"\n")
f.close()