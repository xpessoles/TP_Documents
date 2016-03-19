
# Import du module d'optiomisation 
from scipy.optimize import fsolve
# Import de fonctions mathématiques
from math import cos,sin,pi


# Pas de calcul en degrés :
# =========================
pas_calcul = .5
def systeme(x):
    t1,t2,t3 = x[0],x[1],x[2]
    global t4
    a,b,c,d,e,f = 355,280,280,89.5,160,13
    eq1 = a*cos(t1)+b*cos(t2)*cos(t1)-b*sin(t2)*sin(t1)-c*cos(t4)+d+f*sin(t1)
    eq2 = a*sin(t1)+b*cos(t2)*sin(t1)+b*sin(t2)*cos(t1)-c*sin(t4)+e-f*cos(t1)
    eq3 = t1+t2+t3+t4
    res = [eq1,eq2,eq3]
    return res


# Résolution du système :
# =======================
t4_ini= 223.39*pi/180
t4_fin= 345.02*pi/180

res = []
t4 = t4_ini
sol_ini = [0,0,0]

while t4<=t4_fin :
    t4 = t4 + pas_calcul*pi/180
    res.append(fsolve(systeme,sol_ini))

# Mise en forme des résultats :
# =============================
t1_res = []
t2_res = []
t3_res = []
t4_res = []
for i in range(len(res)):
    t1_res.append(res[i][0]*180/pi)
    t2_res.append(res[i][1]*180/pi)
    t3_res.append(res[i][2]*180/pi)
    t4_res.append(t4_ini*180/pi + i*pas_calcul)

# Affichage des courbes :
# =======================
from scipy import *
from pylab import *
"""
plot(t4_res,t1_res,label="$\\theta_1$")
plot(t4_res,t2_res,label="$\\theta_2$")
plot(t4_res,t3_res,label="$\\theta_3$")
"""
plot(t1_res,t2_res,label="$\\theta_1$")
plot(t1_res,t3_res,label="$\\theta_2$")
plot(t1_res,t4_res,label="$\\theta_3$")

legend()
