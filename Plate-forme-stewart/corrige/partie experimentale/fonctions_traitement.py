# -*- coding: utf-8 -*-
"""
Created on Mon Jan 19 22:03:44 2015

@author: Viviane Reydellet
"""
import cv2
import numpy as np

def seuillage(im,hsv):
    '''retravaille l'image im en utilisant les seuils définis dans le tableau "hsv"
    Ce tableau a la forme suivante [hmin,hmax,smin,smax,vmin,vmax]
    L'image retournée est en niveaux de gris.'''
    imghsv=cv2.cvtColor(im,cv2.COLOR_BGR2HSV)	                     # Convert image from RGB to HSV
    
    if hsv[0]<=hsv[1]:
        SEUIL_MIN = np.array([hsv[0], hsv[2], hsv[4]],np.uint8)
        SEUIL_MAX = np.array([hsv[1], hsv[3], hsv[5]],np.uint8)
    
        imgseuillee=cv2.inRange(imghsv,SEUIL_MIN,SEUIL_MAX)

    else: #cas où valeur_max >valeur min : on veut à la fois une plage de couleur en fin et en début (cas du rouge qui est autour de 255) 
        SEUIL_MIN = np.array([hsv[0], hsv[2], hsv[4]],np.uint8)
        SEUIL_MAX = np.array([255, hsv[3], hsv[5]],np.uint8)
        imgseuillee1=cv2.inRange(imghsv,SEUIL_MIN,SEUIL_MAX)
        
        SEUIL_MIN2 = np.array([0, hsv[2], hsv[4]],np.uint8)
        SEUIL_MAX2 = np.array([hsv[1], hsv[3], hsv[5]],np.uint8)
        imgseuillee2=cv2.inRange(imghsv,SEUIL_MIN2,SEUIL_MAX2)

        imgseuillee=cv2.bitwise_or(imgseuillee1,imgseuillee2)
    
    imgseuillee= cv2.erode(imgseuillee,None,iterations=2)
    imgseuillee= cv2.dilate(imgseuillee,None,iterations=2)
 #hchannel=cv2.split(imghsv)[0] 
 
    return imgseuillee
 
 
def cherche_rond(im,imc):
    '''cherche un rond dans l'image im en utilisant la transformée de Hough'''
    #img=cv2.cvtColor(im, cv2.COLOR_BGR2GRAY) 
    i=[0,0,0]
    img = cv2.medianBlur(im,5)
    circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,1.2,20,
                            param1=50,param2=10,minRadius=0,maxRadius=1000)
# plus param2 est grand plus il faut que le cercle ressemble à un cercle
#param1 sert à régler la sensibilité aux niveaux de gris
 
    print "circles=", circles   
   # circles = np.uint16(np.around(circles))
   # imc=cv2.cvtColor(im, cv2.COLOR_GRAY2BGR)     
    if circles is not None:
        #for i in circles[0,:]:
            i=circles[0,:][0]
            # draw the outer circle
            cv2.circle(imc,(i[0],i[1]),i[2],(0,255,0),2)
            # draw the center of the circle
            cv2.circle(imc,(i[0],i[1]),2,(0,0,255),3)
    return imc,i[0],i[1]
    
    
def cherche_forme(a,imc):
 #taille image
 h=len(a) #hauteur 
 l=len(a[0]) #largeur
 gauche=0
 droite=0
 bas=0
 haut=0
 #-----------------------------------------------------------------------------------------
 #parcourt colonne

 s_l=np.sum(a,0) #tableau contenant les sommes des colonnes
 sx=0
 i=0
 #recherche de la première colonne rouge
 while(sx<2 and i<=len(s_l)-1):
     sx=s_l[i]
     i+=1
 gauche=i

 #recherche du premier retour à une colonne sans rouge
 while (sx>2 and i<=len(s_l)-1):
     sx=s_l[i]
     i+=1
 droite=i-1
 #---------------------------------------------------------------------------------------------------------
 #parcourt ligne
 s_L=np.sum(a,1) #tableau contenant les sommes des lignes
 sy=0
 i=0
 #recherche de la première ligne rouge
 while(sy<2 and i<=len(s_L)-1):
     sy=s_L[i]
     i+=1
 haut=i

 #recherche de la première ligne sans rouge
 while(sy>2 and i<=len(s_L)-1):
     sy=s_L[i]
     i+=1
 bas=i-1

 x_centre=int((gauche+droite)/2)
 y_centre=int((haut+bas)/2)
 
 # draw the center of the circle
 cv2.circle(imc,(x_centre,y_centre),2,(255,0,0),3)
 return imc,x_centre,y_centre