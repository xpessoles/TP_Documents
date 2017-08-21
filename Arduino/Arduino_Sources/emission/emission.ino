#include <SPI.h>
//#include <Mirf.h>
//#include <nRF24L01.h>
//#include <MirfHardwareSpiDriver.h>
//#include <PS2X_lib.h>  //for v1.6
#include <Wire.h>
#include <Servo.h>
#include <RF24.h>
#include <RF24_config.h>

RF24 radio(9,10);           // Define radio pin RF24 radio(CE,CSN), this case mean CE -> 8 & CSN -> 10. Hope it's a best choice. Or your can change like you want
const uint64_t pipe = 0xE8E8F0F0E1LL;
//#include <nunchuck.h>
static uint8_t nunchuck_buf[6];   // array to store nunchuck data,


Servo esc1;
Servo esc2;
int throttlePin = 0;
byte data[2];  

void setup(){
  Serial.begin(19200);
  nunchuck_setpowerpins(); // use analog pins 2&3 as fake gnd & pwr
  nunchuck_init(); // send the initilization handshake
  esc1.attach(7);
  radio.begin();           // Turn on RF24L01
  radio.openWritingPipe(pipe);
  radio.openReadingPipe(1,pipe);
  Serial.print ("Finished setup\n");
//  Mirf.cePin = 9; // CE sur D9
//  Mirf.csnPin = 10; // CSN sur D10
//  Mirf.spi = &MirfHardwareSpi;
//  Mirf.init(); 
//
//  Mirf.channel = 0; // On va utiliser le canal 0 pour communiquer (128 canaux disponible, de 0 a  127)
//  Mirf.payload = 10; //  ici il faut dÃ©clarer la taille du "payload" soit du message qu'on va transmettre, au max 32 octets
//  Mirf.config(); 
//
//  Mirf.setTADDR((byte *)"nrf02"); // Le 1er module va envoyer ses info au 2eme module
//  Mirf.setRADDR((byte *)"nrf01"); // On definit ici l'adresse du 1er module

  Serial.println("Le client est pret...");
  
  
}

void loop(){
nunchuck_get_data();
nunchuck_print_data();
//delay(400);
}


//
// Nunchuck functions
//



// Uses port C (analog in) pins as power & ground for Nunchuck
static void nunchuck_setpowerpins()
{
#define pwrpin PORTC3
#define gndpin PORTC2
    DDRC |= _BV(pwrpin) | _BV(gndpin);
    PORTC &=~ _BV(gndpin);
    PORTC |=  _BV(pwrpin);
    delay(100);  // wait for things to stabilize        
}

// initialize the I2C system, join the I2C bus,
// and tell the nunchuck we're talking to it
void nunchuck_init()
{ 
  Wire.begin();                  // join i2c bus as master
  Wire.beginTransmission(0x52); // transmit to device 0x52
  Wire.write(0x40);   // sends memory address
  Wire.write(0x00);   // sends sent a zero.  
  Wire.endTransmission(); // stop transmitting
}

// Send a request for data to the nunchuck
// was "send_zero()"
void nunchuck_send_request()
{
  Wire.beginTransmission(0x52); // transmit to device 0x52
  Wire.write(0x00);   // sends one byte
  Wire.endTransmission(); // stop transmitting
}

// Receive data back from the nunchuck, 
int nunchuck_get_data()
{
    int cnt=0;
    Wire.requestFrom (0x52, 6); // request data from nunchuck
    while (Wire.available ()) {
      // receive byte as an integer
      nunchuck_buf[cnt] = nunchuk_decode_byte(Wire.read());
      cnt++;
    }
    nunchuck_send_request();  // send request for next data payload
    // If we recieved the 6 bytes, then go print them
    if (cnt >= 5) {
     return 1;   // success
    }
    return 0; //failure
}

// Print the input data we have recieved
// accel data is 10 bits long
// so we read 8 bits, then we have to add
// on the last 2 bits.  That is why I
// multiply them by 2 * 2


void nunchuck_print_data()
{ 
  static int i=0;
  int joy_x_axis = nunchuck_buf[0];
  int joy_y_axis = nunchuck_buf[1];
  int accel_x_axis = nunchuck_buf[2]; // * 2 * 2; 
  int accel_y_axis = nunchuck_buf[3]; // * 2 * 2;
  int accel_z_axis = nunchuck_buf[4]; // * 2 * 2;

  int z_button = 0;
  int c_button = 0;

  // byte nunchuck_buf[5] contains bits for z and c buttons
  // it also contains the least significant bits for the accelerometer data
  // so we have to check each bit of byte outbuf[5]
  if ((nunchuck_buf[5] >> 0) & 1) 
    z_button = 1;
  if ((nunchuck_buf[5] >> 1) & 1)
    c_button = 1;

  if ((nunchuck_buf[5] >> 2) & 1) 
    accel_x_axis += 2;
  if ((nunchuck_buf[5] >> 3) & 1)
    accel_x_axis += 1;

  if ((nunchuck_buf[5] >> 4) & 1)
    accel_y_axis += 2;
  if ((nunchuck_buf[5] >> 5) & 1)
    accel_y_axis += 1;

  if ((nunchuck_buf[5] >> 6) & 1)
    accel_z_axis += 2;
  if ((nunchuck_buf[5] >> 7) & 1)
    accel_z_axis += 1;

//  Serial.print(i,DEC);
//  Serial.print("\t");
//  
//  Serial.print("joy:");
//  /*joy_x_axis = map(joy_x_axis, 28, 225, 0, 179);*/
//  Serial.print(joy_x_axis,DEC);
//  Serial.print(",");
  
  /*
  Serial.print(joy_y_axis, DEC);
  Serial.print("  \t");

  Serial.print("acc:");
  Serial.print(accel_x_axis, DEC);
  Serial.print(",");
  Serial.print(accel_y_axis, DEC);
  Serial.print(",");
  Serial.print(accel_z_axis, DEC);
  Serial.print("\t");

  Serial.print("but:");
  Serial.print(z_button, DEC);
  Serial.print(",");
  Serial.print(c_button, DEC);
*/

    int numero1 = joy_x_axis;
  int numero2 = joy_y_axis;
  int numero3 = accel_x_axis;
  int numero4 = accel_y_axis;

data[0] =joy_x_axis;


//  data[0] = (byte )((numero1 >> 8) & 0xff);
//  data[1] = (byte )(numero1 & 0xff);
//  data[2] = (byte )((numero2 >> 8) & 0xff);
//  data[3] = (byte )(numero2 & 0xff);
//  data[4] = (byte )((numero3 >> 8) & 0xff);
//  data[5] = (byte )(numero3 & 0xff);
//  data[6] = (byte )((numero4 >> 8) & 0xff);
//  data[7] = (byte )(numero4 & 0xff);
//Serial.print(data[0]);
//Serial.print(data[1]);
//Serial.print(data[2]);
//Serial.print(data[3]);
//Serial.print(data[4]);
//Serial.print(data[5]);
//Serial.print(data[6]);
//Serial.print(data[7]);

//Mirf.send((byte *)&data); // On envoi les donnees
radio.write(data,sizeof(data));  // Radio sending's command
esc1.write(joy_x_axis);
   Serial.print("\r\n");  // newline
  i++;
}

// Encode data to format that most wiimote drivers except
// only needed if you use one of the regular wiimote drivers
char nunchuk_decode_byte (char x)
{
  x = (x ^ 0x17) + 0x17;
  return x;
}


