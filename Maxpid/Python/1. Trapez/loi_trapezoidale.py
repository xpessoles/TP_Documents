import matplotlib.pyplot as plt


# Version 1 : renvoie uniquement les 4 points utiles
def trapeze1(a1, a2, vmax, tmax):
    t = [0, vmax/a1, tmax+vmax/a2, tmax]
    v = [0, vmax, vmax, 0]
    return t, v


# Version 2 : renvoie nbPoints
def trapeze2(a1, a2, vmax, tmax, nbPoints):
    t = [0] * nbPoints
    v = [0] * nbPoints
    t1 = vmax / a1
    t2 = tmax+vmax/a2
    dt = tmax / (nbPoints - 1)
    for i in range(nbPoints):
        ti = i * dt
        t[i] = ti
        if ti < t1:
            v[i] = a1 * ti
        elif ti < t2:
            v[i] = vmax
        else:
            v[i] = a2 * (ti-tmax)
    return t, v


def lecture(fichier):
    t = []
    v = []
    with open(fichier, 'r') as f:
        for ligne in f:
            ti, vi = [float(val.strip()) for val in ligne.split(';')]
            t.append(ti)
            v.append(vi)
    return t, v

# Par convention, les constantes sont souvent en majuscule
TMAX = 0.4  # durée totale du trapeze
VMAX = 1.1  # vitesse angulaire en rad/s
A1 = 10  # accélération angulaire en rad/s²
A2 = -10  # décélération angulaire en rad/s²
NP = 500  # Nombre de point de calcul

tCom, vCom = trapeze2(A1, A2, VMAX, TMAX, NP)  # ou trapeze1(A1, A2, VMAX, TMAX)
plt.plot(tCom, vCom, label="loi de commande")

tExp, vExp = lecture("mes_exp.csv")
plt.plot(tExp, vExp, label="mesures expérimentales")

plt.grid()
plt.ylabel('vitesse angulaire du bras en rad/s')
plt.xlabel('temps en secondes')
plt.legend()

plt.show()
