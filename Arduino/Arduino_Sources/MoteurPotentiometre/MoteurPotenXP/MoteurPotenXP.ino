int sensorPin = A5;//   // select the input pin for the potentiometer
//int ledPin = 11;      // select the pin for the LED
int sensorValue = 0;  // variable to store the value coming from the sensor
int SortiePwm = 11;
float pwm = 0;
float seuil = 0.;
int ValeurPwm = 0;

void setup() {
  // declare the ledPin as an OUTPUT:
  pinMode(SortiePwm, OUTPUT);  
  Serial.begin(57600);
}

void loop() {
  // read the value from the sensor:
  sensorValue = analogRead(sensorPin);  
  //ValeurPwm = sensorValue / 4;
  seuil = 100.;
  pwm = seuil + ((255.-seuil)* (float) sensorValue)/1023.;
  ValeurPwm = (int) pwm;
  analogWrite(SortiePwm, ValeurPwm); 

  Serial.print("Entree : ");
  Serial.print(sensorValue);

  Serial.print("   PWM : ");
  Serial.print(pwm);

  Serial.println();
  // turn the ledPin on
  //digitalWrite(ledPin, HIGH);  
  // stop the program for <sensorValue> milliseconds:
  //delay(sensorValue);          
  // turn the ledPin off:        
  //digitalWrite(ledPin, LOW);   
  // stop the program for for <sensorValue> milliseconds:
  //delay(sensorValue);
  //Serial.print("A0 "); // en-tete (A0) suivi d'un espace
  //Serial.print(sensorValue); // la valeur
  //Serial.println();
}

