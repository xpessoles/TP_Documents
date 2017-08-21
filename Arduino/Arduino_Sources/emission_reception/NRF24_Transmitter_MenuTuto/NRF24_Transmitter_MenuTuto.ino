#include <SPI.h>
#include <nRF24L01.h>      // define NRF24L01's library (download from référence) 
#include <RF24.h>
#include <RF24_config.h>

RF24 radio(9,10);           // Define radio pin RF24 radio(CE,CSN), this case mean CE -> 8 & CSN -> 10. Hope it's a best choice. Or your can change like you want
const uint64_t pipe = 0xE8E8F0F0E1LL;


void setup(void)
{
  Serial.begin(9600);      // Setup serial monitor'rate to 9600. Defaut setting 
  delay(300);              // Delay 0.3s before next step
  
  radio.begin();           // Turn on RF24L01
  radio.openWritingPipe(pipe);
  radio.openReadingPipe(1,pipe);
  
  Serial.println("Humidity and temperature\n\n");  // Display "Humidity and temperature\n\n" Arduino Serial Monitor (Tools --> Serial Monitor)
  delay(700);
}
  
void loop(void)
{
 
// Setting up serial monotor display:
  Serial.print("Current humidity = ");
  Serial.print(DHT.humidity);
  Serial.print(" %  ");
  Serial.print("temperature = ");
  Serial.print(DHT.temperature); 
  Serial.println(" C  ");
  Serial.print(" --> sending : ");
  
  radio.write(data_1,sizeof(data_1));  // Radio sending's command
 
  Serial.print(" --> succesful\n");
  
  delay(400);
  
  radio.powerDown();  // Save power by powerdown mode
  delay(500);
  radio.powerUp();    // Turn back to online's mode
}
