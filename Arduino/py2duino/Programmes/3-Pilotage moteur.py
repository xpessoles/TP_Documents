from py2duino import *
import time

ar1=Arduino(4)          # déclaration de l'Arduino connecté au COM4 en ar1

A=DigitalOutput(ar1,7)  # Alimentation de la carte de puissance connecté au pin digital 7
A.high()                # Mise à l'état haut du pin 7 = carte de puissance alimentée

R=DigitalOutput(ar1,5)  # Rotation du moteur piloté par le pin digital 5

S=DigitalOutput(ar1,4)  # Sens de rotation du moteur piloté par le pin digital 4

S.high()
R.high()
time.sleep(5)           # Rotation pendant 5s dans un sens
R.low()
time.sleep(2)           # Pause 2s
S.low()
R.high()
time.sleep(5)           # Rotation pendant 5s dans l'autre sens
R.low()


