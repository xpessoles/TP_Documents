# -*- coding: utf-8 -*-
"""
Created on Sat Nov 21 16:08:09 2015

@author: Remi
"""
import matplotlib.pyplot as plt
import numpy as np

g=9.81
alpha=(20*2*np.pi)/360
m=22.572
Fv=15
T=56.2

def lecture(fichier):

    f = open(fichier, 'r')
    t = []
    d = []
    for ligne in f:
         champs = ligne.split(';')
         t.append(float(champs[0].strip()))
         d.append(float(champs[1].strip()))
    t=np.array(t) 
    d=np.array(d)     
    return t, d
    
t, d = lecture("Classeur1.csv")  

e = -(((m*g*np.sin(alpha)-T)/(Fv**2))*(m*np.exp(-Fv*t/m)-m+Fv*t))

plt.plot(t,d)

plt.plot(t,e)

plt.ylabel('postion y')
plt.xlabel('temps t')
plt.show()