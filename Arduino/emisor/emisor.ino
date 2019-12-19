#include <RF24.h>
#include <SPI.h>
//#include <EEPROM.h>
#include <Arduino.h>
//#include <Wire.h>
#include <U8g2lib.h>
#include <MPU9250.h>
#include <string.h>

#define BUZZER_PIN 3
#define LED_PIN1 5 //Red
#define LED_PIN2 4//blue
#define CE_PIN 9
#define CSN_PIN 10



U8G2_SSD1306_96X16_ER_F_HW_I2C u8g2(U8G2_R0, /* reset=*/ U8X8_PIN_NONE);   
MPU9250 mpu;
RF24 radio(CE_PIN,CSN_PIN);

byte direccion[6] ={'F','u','l','l','a','x'};
const int interval_ACC = 16;           
const int interval_LED1 = 300;   
const int interval_LED2 = 500;   

unsigned int prev_Millis_ACC = 0;        
unsigned int prev_Millis_LED1 = 0;        
unsigned int prev_Millis_LED2 = 0;   


struct package
{
  float RollC;
  float PitchC;
  float YawC;
  int stateLed1;
  int stateLed2;
  unsigned int current_Millis;
};

typedef struct package Package;
Package data;

void setup(void)
   {   
       pinMode(LED_PIN1, OUTPUT);
       pinMode(LED_PIN2, OUTPUT);
       radio.openWritingPipe(direccion);
       radio.begin();
       Wire.begin();
       delay(2000);
       
       mpu.setup();
       data.stateLed1 = 0;
       data.stateLed2 = 0;
       u8g2.begin();
       u8g2.clearBuffer();          
       u8g2.setFont(u8g2_font_ncenB08_tr);
       char Title = F("Full_Axis listo.");

       u8g2.drawStr(2,10,Title);  
       u8g2.sendBuffer();          
       delay(1000);  

    }
  

void loop(void)
  {
    data.current_Millis = millis();
    if (data.current_Millis - prev_Millis_ACC >= interval_ACC){
        prev_Millis_ACC = data.current_Millis;
        mpu.update();
        data.RollC = mpu.getRoll();
        data.YawC = mpu.getYaw();
        data.PitchC = mpu.getPitch();
        radio.write(&data, sizeof(data));
    }

    if (data.current_Millis - prev_Millis_LED1 >= interval_LED1){
        prev_Millis_LED1 = data.current_Millis;
        switch (data.stateLed1){
          case 1:
            data.stateLed1 = 0;
            digitalWrite(LED_PIN2, LOW);
            break;                          
          default:
            data.stateLed1 = 1;
            digitalWrite(LED_PIN2, HIGH);          
            break;
          }
    }
    if (data.current_Millis - prev_Millis_LED2 >= interval_LED2){
        prev_Millis_LED2 = data.current_Millis;
        switch (data.stateLed2){
          case 1:
            data.stateLed2 = 0;
            digitalWrite(LED_PIN1, LOW);
            break;                          
          default:
            data.stateLed2 = 1;
            digitalWrite(LED_PIN1, HIGH);
            break;
          }
    }    
   }


   ///con F() en rf24 se ganaron 374 bytes 
