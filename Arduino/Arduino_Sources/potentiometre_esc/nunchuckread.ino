/*
 * NunchuckPrint
 *
 * 2007 Tod E. Kurt, http://todbot.com/blog/
 *
 * The Wii Nunchuck reading code is taken from Windmeadow Labs
 *   http://www.windmeadow.com/node/42
 */
 
#include <Wire.h>
#include <Servo.h>
 
Servo esc;
int throttlePin = 0;


void setup()
{
  Serial.begin(19200);
  esc.attach(4);
  Serial.print ("Finished setup\n");
}

void loop()
{
  int sensorValue = analogRead(A0);
  sensorValue=map(sensorValue, 0, 1023, 0, 179);
  esc.write(sensorValue);
  //delay(100);
}



