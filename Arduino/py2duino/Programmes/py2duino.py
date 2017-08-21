# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        py2duino
# Purpose:     Programming arduino from python commands
#
# Author:      David Violeau, Alain Caignot
#
# Created:     01/01/2014
# Copyright:   (c) Demosciences 2014
# Licence:     GPL
#-------------------------------------------------------------------------------
import serial
import sys
import time
import struct
import traceback

class Servo():
    #-------------------------------------------------------------------------------
    # Classe Servo pour piloter un servomoteur
    #
    # Les servomoteurs doivent etre definis sur les broches 9 et 10 pour l'instant
    # Il suffit ensuite de definir les numeros des servomoteurs 1 ou 2
    # servo=Servo(monarduino,1)
    #
    # Pour demander au servomoteur de tourner de x degre (de 0 à 180), taper servo.write(x)
    #-------------------------------------------------------------------------------
    def __init__(self,parent,number):
        self.number=number
        self.parent=parent
        if number!=1 and number!=2:
            print("Les servomoteurs doivent etre branches sur les pin digitaux 9 ou 10, taper Servo(monarduino,1 ou 2)")
            self.parent.close()
        else:
            self.attach()
            print("attach ok")
        
    def attach(self):
        mess="Sa"+str(self.number)
        self.parent.ser.write(bytes(mess,"ascii"))
        
    def dettach(self):
        mess="Sd"+str(self.number)
        self.parent.ser.write(bytes(mess,"ascii"))
        print("detach ok")

    def write(self,value):
        if value<0 :
            value=0
        elif value>180:
            value=180
        
        mess="Sw"+str(self.number)+chr(value)
        self.parent.ser.write(bytes(mess,"ISO-8859-1"))


class DigitalOutput():
    #-------------------------------------------------------------------------------
    # Classe DigitalOutput pour mettre à l'état haut ou bas une sortie digitale
    #
    # Vous devez spécifier la carte arduino et le pin digital de sortie souhaité
    # led=DigitalOutput(macarte,9)
    #
    # Pour mettre à l'état haut taper : led.high(), pour l'état bas : led.low()
    #-------------------------------------------------------------------------------

    def __init__(self,parent,pin):
        self.pin=pin
        self.parent=parent
        self.init()
        
    def init(self):
        self.parent.pinMode(self.pin,"OUTPUT")


    def high(self):
        self.parent.digitalWrite(self.pin,1)

    def low(self):
        self.parent.digitalWrite(self.pin,0)

class DigitalInput():
    #-------------------------------------------------------------------------------
    # Classe DigitalInput pour lire la donnée binaire d'un pin digital
    #
    # Vous devez spécifier la carte arduino et le pin digital d'entré souhaité
    # push=DigitalInput(macarte,9)
    #
    # Pour lire la valeur, tapez : push.read(). La valeur obtenue est 0 ou 1 (état haut)
    # La fonction push.upfront() (ou downfront) permet de renvoyer 1 ou 0 sur front montant ou descendant de l'entrée
    #-------------------------------------------------------------------------------
    def __init__(self,parent,pin):
        self.pin=pin
        self.parent=parent
        self.previous_value=0
        self.value=0
        self.init()

    def init(self):
        self.parent.pinMode(self.pin,"INPUT")
        self.value=self.parent.digitalRead(self.pin)
        self.previous_value=self.value
        
    def read(self):
        return self.parent.digitalRead(self.pin)

    def upfront(self):
          self.value=self.parent.digitalRead(self.pin)
          val=0
          if  ((self.value!=self.previous_value) & (self.value==1)):
              val=1
          else :
              val=0
          self.previous_value=self.value
          return val

    def downfront(self):
          self.value=self.parent.digitalRead(self.pin)
          val=0
          if  ((self.value!=self.previous_value) & (self.value==0)):
              val=1
          else :
              val=0
          self.previous_value=self.value
          return val         

