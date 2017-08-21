from py2duino import *
import time

ar1=Arduino(4)          # déclaration de l'Arduino connecté au COM4 en ar1
R=DigitalOutput(ar1,2)  # LED rouge (R) piloté par le pin digital 2
R.low()                 # Mise à l'état bas de la sortie => éteindre LED
P=AnalogInput(ar1,0)    # Sortie du potentiomètre sur le pin analog A0 déclaré en entrée

while P.read()<500 :   #boucle d'attente du dépassement de la valeur 500 en sortie du potentiomètre
    time.sleep(1)
    print(P.read())

R.high()   



