# -*- coding: utf-8 -*-
"""
Created on Thu Nov 19 10:07:33 2015

@author: Sébastien
"""
#On importe les bibliothèque. la bibliothèque py2duino est renommée duino
import py2duino as duino
import time
import matplotlib.pyplot as plt
import numpy as np

def aquisition_Codeur(com, duree, Te):
#fonction permettant l'acquisition du signal du codeur. Paramètres d'entrées
#numéro du port com, durée de l'acquisition, période d'échantillonage)
#Renvoie une liste de mesures
    ar1 = duino.Arduino(com) #défini le numéro du port com
    codeur= duino.Encoder(ar1, 2, 3, 4) #on récupère les valeurs de l'encodeur au pin2 et 3. 4 est le mode sens+/-
    nbMesures = round(duree / Te) #calcul du nombre de mesure lors de l'acquisition
    i_Mesure = 0 
    mesures = [0] * nbMesures #création d'un tableau de la taille du nombre de mesure
    while i_Mesure < nbMesures: #boucle de mesure
        mesures[i_Mesure] = codeur.read() #complète le tableau avec lecture du codeur
        i_Mesure += 1 #incrémentation du numéro de la mesure
        time.sleep(Te) #pause durée période d'échantillonnage
    ar1.close() #fermeture du port
    return mesures #renvoi du tableau de mesures

def lissage(lst): #fonction lissage
    lst = np.array(lst) #tableau dans variable lst
    return (lst[1:] + lst[:-1])/2 #renvoie la valeur - valeur précédente divisée par 2

def vitesse(lstMesures): #fonction vitesse attend la liste des mesures lissée
    lst = np.array(lstMesures) #tableau dans variable lst
    return lst[1:] - lst[:-1] #renvoie du tableau de vitesse


duree = 5 #durée d'acquisition
Te = 0.1 #période échantillonage
m = aquisition_Codeur(8, duree, Te) #acquisition codeur
t = np.arange(0, duree, Te) #créer un tableau pour le temps (de 0 à durée avec intervalle de Te)
mLisse = lissage(m) #utilise la fonction lissage
plt.plot(t, m, label='mesures') #tracé des mesures en fonction du temps
plt.plot(t[1:], mLisse, label="lissee") #tracé des mesures lissées en fonction du temps
plt.plot(t[2:], vitesse(mLisse), label='vitesse lissée') #tracé de la vitesse lissée en fct du tps
plt.legend(loc='best') #placement de la légende au mieux dans le graphe
plt.show() #éditer le tracé
