#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>
#include <RF24_config.h>
#include <PCD8544.h>  // Define NOKIA 5110 LCD library

////////////////////////////////////
//For LCD Nokia 5110
static const byte glyph[] = { B00010000, B00110100, B00110000, B00110100, B00010000 };
static PCD8544 lcd;
////////////////////////////////////

RF24 radio(8,10);    // define radio pin, this case mean CE -> 8(Green) & CSI -> 10(Yellow) 
const uint64_t pipe = 0xE8E8F0F0E1LL;    // define pipe of signal, ardresse of pipe
byte data_1[3];      // data receive from transmitter. "humidity" and "Temperature"

void setup(void)
{
  lcd.begin(84, 48);          // PCD8544-compatible displays may have a different resolution...
  lcd.createChar(0, glyph);   // Add the smiley to position "0" of the ASCII table...
  
//  Serial.begin(9600);
  radio.begin();  // Start up radio of NRF24
  radio.openReadingPipe(1,pipe);  // open a pipe for read a radio
  radio.startListening();  // start listening all data transmitted by client
  
  pinMode(1,OUTPUT);
}

void loop()   
{
  if ( radio.available() )
  {
     bool done = false;  // define done in boolin type for a loop while
     digitalWrite(2,HIGH);
    while (!done)  // not done
    {
      done = radio.read( data_1, sizeof(data_1) );

// Display on LCD Nokia      
      lcd.setCursor(0, 0);          // Set cursor of LCD on first line
        lcd.print("MenuTuto \n");   // Print or display "MenuTuto" on first line of LCD
      lcd.setCursor(0, 1);          // Set cursor of LCD on second line for temperature's data
        lcd.print("T is:\n");
        lcd.print(data_1[0]);
        lcd.print(" C");
      lcd.setCursor(0, 2);          // Set cursor of LCD on thirt line for humidity's data
        lcd.print("H is:\n");
        lcd.print(data_1[1]);
        lcd.print(" %");
        
      delay(10);
    }
  }
  digitalWrite(2,LOW);
}
