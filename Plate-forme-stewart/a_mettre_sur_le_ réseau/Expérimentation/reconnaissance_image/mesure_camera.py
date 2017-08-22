# -*- coding: utf-8 -*-
"""
Created on Sat Apr 18 18:36:07 2015

@author: Viviane Reydellet
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 13:42:45 2015

@author: Viviane Reydellet
"""
#!/usr/bin/python


import ConfigParser
import csv

import cv2
from gi.repository import Gtk as gtk, Gdk
from gi.repository import GLib, GObject

import cairo

import numpy as np
import time
import threading
import serial


global hsv
global cap
global im_lue





#INTERFACE
class int_reconnaissance:
    
    def __init__(self):
        global interface,interf
               
        interface = gtk.Builder()
        interface.add_from_file('interface_TP.glade')
        
        interface.connect_signals(self)
        #interface.connect_signals({'quitter' : quitter, 'changerTexte' : self.changerTexte})
        self.barreHmin = interface.get_object("vscaleHmin")
        self.barreHmax = interface.get_object("vscaleHmax")
        self.barreSmin = interface.get_object("vscaleSmin")
        self.barreSmax = interface.get_object("vscaleSmax")
        self.barreVmin = interface.get_object("vscaleVmin")
        self.barreLum = interface.get_object("vscaleLum")
        self.barreCont = interface.get_object("vscaleCont")
        self.barreVmax = interface.get_object("vscaleVmax")
        self.barreEchelle=interface.get_object("scale_echelle")
        self.dessinH = interface.get_object("drawingareaH")
        self.dessinS = interface.get_object("drawingareaS")
        self.dessinV = interface.get_object("drawingareaV")
       
        self.dessin1 = interface.get_object("drawingarea1b")
        self.dessin2 = interface.get_object("drawingarea2b")
        self.dessinP = interface.get_object("drawingarea_progres")
              
        self.regl_duree=interface.get_object("temps")
        self.regl_duree.set_value(10)
        
        self.fen_regl = interface.get_object("fen_regl")
        self.fen_rec= interface.get_object("fenetre_reconnaissance")   
         
        self.fen_attendre=interface.get_object("attendre")
        self.fen_pb_camera=interface.get_object("probleme_camera")
        self.doc_ouvert=interface.get_object("document_ouvert")
        self.progressbar=interface.get_object("progressbar1")
        #CREATION DES IMAGES ASSOCIEES AUX BARRES DE DEFILEMENT
        [self.Himg,self.Vimg]=creation_images_barres()        
    
        #creation du pixmap pour la barre de progression
        #self.pixmapP = creation_pixmap(self.dessinP)
        #r=self.dessinP.get_allocation()
        #self.Pimg = np.zeros((r.height,r.width,3), np.uint8)
        #self.Pimg[:,:]=[0,0,220]
               
        #self.pixmapP=change_im_sur_surface(self.Pimg,self.pixmapP,self.dessinP)
        
        self.fen_rec.show()
       
        #creation des pixmaps associés aux 2 zones de dessin image brute et image seuillee       
        self.pixmap1=creation_pixmap(self.dessin1)
        self.pixmap2=creation_pixmap(self.dessin2)
        if ret==True:
            x,y,imc,ims=traitement_im(im_lue,hsv,diametre)
        else:
            x,y,imc,ims= 0,0,np.zeros((288,384,3), np.uint8),np.zeros((288,384,3), np.uint8)
        
        self.pixmap1=change_im_sur_surface(imc,self.pixmap1,self.dessin1)
        self.pixmap2=change_im_sur_surface(ims,self.pixmap2,self.dessin2) 
         
        self.pipette=0
        self.fen_regl.connect('delete-event', lambda w, e: w.hide() or True)
        
    def change_scale(self,j,widget):
            '''fonction executée lors de l'action sur une barre de défilement H,S,V'''
            
            hsv[j]=int(widget.get_value())
            if ret: #capture video fonctionne
                x,y,imc,ims=traitement_im(im_lue,hsv,diametre)
            else:
                x,y,imc,ims= 0,0,np.zeros((288,384,3), np.uint8),np.zeros((288,384,3), np.uint8)
            self.Himg,self.Vimg,Himg2,Vimg2=modif_images_barres(hsv, self.Himg, self.Vimg)
                       
            interf.pixmapH=change_im_sur_surface(Himg2,interf.pixmapH,self.dessinH)
            interf.pixmapV=change_im_sur_surface(Vimg2,interf.pixmapV,self.dessinV)
            interf.pixmap1=change_im_sur_surface(imc,interf.pixmap1,self.dessin1)
            interf.pixmap2=change_im_sur_surface(ims,interf.pixmap2,self.dessin2)            
           
    def on_cap_clicked(self,widget):
        global im_lue        
        #global Himg
        ret, im_lue = cap.read() 
        ret, im_lue = cap.read()
        #print(cap.get(cv2.CAP_PROP_BRIGHTNESS),cap.get(cv2.CAP_PROP_CONTRAST)) 
        if ret:
            x,y,imc,ims=traitement_im(im_lue,hsv,diametre)
            interf.pixmap1=change_im_sur_surface(imc,interf.pixmap1,interf.dessin1)
            interf.pixmap2=change_im_sur_surface(ims,interf.pixmap2,interf.dessin2)
        else:
            interf.fen_pb_camera.show()            
          
              
    def on_regl_clicked(self,widget): 
        self.fen_regl.show_all()
        self.barreHmin.set_value(hsv[0])
        self.barreHmax.set_value(hsv[1])
        self.barreSmin.set_value(hsv[2])
        self.barreSmax.set_value(hsv[3])
        self.barreVmin.set_value(hsv[4])
        self.barreVmax.set_value(hsv[5])
        self.barreLum.set_value(int(LumCont[0]*100/255))
        self.barreCont.set_value(int(LumCont[1]*100/20))
              
        #HimgBGR=np.array(self.Himg) #copie indépendante de Himg
        #HimgBGR=cv2.cvtColor(HimgBGR,cv2.COLOR_HSV2BGR)
        #affiche_im_sur_display(HimgBGR,self.pixmapH)
    
    def on_quitte_clicked(self,widget):
        '''au clic sur le bouton quitter de la fenetre réglage'''
        self.fen_regl.hide()        
    
    def on_scale_echelle_value_changed(self, widget):
        global diametre
        diametre=int(widget.get_value())                    
        x,y,imc,ims=traitement_im(im_lue,hsv,diametre)
        interf.pixmap1=change_im_sur_surface(imc,interf.pixmap1,interf.dessin1)
        
    def on_vscaleHmin_value_changed(self, widget):
        self.change_scale(0,widget)         
    def on_vscaleHmax_value_changed(self, widget):                      
        self.change_scale(1,widget) 
        
    def on_vscaleSmin_value_changed(self, widget):                    
        self.change_scale(2,widget)
    def on_vscaleSmax_value_changed(self, widget):        
        self.change_scale(3,widget)
    def on_vscaleVmin_value_changed(self, widget):         
        self.change_scale(4,widget)
    def on_vscaleVmax_value_changed(self, widget):         
        self.change_scale(5,widget)
            
    def on_vscaleLum_value_changed(self, widget):
        global im_lue
        LumCont[0]=int(widget.get_value()*255/100)
        cap.set(cv2.CAP_PROP_BRIGHTNESS,LumCont[0])
        ret, im_lue = cap.read()
        if ret:
            x,y,imc,ims=traitement_im(im_lue,hsv,diametre)
            interf.pixmap1=change_im_sur_surface(imc,interf.pixmap1,interf.dessin1)
            interf.pixmap2=change_im_sur_surface(ims,interf.pixmap2,interf.dessin2)
        else:
            interf.fen_pb_camera.show()
            
    def on_vscaleCont_value_changed(self, widget):
        global im_lue         
        LumCont[1]=int(widget.get_value()*20/100)
        cap.set(cv2.CAP_PROP_CONTRAST,LumCont[1])
        ret, im_lue = cap.read() 
        if ret:
            x,y,imc,ims=traitement_im(im_lue,hsv,diametre)
            interf.pixmap1=change_im_sur_surface(imc,interf.pixmap1,interf.dessin1)
            interf.pixmap2=change_im_sur_surface(ims,interf.pixmap2,interf.dessin2)
        else:
            interf.fen_pb_camera.show()
    def on_LumContDefaut_clicked(self,widget):
        self.barreLum.set_value(int(LumCont0[0]))
        self.barreCont.set_value(int(LumCont0[1]))
        ret, im_lue = cap.read() 
        if ret:
            x,y,imc,ims=traitement_im(im_lue,hsv,diametre)
            interf.pixmap1=change_im_sur_surface(imc,interf.pixmap1,interf.dessin1)
            interf.pixmap2=change_im_sur_surface(ims,interf.pixmap2,interf.dessin2)
        else:
            interf.fen_pb_camera.show()
    def on_drawingareaH_configure_event(self,widget,event):
        interf.pixmapH = cairo.ImageSurface(cairo.FORMAT_RGB24, 26, 295)
        interf.pixmapH = change_im_sur_surface(self.Himg,interf.pixmapH,interf.dessinH)
    
    def on_drawingareaV_configure_event(self,widget,event):
        interf.pixmapV = cairo.ImageSurface(cairo.FORMAT_RGB24, 26, 295)
        interf.pixmapV = change_im_sur_surface(self.Vimg,interf.pixmapV,interf.dessinV)