class AnalogInput():
    #-------------------------------------------------------------------------------
    # Classe AnalogInput pour lire les données issues d'une voie analogique
    #
    # Vous devez spécifier la carte arduino et le pin analogique d'entrée souhaitée
    # analog=AnalogInput(macarte,0)
    #
    # Pour lire la valeur analogique : analog.read(). La valeur renvoyée est comprise entre 0 et 1023
    #-------------------------------------------------------------------------------
    def __init__(self,parent,pin):
        self.pin=pin
        self.parent=parent
        self.value=0

    def read(self):
        self.value=self.parent.analogRead(self.pin)
        return self.value

class AnalogOutput():
    #-------------------------------------------------------------------------------
    # Classe AnalogOutput pour envoyer une grandeur analogique variant de 0 à 5 V 
    # ce qui correspond de 0 à 255 
    # Vous devez spécifier la carte arduino et le pin Analogique (pwm ~) de sortie souhaité
    # led=AnalogOutput(macarte,9)
    #
    # Utiliser la commande led.write(200)
    #-------------------------------------------------------------------------------
    def __init__(self,parent,pin):
        self.pin=pin
        self.parent=parent
        self.value=0

    def write(self,val):
        if val>255 :
            val=255
        elif val<0:
            val=0
        self.parent.analogWrite(self.pin,val)

class DCmotor():
    #-------------------------------------
    # Classe DCmotor pour le pilotage des moteurs a courant continu
    #
    # Les parametres de definition d'une instance de la classe sont :
    # - la carte arduino selectionnee
    # - le numero du moteur de 1 a 4
    # - le pin du PWM1
    # - le pin de sens ou de PWM2
    # - le type de pilotage : 0 (type L293 avce 2 PWM) ou  1 (type L298 avec un PWM et une direction)
    # Ex : monmoteur=DCmotor(arduino1,1,3,5,0) (moteur 1 pilotage de type L293 avec les PWM des pins 3 et 5
    #
    # Pour faire tourner le moteur a une vitesse donne, taper : monmoteur.write(x) avec x compris entre -255 et 255)
    #-------------------------------------

    def __init__(self,parent,number,pin_pwm,pin_dir,mode):
        self.pin1=pin_pwm
        self.pin2=pin_dir
        self.mode=mode
        self.number=number
        self.parent=parent
        if mode!=0 and mode!=1:
            print("Choisir un mode egal a 0 pour un pilotage par 2 PWM ou 1 pour un pilotage par un PWM et un pin de sens")
        elif number!=1 and number!=2 and number!=3 and number!=4:
            print("Choisir un numero de moteur de 1 a 4")
        else :
            try:
                mess="C"+str(self.number)+chr(48+self.pin1)+chr(48+self.pin2)+str(self.mode)
                self.parent.ser.write(bytes(mess,"ISO-8859-1"))
                tic=time.time()
                toread=self.parent.ser.inWaiting()
                value=""
                while(toread < 2 and time.time()-tic < 1):  # attente retour Arduino
                    toread=self.parent.ser.inWaiting();
                value=self.parent.ser.read(toread);
                if value==b"OK":
                    print("Moteur "+str(self.number)+" correctement connecté")
                else:
                    print("Problème de déclaration et connection au moteur")
                    self.parent.close()
                    return
            except:
                print("Problème de déclaration et connection au moteur")
                self.parent.close()
            
    def write(self,value):
        value=int(value)
        if value<-255:
            value=-255
        elif value>255:
            value=255
        if value<0:
            direction=0
        else:
            direction=1
        mess="M"+str(self.number)+chr(48+direction)+chr(abs(round(value)))
        self.parent.ser.write(bytes(mess,"ISO-8859-1"))


