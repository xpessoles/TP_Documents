
import matplotlib.pyplot as pl

def lecture(fichier):
    """Renvoie la liste des temps et la liste des valeurs contenues dans le
    fichier CSV."""
    t = []
    a0 = []
    with open(fichier, 'r') as f:
        for ligne in f:
            ti, a0i = [int(val.strip()) for val in ligne.split(';')]
            t.append(ti)
            a0.append(a0i)
    return t, a0

t, a0 = lecture("mesure.csv")
pl.plot(t, a0)
pl.grid()
pl.savefig('figure.png')
pl.show()