#    def on_drawingarea_progres_configure_event(self,widget,event):
#        #interf.pixmapP = cairo.ImageSurface(cairo.FORMAT_RGB24, 26, 295)
#        interf.pixmapP = change_im_sur_surface(self.Pimg,interf.pixmapP,interf.dessinP)
               
          
    #traçage des pixmaps sur chacune des drawingarea 
    def on_drawingarea1b_draw(self,windows,cr):
        cr.set_source_surface(interf.pixmap1,0,0)
        cr.paint()
        return False
    def on_drawingarea2b_draw(self,windows,cr):
        cr.set_source_surface(interf.pixmap2,0,0)
        cr.paint()
        return False
    def on_drawingareaH_draw(self,windows,cr):
        cr.set_source_surface(interf.pixmapH,0,0)
        cr.paint()
        return False
   
    def on_drawingareaV_draw(self,windows,cr):
        cr.set_source_surface(interf.pixmapV,0,0)
        cr.paint()
        return False
    def on_drawingareaCible_draw(self,windows,cr):
        global x_cible, y_cible
        cr.set_source_surface(interf.pixmapC,0,0)
        cr.paint()
        self.ctC=cr #sauve le contexte pour pouvoir l'utiliser dans le threading
        return False
#    def on_drawingarea_progres_draw(self,windows,cr):
#        cr.set_source_surface(interf.pixmapP,0,0)
#        cr.paint()
#        return False
        