class Encoder():
    #-------------------------------------
    # Classe Encoder pour la lecture d'interruption sur des encodeurs 2 voies
    #
    # Les parametres de definition d'une instance de la classe sont :
    # - la carte arduino selectionnee
    # - le pin de l'entrée digitale de la voie A (avec interruption)
    # - le pin de l'entrée digitale de la voie B (avec ou sans interruption)
    # - le type de lecture : 1 pour front montant de la voie A (et sens donné par la voie B), 2 pour fronts montants et descendants de la voie A seule, 4 pour fronts montants et descendants des deux voies
    #
    # codeur=Encoder(macarte,2,3,1)
    # pour lire le nombre de tops, taper codeur.read(). La valeur obtenue peut etre positive ou négative (codée sur 4 octets)
    # Pour remettre à 0 la valeur lue, codeur.reset()
    #-------------------------------------
    def __init__(self,parent,pinA,pinB,mode):
        self.parent=parent
        self.pinA=pinA
        self.pinB=pinB
        self.mode=mode
        self.corresp=[-1,-1,0,1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,5,4,3,2]
        try:
            if self.corresp[self.pinA]==-1 or self.corresp[self.pinB]==-1:
                print("Les pins utilisés pour l'encodeur doivent accepter les interruptions. Choisir les pins 2,3 (UNO, MEGA) ou 18 à 21 (MEGA)")
                self.parent.close()
        except:
            print("Les pins utilisés pour l'encodeur doivent accepter les interruptions. Choisir les pins 2,3 (UNO, MEGA) ou 18 à 21 (MEGA)")
            self.parent.close()
        if mode!=1 and mode!=2 and mode !=4:
            print(["Choisir un mode pour le codeur egal a : ",
                   "1 : front montant de la voie A, ",
                   "2 : front montant et descendants de la voie A,",
                   "4 : fronts montants et descendants des voies A et B"])
            self.parent.close()
        else :
            if mode==4:
                mess="Ea"+chr(self.corresp[self.pinA])+chr(self.corresp[self.pinB])+str(mode)
            else:
                mess="Ea"+chr(self.corresp[self.pinA])+chr(self.pinB)+str(mode)
            self.parent.ser.write(bytes(mess,"ISO-8859-1"))

    def reset(self):
        mess="Ez"+chr(self.corresp[self.pinA])
        self.parent.ser.write(bytes(mess,"ISO-8859-1"))          

    def read(self):
        mess="Ep"+chr(self.corresp[self.pinA])
        self.parent.ser.write(bytes(mess,"ISO-8859-1"))
        toread=self.parent.ser.inWaiting()
        tic=time.time()
        while(toread < 4 and time.time()-tic < 1):  # attente retour Arduino
            toread=self.parent.ser.inWaiting();
        value=self.parent.ser.read(toread);
        value=struct.unpack('l',value)
        return value[0]
                  
