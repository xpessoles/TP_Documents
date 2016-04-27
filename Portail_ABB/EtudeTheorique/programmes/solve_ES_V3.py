
# Import du module d'optiomisation 
from scipy.optimize import fsolve
# Import de fonctions mathématiques
from math import cos,sin,pi

# Pas de calcul de la loi entrée sortie (en degrés)
pas_calcul = 4

global t1,t1_ini,t1_fin

t1_ini = -90*pi/180
t1_fin =  0*pi/180
t1 = t1_ini


# Définition du système d'équations 
# =================================
global a,b,c,d,e,ff
a,b,c,d,e,ff = 355,280,280,89.5,160,13

def systeme(x,t1):
    t2,t3,t4 = x[0],x[1],x[2]
    eq1 = a*cos(t1)+b*cos(t2)*cos(t1)-b*sin(t2)*sin(t1)-c*cos(t4)+d+ff*sin(t1)
    eq2 = a*sin(t1)+b*cos(t2)*sin(t1)+b*sin(t2)*cos(t1)-c*sin(t4)+e-ff*cos(t1)
    eq3 = t1+t2+t3-t4
    res = [eq1,eq2,eq3]
    return res


# Résolution du système :
# =======================
def resoudre():
    res = []
    t1 = t1_ini
    sol_ini = [-2,1,-2]  
    while t1<=t1_fin :
        res.append(fsolve(systeme,sol_ini,t1))
        sol_ini = res[-1]
        t1 = t1 + pas_calcul*pi/180    
    t1_res = []
    t2_res = []
    t3_res = []
    t4_res = []
    for i in range(len(res)):
        t4_res.append(res[i][2]*180/pi)
        t2_res.append((res[i][0]*180/pi))
        t3_res.append((res[i][1]*180/pi))
        t1_res.append(t1_ini*180/pi + i*pas_calcul)

    return [t1_res,t2_res,t3_res,t4_res]


# Affichage des courbes :
# =======================
from scipy import *
from pylab import *
t1_res,t2_res,t3_res,t4_res = resoudre()

plot(t1_res,t2_res,label="$\\theta_2$")
plot(t1_res,t3_res,label="$\\theta_3$")
plot(t1_res,t4_res,label="$\\theta_4$")
plt.show()
"""
# Détermination du couple moteur :
# ================================
def Cm(t1_res,t2_res,t3_res,t4_res):
    Cm = []
    F,L = 40,950
    for i in range(len(t3_res)):
        aa = -c*F*L*sin(radians(t3_res[i]))
        bb = a*sin(radians(t2_res[i]))+ff*cos(radians(t2_res[i]))
        Cm.append(aa/bb/1000)
    return Cm
   
#aa = [340,350,360,370]
aa = [355]
for e in aa : 
    a = e
    res = resoudre()
    cm = Cm(res[0],res[1],res[2],res[3])
    #plt.plot(res[0],cm)
"""    