# à traiter
    def on_fenetre_reconnaissance_show(self, widget, event):
        time.sleep(2)
        self.on_cap_clicked(widget)
        print("hello")
    def on_fenetre_reconnaissance_activate_default(self, widget, event):
        time.sleep(2)
        self.on_cap_clicked(widget)
        print("hello2")
  
    def on_fenetre_reconnaissance_map (self, widget, event):
        self.on_cap_clicked(widget)
        
    def on_fenetre_reconnaissance_destroy(self, widget):
        self.fen_regl.hide()
        self.fen_attendre.hide()
        gtk.main_quit()
  
    def on_OK_clicked(self,widget):
        self.fen_info.hide()
   
    def on_depart_suivi_clicked(self,widget):
        mesure()
    
    def clic_souris_dessin1(self,widget,event):
        '''clic dans la zone de dessin après avoir selectionné pipette'''
        if (event.button == 1) and (interf.pipette==1) and event.x<384 and event.x>0 and event.y >0 and event.y<288:
            im=redimensionne(im_lue)
            im=cv2.cvtColor(im,cv2.COLOR_BGR2HSV)	 
            [h,s,v]=im[event.y,event.x]
            interf.pipette=0
            self.barreHmin.set_value((h-20)%180)
            self.barreHmax.set_value((h+20)%180)
            self.barreSmin.set_value(100)
            self.barreSmax.set_value(255)
            self.barreVmin.set_value(80)
            self.barreVmax.set_value(255)
            cursor_normal = Gdk.Cursor(Gdk.CursorType.ARROW)
            self.fen_rec.get_window().set_cursor(cursor_normal)
            self.fen_regl.get_window().set_cursor(cursor_normal)
            
    def on_pipette_clicked(self,widget):
       '''clic sur le bouton pipette'''
       interf.pipette=1
       cursor_special = Gdk.Cursor(Gdk.CursorType.PLUS)
       self.fen_rec.get_window().set_cursor(cursor_special)
       self.fen_regl.get_window().set_cursor(cursor_special)
