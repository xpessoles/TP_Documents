import matplotlib.pyplot as plt
import numpy as np

g=100
alpha=(20*2*np.pi)/360


def lecture(fichier):

    f = open(fichier, 'r')
    t = []
    
    for ligne in f:
         champs = ligne.split(',')
         t.append(int(champs[0].strip()))
    t=np.array(t)   
    return t
    
t = lecture("loigalet.csv")   
d = g*np.sin(alpha)*t**2/2

plt.plot(t,d)
plt.ylabel('postion y')
plt.xlabel('temps t')
plt.show()