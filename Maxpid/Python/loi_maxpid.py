import matplotlib.pyplot as plt
import numpy as np

a=70
b=80
c=80
xinit=70
pas=4
x=np.linspace(90,0,10)
plt.plot(x,360*(np.sqrt(a**2+b**2+c**2+2*c*(a*np.cos(x*np.pi/180)-b*np.sin(x*np.pi/180)))-xinit)/pas)
plt.ylabel('deplacement x')
plt.xlabel('angle bras')

def lecture(fichier):

    f = open(fichier, 'r')
    t = []
    d = []
    for ligne in f:
         champs = ligne.split(',')
         t.append(int(champs[0].strip()))
         d.append(int(champs[1].strip()))
    return t, d
    
t, d = lecture("mesures.csv")   
plt.plot(t,d)
plt.show()