#boutons amenant à quitter l'interface        
    def on_Retour_clicked(self,widget): #sortie par le bouton annuler
        self.fen_rec.hide()
        gtk.main_quit()
        
    def on_quit_clicked(self,widget): #sortie par le bouton "quitter"
        self.fen_rec.hide()
        self.fen_regl.hide()
        gtk.main_quit()
        
    def on_quit_camera_clicked(self,widget): #bouton suite à la fenetre "la capture video ne fonction pas. Vérifier le branchement de la caméra..."
        self.fen_rec.hide()
        self.fen_regl.hide()
        self.fen_pb_camera.hide()
        gtk.main_quit()
        
     
        
#FONCTIONS DE TRAITEMENT D'IMAGE
#----------------------------------------------------------------------

def seuillage(imghsv,hsv):
    '''retravaille l'image im au format HSV en utilisant les seuils définis dans le tableau "hsv"
    Ce tableau a la forme suivante [hmin,hmax,smin,smax,vmin,vmax]
    L'image retournée est en niveaux de gris.'''
        
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
    
    imgseuillee= cv2.erode(imgseuillee,None,iterations=5)
    imgseuillee= cv2.dilate(imgseuillee,None,iterations=5)
 
    return imgseuillee
 
 
def cherche_centre(im):
    '''détermine le centre de gravité  de manière classique, utilisation des fonctions numpy pour réaliser la somme
    im est l'image traitée (seuillée)'''
         
    h=len(im)
    l=len(im[0])
    s=0
    
    #recherche de xg
    sL=np.sum(im,0) #tableau contenant les sommes des lignes pour chaque colonne
    nC=np.arange(l) #tableau contenant les indexs des colonnes
    pos_p=sL*nC #tableau contenant les positions pondérées
    s=(np.sum(sL,0))#somme de tous les pixels blancs  
    
    if s>0:
        xg=np.sum(pos_p,0)/(np.sum(sL,0))
    
        #recherche de yg
        sC=np.sum(im,1) #tableau contenant les sommes des colonnes pour chaque ligne
        nL=np.arange(h) #tableau contenant les indexs des lignes
        pos_p=sC*nL #tableau contenant les positions pondérées
        yg=np.sum(pos_p,0)/s
    else: #si l'image est complétement noire, on place le cdg au centre de l'image
        xg=l/2
        yg=h/2
        
    return int(xg),int(yg)



##-------------------------------------------------------------------
##-FONCTIONS ASSOcIEES AU MODULE DE REGLAGE

def creation_images_barres():
    '''crée les images le long des barres de défilement H, S et V'''
    g=236
    Himg = np.zeros((295,26,3), np.uint8)
    Himg[:,0:3]=[0,0,g]
    Himg[:,23:26]=[0,0,g]
    Himg[0:21,3:23]=[0,240,240]
    Himg[200:221,3:23]=[180,240,240]
    Himg[0:21,3:23]=[0,0,g]
    Himg[275:296,3:23]=[0,0,g]
    for i in range(21,275):
        Himg[i,3:23]=[(i-21)*180/255,240,240]  
        
    if hsv[0]<=hsv[1]:
        hmoy=(hsv[0]+hsv[1])/2
    else:
        hmoy=((hsv[0]+hsv[1]+180)/2)%180
    
    Vimg = np.zeros((280,280,3), np.uint8)
    Vimg[:,0:15]=[0,0,g]
    Vimg[:,270:280]=[0,0,g]
    Vimg[0:15,:]=[0,0,g]
    Vimg[270:280,:]=[0,0,g]
    for i in range(15,271):
        for j in range(15,271):
            Vimg[i,j]=[hmoy,i-15,j-15]
    return(Himg,Vimg)

def creation_pixmap(dessin):
    '''crée un pixmap (surface cairo) de taille adaptée à la "drawingarea" desssin'''
    
    format=cairo.FORMAT_RGB24
    r = dessin.get_allocation()
    pixmap = cairo.ImageSurface(format, r.width, r.height)
    return(pixmap)
    


def change_im_sur_surface(im,surface,dessin):
    '''place une image im au format HSV sur une surface cairo, puis l'affiche sur la drawingarea dessin'''
    im=cv2.cvtColor(im,cv2.COLOR_HSV2BGR)
    im=cv2.cvtColor(im,cv2.COLOR_BGR2BGRA)
    [h,l,p]=im.shape
    format=cairo.FORMAT_RGB24
    stride = cairo.ImageSurface.format_stride_for_width (format, l)
    surface = cairo.ImageSurface.create_for_data (im, format, l, h, stride)
    #GLib.idle_add(des, dessin)
    dessin.queue_draw()
 
    return(surface)
    
    