class Arduino():
    #-------------------------------------
    # Classe Arduino pour definition d'une carte arduino
    #
    # Les parametres de definition d'une instance de la classe sont :
    # - le port de communication
    # - le taux de transfert qui doit etre laissé à 115200 (argument optionnel)
    #
    # La connection à la carte est faite automatiquement à la déclaration
    # Taper macarte=Arduino(8) pour se connecter automatiquement à la carte sur le port 8
    # Taper macarte.close() pour fermer la connexion
    #-------------------------------------    
    def __init__(self,com,baudrate=115200):
        self.ser = serial.Serial()
        self.com=com #define com port
        self.baudrate=baudrate #define com debit
        self.digitalPins=[] #list of defined digital pins
        self.analogPins=[]  #list of defined analog pins
        self.interrupts=[]  #list of defined interrupt
        self.connect()


    def connect(self):
        self.ser.baudrate=self.baudrate   #definition du debit
        import os
        if os.name == "posix":
            self.ser.port=self.com
        else:
            self.ser.port=self.com-1
        connect = 0
        try:
            self.ser.open();         #open port
            time.sleep(2);           #wait for stabilisation
            self.ser.write(b"R3");    #send R3 to ask for arduino program
            tic = time.time();

            toread=self.ser.inWaiting();
            while(toread < 2 and time.time()-tic < 2):  # attente retour Arduino
                toread=self.ser.inWaiting();
            value=self.ser.read(toread)
            if value == b"v3":
                print("Connexion ok avec l'arduino")
                connect=1

        finally:
            if connect==0:
                print("Connexion impossible avec l'arduino. Verifier que le com est le bon et que le programme v3.ino est bien chargé dans l'arduino")
                return 0
            else:
                return 1

    def close(self):
        self.ser.close()


    def pinMode(self,pin,type):
        mode='x'
        if type=='OUTPUT':
            mode='1'
        elif type=='INPUT':
            mode='0'
        else:
            print("Attention le type OUTPUT ou INPUT du pin n'est pas bien renseigne")
        if mode != 'x':
            mess="Da"+chr(pin+48)+mode
            #self.ser.write(bytes(mess,"ascii"))
            self.ser.write(bytes(mess,"ISO-8859-1"))
            self.digitalPins.append(pin)

    def digitalwrite(self,pin,value):
        self.digitalWrite(self,pin,value)

    def digitalWrite(self,pin,value):
        try:
            self.digitalPins.index(pin)
            data='x'
            if value=="HIGH":
                data='1'
            elif value=="LOW":
                data='0'
            elif value==1 or value==0:
                data=str(value)
            else:
                print("Valeur incorrecte pour un pin digital")
            if data !='x':
                mess="Dw"+chr(pin+48)+data
                #self.ser.write(bytes(mess,"ascii"))
                self.ser.write(bytes(mess,"ISO-8859-1"))

        except:
            print("Erreur de transmission ou bien le pin digital n'a pas ete bien assigne au prealable avec arduino.pinMode")
            self.close()
            traceback.print_exc(file=sys.stdout)


    def analogwrite(self,pin,value):
        self.analogWrite(self,pin,value)

    def analogWrite(self,pin,value):
        try:
            if abs(value)>255:
                code_sent="W"+chr(pin+48)+chr(255);
            else:
                code_sent="W"+chr(pin+48)+chr(abs(round(value)))
            self.ser.write(bytes(code_sent,"ISO-8859-1"))

        except:
            print("Erreur de transmission")
            self.close()
            #traceback.print_exc(file=sys.stdout)

    def digitalread(self,pin):
        return self.digitalRead(self,pin)

    def digitalRead(self,pin):
        try:
            self.digitalPins.index(pin)
            mess="Dr"+chr(pin+48)
            #self.ser.write(bytes(mess,"ascii"))
            self.ser.write(bytes(mess,"ISO-8859-1"))
            tic=time.time()
            toread=self.ser.inWaiting();
            while(toread < 1 and time.time()-tic < 1):  # attente retour Arduino
                toread=self.ser.inWaiting();
            value=self.ser.read(toread)
            return int(value)
        except:
            print("Erreur de transmission ou bien le pin digital n'a pas ete bien assigne au prealable avec arduino.pinMode")
            self.close()
            #traceback.print_exc(file=sys.stdout)

    def analogread(self,pin):
        return self.analogRead(self,pin)

    def analogRead(self,pin):
        try:
            mess="A"+chr(pin+48)
            #self.ser.write(bytes(mess,"ascii"))
            self.ser.write(bytes(mess,"ISO-8859-1"))
            toread=self.ser.inWaiting()
            tic=time.time()
            while(toread < 2 and time.time()-tic < 1):  # attente retour Arduino
                toread=self.ser.inWaiting();
            value=self.ser.read(toread);
            value=struct.unpack('h',value)
            return value[0]
        except:
            print("Erreur de transmission")
            self.close()
            #traceback.print_exc(file=sys.stdout)

    def Servo(self,pin):
        return Servo(self,pin)

        
