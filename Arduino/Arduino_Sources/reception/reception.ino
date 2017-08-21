#include <Servo.h> 
#include <SPI.h>
#include <Mirf.h>
#include <nRF24L01.h>
#include <MirfHardwareSpiDriver.h>

Servo esc1;
int ledPin = 5;  

void setup() {
esc1.attach(7);
pinMode(ledPin, OUTPUT);
  
  Serial.begin(9600);  // pour le debogage
  
  Mirf.cePin = 9; // CE sur D9
  Mirf.csnPin = 10; // CSN sur D10
  Mirf.spi = &MirfHardwareSpi; 
  Mirf.init();

  Mirf.channel = 0; 
  Mirf.payload = 10; 
  Mirf.config(); 
  
  Mirf.setTADDR((byte *)"nrf01"); // Le 2eme module va envoyer ses info au 1er module
  Mirf.setRADDR((byte *)"nrf02"); // On dÃ©finit ici l'adresse du 2eme module
  
}

void loop(){
  
  

  
  int numero1=512;
  int numero2=512;
  int numero3=512;
  int numero4=512;
  byte numero;
  int pairimpair;
  byte data[Mirf.payload]; // Tableau de byte qui va stocker le message recu
  
  if(!Mirf.isSending() && Mirf.dataReady()){ // Si un message a Ã©tÃ© recu et qu'un autre n'est pas en cours d'emission
    
   Mirf.getData(data); // on recupere le message 
  
  // la suite de 4 bytes est convertie en 2 int   
   numero1 = ((long )data[0]) << 8;
   numero1 |= data[1];
   numero2 = ((long )data[2]) << 8;
   numero2 |= data[3];
   numero3 = ((long )data[4]) << 8;
   numero3 |= data[5];
   numero4 = ((long )data[6]) << 8;
   numero4 |= data[7];
    
    
     numero1 = map(numero1, 0, 255, 0, 15);
     numero2 = map(numero2, 0, 255, 0, 15);
     numero3 = map(numero3, 0, 255, 0, 15);
     numero4 = map(numero4, 0, 255, 0, 15);
       
     numero1 = sq(numero1);
     numero2 = sq(numero2);
     numero3 = sq(numero3);
     numero4 = sq(numero4);  
     

esc1.write(numero1);              // tell servo to go to position in variable 'pos' 
    delay(15);  
  
  
  
   // pour debogage, on pourra enlever ensuite:
   Serial.print("Recu les numeros ");    
   Serial.print(numero1,DEC);
   Serial.print(" , ");
   Serial.print(numero2,DEC);
    Serial.print(" , ");
   Serial.print(numero3,DEC);
   Serial.print(" , ");
   Serial.print(numero4,DEC);
   Serial.print(" , ");

   
   

}}