def change_imRGB_sur_surface(im,surface,dessin):
    '''place une image im au format RGB sur une surface cairo, puis l'affiche sur la drawingarea dessin'''
    im=cv2.cvtColor(im,cv2.COLOR_RGB2BGR)
    im=cv2.cvtColor(im,cv2.COLOR_BGR2BGRA)
    [h,l,p]=im.shape
    format=cairo.FORMAT_RGB24
    stride = cairo.ImageSurface.format_stride_for_width (format, l)
    surface = cairo.ImageSurface.create_for_data (im, format, l, h, stride)
    dessin.queue_draw()
   
    return(surface)


#def draw_on_area (dessin,pixmap):
#    '''dessine le contenu de pixmap sur dessin'''
#    cr=cairo.Context(pixmap)
#    cr.set_source_surface(pixmap, 0, 0)
#    cr.paint()
#    dessin.queue_draw()


def modif_images_barres(hsv,Himg,Vimg):
    '''modifie les images le long des barres de défilement S et V en fonction des nouveaux paramètres hsv'''
    #global Himg, Vimg
    
    #MODIF DES COULEURS DES BARRES S et V        
    if hsv[0]<=hsv[1]:
        hmoy=(hsv[0]+hsv[1])/2
    else:
        hmoy=((hsv[0]+hsv[1]+180)/2)%180
    
     
    for i in range(15,271):
        for j in range(15,271):
             Vimg[i,j]=[hmoy,i-15,j-15]
   
    #TRACE DES 3 RECTANGLES
    Himg2,Vimg2=np.array(Himg),np.array(Vimg)
    if hsv[0]<=hsv[1]:   
        cv2.rectangle(Himg2, (1,hsv[0]*255/180+20), (24,hsv[1]*255/180+20), 1, thickness=3)
    else:
        cv2.rectangle(Himg2, (1,hsv[0]*255/180+20), (24,275), 1, thickness=3)
        cv2.rectangle(Himg2, (1,20), (24,hsv[1]*255/180+20), 1, thickness=3)
    
    cv2.rectangle(Vimg2, (hsv[4]+15,hsv[2]+15), (hsv[5]+18,hsv[3]+18), 1, thickness=3)
    
    return(Himg,Vimg,Himg2,Vimg2)
    

def redimensionne(im_lue):
    '''redimensionne l'image à la taille de la zone dessin1, pour la mettre dans la zone de dessin dessin1b'''
    im = np.array(im_lue) #copie indépendante de im_lue
    coef=min(384./im.shape[1],288./im.shape[0]) 
    im=cv2.resize(im,dsize=(0,0),fx=coef,fy=coef)
    return(im)

def traitement_im(im_b,hsv,diametre):
    '''resize et seuille l'image, renvoie les 2 images : image seuillée et image de base avec le centre marqué aux dimensions de la zone de dessin'''
    
    im_b = cv2.resize(im_b,dsize=(0,0),fx=0.8,fy=0.8) #redimensionne à 80%
    im_b=cv2.cvtColor(im_b,cv2.COLOR_BGR2HSV)	  # Convert image from BGR to HSV    
    im_seuil = seuillage(im_b,hsv)
    [xc,yc]=cherche_centre(im_seuil)
   
    cv2.circle(im_b,(xc,yc),2,(255,0,0),3) # affiche le point repéré sur l'image
    cv2.circle(im_b,(xc,yc),12,(100,255,255),1) #affiche un cercle autour
    cv2.circle(im_b,(xc,yc),int(diametre/2),(255,255,255),1) #affiche le cercle de reglage de l'échelle
    #im_c=cv2.cvtColor(im_c,cv2.COLOR_BGR2HSV)
    im_b=redimensionne(im_b)   #resize l'image pour l'affichage sur la zone de dessin à 384*288
    im_seuil=redimensionne(im_seuil)
    im_seuil=cv2.cvtColor(im_seuil,cv2.COLOR_GRAY2RGB)
    im_seuil=cv2.cvtColor(im_seuil,cv2.COLOR_RGB2HSV)
     
    return(xc,yc,im_b,im_seuil)

                
