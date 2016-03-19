# X. Pessoles
# Lycée le Martinière - 2016

# Import du module d'optimisation 
from scipy.optimize import fsolve
# Import de fonctions mathématiques
from math import cos,sin,pi

a,b,c,d,e,ffff = 355,280,280,89.5,160,13
global t1

# Définition du système à résoudre pour déterminer la loi ES:
# ============================================================
def systeme(x):
    t2,t3,t4 = x[0],x[1],x[2]
    eq1 = a*cos(t1)+b*cos(t2)*cos(t1)-b*sin(t2)*sin(t1)-c*cos(t4)+d+ffff*sin(t1)
    eq2 = a*sin(t1)+b*cos(t2)*sin(t1)+b*sin(t2)*cos(t1)-c*sin(t4)+e-ffff*cos(t1)
    eq3 = t1+t2+t3-t4
    res = [eq1,eq2,eq3]
    return res


# Résolution du système :
# =======================
pas_calcul = .5 # degrés
t1_ini= -90*pi/180
t1_fin= 0*pi/180

res = []
t1 = t1_ini
sol_ini = [-2,1,-2]

while t1<=t1_fin :
    res.append(fsolve(systeme,sol_ini))
    sol_ini = res[-1]
    t1 = t1 + pas_calcul*pi/180    
    

# Mise en forme des résultats :
# =============================
t1_res = []
t2_res = []
t3_res = []
t4_res = []
for i in range(len(res)):
    """t4_res.append(res[i][2]*180/pi+136.6)
    t2_res.append((res[i][0]*180/pi+90)*-1)
    t3_res.append((res[i][1]*180/pi-44)*(-1))"""
    t4_res.append(res[i][2]*180/pi)
    t2_res.append((res[i][0]*180/pi))
    t3_res.append((res[i][1]*180/pi))
    t1_res.append(t1_ini*180/pi + i*pas_calcul)

# Affichage des courbes :
# =======================
from scipy import *
from pylab import *

plot(t1_res,t2_res,label="$\\theta_2$")
plot(t1_res,t3_res,label="$\\theta_3$")
plot(t1_res,t4_res,label="$\\theta_4$")

 
legend()

