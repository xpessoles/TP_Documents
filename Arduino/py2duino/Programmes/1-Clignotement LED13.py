from py2duino import *
import time

ar1=Arduino(9)
ar1.pinMode(13,'OUTPUT')

i=5
while (i<10):
	ar1.digitalWrite(13,"HIGH")
	time.sleep(1)   #pause 1s
	ar1.digitalWrite(13,"LOW")
	time.sleep(1)   #pause 1s
	i+=1