def mesure():
    '''realise la mesure'''
    global Lres, im_lue 

   
    ret, im = cap.read() #premiere image lue
    if ret:
        im=redimensionne(im)
        (hautIm,largIm,pim)=im.shape
    else:
        interf.fen_pb_camera.show()
        while gtk.events_pending():
         gtk.main_iteration()
    #initialisation liste de stockage des résultats Lres[i]=[temps,x,y]
    Lres=[]
    
    t0=time.clock()
    t=0
    t1=t0    
       
    ret, im_b = cap.read()
    duree=interf.regl_duree.get_value()
    while (t<duree) and ret:
        
        L=[0.]*3 #liste temporaire pour stockage resultats
        t=time.clock()-t0  #temps ecoule depuis le début de la mesure 
              
        #stockage du temps      
        L[0]=t
       
        #traitement image et affichage
        [x,y,imc,ims]=traitement_im(im_b,hsv,diametre) #traitement de l'image x,y, : position du point reconnu
        interf.pixmap1=change_im_sur_surface(imc,interf.pixmap1,interf.dessin1)
        interf.pixmap2=change_im_sur_surface(ims,interf.pixmap2,interf.dessin2) 
        #-interf.pixmapP=change_im_sur_surface(interf.Pimg,interf.pixmapP,interf.dessinP)
         
        #stockage des resultats dans L
        L[1]=x #positions detectees
        L[2]=y       
       
        Lres.append(L)
        ret, im_b = cap.read()
        
        interf.progressbar.set_fraction(t/duree)
#        print("event",gtk.events_pending)
        while gtk.events_pending():
           gtk.main_iteration()
        #time.sleep(0.001)
    im_lue=im_b
  
    
    test=True
    while(test):
     try:        
        fres=open("resultats.csv", "wb")
        test=False
     except:
        
        interf.fen_attendre.show()
        while gtk.events_pending():
           gtk.main_iteration()
       # print 'Fermer le fichier resultats.csv qui est utilise par une autre application\n'
       # a=raw_input( 'Appuyer sur sur une touche pour poursuivre...\n')        
        
    c = csv.writer(fres,delimiter=';')
    c.writerow(["Nombre de points: ",len(Lres)])
    c.writerow(["Temps(s)","x(pixels)","y(pixels)"])
    c.writerows(Lres)
    fres.close()        
        

   
 
#-------------------------------------------
#MAIN


#lecture du fichier d'initialistation
try:
    config = ConfigParser.ConfigParser()
    config.readfp(open("ParametresVideo.ini"))
except:
    print("La lecture du fichier ParametresVideo.ini a échoué") 

try:
    hsv=[]
    LumCont=[]
        
    #lecture de h,s,v
    options=["Hmin","Hmax","Smin","Smax","Vmin","Vmax"]
    for option in options: 
        hsv.append(config.getint("valeurs_hsv", option))
    #Lecture de luminosité constraste    
    LumCont=[config.getint("valeurs_hsv", "Luminosite"),config.getint("valeurs_hsv", "Contraste")]
    diametre=0 #initialisation du diatre pour reglage echelle
     
finally:
    if len(hsv)!=6:#si jamais le fichier init n'a pas été rempli correctement
       hsv=[0,100,0,255,0,255]
    if len(LumCont)!=2:#si jamais le fichier init n'a pas été rempli correctement
       LumCont=[100,60]
   
    LumCont0=[0,60]

    #ouverture capturevideo      
    cap = cv2.VideoCapture(0)
    #♠LumCont0[0]=cap.get(cv2.CAP_PROP_BRIGHTNESS) #valeurs par defaut de luminosité contraste
    #LumCont0[1]=cap.get(cv2.CAP_PROP_CONTRAST)

    ret, im_lue = cap.read() #premiere image lue
    if ret==True:
        im=redimensionne(im_lue)
        (hautIm,largIm,pim)=im.shape
    else:
        print("echec lecture video")          

    
    try:
        if __name__ == "__main__":
            interf=int_reconnaissance()
            gtk.main()


    finally:
        cap.release()
        print("oK")
 
        #enregistrement des paramètres utilisateur
        config = ConfigParser.SafeConfigParser()
        config.read("ParametresVideo.ini")
        #valeurs HSV reglees
        if not config.has_section("valeurs_hsv"):
            config.add_section("valeurs_hsv")
            options=["Hmin","Hmax","Smin","Smax","Vmin","Vmax"]
        i=0
        for option in options: 
            config.set("valeurs_hsv", option, str(hsv[i]))
            i+=1
        #luminosité contraste
        config.set("valeurs_hsv", "Luminosite", str(LumCont[0]))
        config.set("valeurs_hsv", "Contraste", str(LumCont[1]))
         
        fp = open("ParametresVideo.ini", 'w')
        config.write(fp)
        fp.close()
 