from py2duino import *
import time

ar1=Arduino(4)          # déclaration de l'Arduino connecté au COM4 en ar1
R=DigitalOutput(ar1,2)  # LED rouge (R) piloté par le pin digital 2
R.high()                # Mise à l'état haut de la sortie => allumage LED


i=1
while (i<10):
	R.high()
	time.sleep(0.2)   # pause 0,2s
	R.low()
	time.sleep(0.2)   # pause 0,2s
	i+=1



