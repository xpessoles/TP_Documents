# -*- coding: utf-8 -*-
"""
Created on Sat Nov 21 16:08:09 2015

@author: Remi
"""
import matplotlib.pyplot as plt
import numpy as np

g=10
alpha=(20*2*np.pi)/360

def lecture(fichier):

    f = open(fichier, 'r')
    t = []
    d = []
    for ligne in f:
         champs = ligne.split(';')
         t.append(int(champs[0].strip()))
         d.append(int(champs[1].strip()))
    t=np.array(t) 
    d=np.array(d)     
    return t, d
    
t, d = lecture("essai.csv")  

e = g*np.sin(alpha)*t**2/2 

plt.plot(t,d)

plt.plot(t,e)

plt.ylabel('postion y')
plt.xlabel('temps t')
plt.show()