from py2duino import *
import time

ar1=Arduino(4)          # déclaration de l'Arduino connecté au COM4 en ar1
R=DigitalOutput(ar1,7)  # LED rouge (R) piloté par le pin digital 7
R.low()                 # Mise à l'état bas de la sortie => LED éteinte
B=DigitalInput(ar1,2)   # Bouton sur le pin digital 2 déclaré en entrée


while (B.read()!=1) :   # boucle d'attente d'appui sur le bouton poussoir
    time.sleep(1)
    print(B.read())     # contrôle de la valeur renvoyée par le bouton poussoir

R.high()                # Led allumée

time.sleep(2)

while (B.read()!=1) :   # boucle d'attente d'appui sur le bouton poussoir
    time.sleep(1)
    print(B.read())     # contrôle de la valeur renvoyée par le bouton poussoir

R.low()                 # Led éteinte
