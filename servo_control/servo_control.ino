
#include <Wire.h>
#include "Adafruit_PWMServoDriver.h"

// called this way, it uses the default address 0x40
Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();
// you can also call it with a different address you want
//Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver(0x41);

// Depending on your servo make, the pulse width min and max may vary, you 
// want these to be as small/large as possible without hitting the hard stop
// for max range. You'll have to tweak them as necessary to match the servos you
// have!
#define H_SERVOMIN  180 // this is the 'minimum' pulse length count (out of 4096)
#define H_SERVOMAX  650   // this is the 'maximum' pulse length count (out of 4096)
#define V_SERVOMIN 180
#define V_SERVOMAX 650

#define V_SPEED 3
#define H_SPEED 3

// our servo # counter
uint8_t servonum = 0;
int hServoPos = (H_SERVOMIN+H_SERVOMAX)/2;
int vServoPos = V_SERVOMAX;

char buffer;
void setup() {
  Serial.begin(9600);
   pwm.begin();
  
  pwm.setPWMFreq(60);  // Analog servos run at ~60 Hz updates
}

// you can use this function if you'd like to set the pulse length in seconds
// e.g. setServoPulse(0, 0.001) is a ~1 millisecond pulse width. its not precise!
void setServoPulse(uint8_t n, double pulse) {
  double pulselength;
  
  pulselength = 1000000;   // 1,000,000 us per second
  pulselength /= 60;   // 60 Hz
  Serial.print(pulselength); Serial.println(" us per period"); 
  pulselength /= 4096;  // 12 bits of resolution
  Serial.print(pulselength); Serial.println(" us per bit"); 
  pulse *= 1000;
  pulse /= pulselength;
  Serial.println(pulse);
  pwm.setPWM(n, 0, pulse);
}

//Sets the servo position between 0-2H_SPEEDH_SPEED
void setServoPos(int pos,uint8_t number){
  //uint16_t pulseLen = ((double)pos/(double)2H_SPEED6.0) * (H_SERVOMAX-H_SERVOMIN) + H_SERVOMIN;
  pwm.setPWM(number,0,pos);
}

void loop() {
 
  if (Serial.available() > 0){
    while (Serial.available() > 0){
      buffer = Serial.read();
      if (buffer =='a'){
        if (hServoPos > H_SERVOMIN+H_SPEED){
          hServoPos -= H_SPEED;
        }else{
          hServoPos = H_SERVOMIN;
        }
      }else if (buffer == 'd'){
        if (hServoPos < H_SERVOMAX-H_SPEED  ){
          hServoPos += H_SPEED;
        }else{
          hServoPos = H_SERVOMAX;
        }
      }else if (buffer == 'w'){
        if (vServoPos < V_SERVOMAX-V_SPEED  ){
          vServoPos += V_SPEED;
        }else{
          vServoPos = H_SERVOMAX;
        }
      }else if (buffer == 's'){
        if (vServoPos < V_SERVOMAX+V_SPEED  ){
          vServoPos -= V_SPEED;
        }else{
          vServoPos = V_SERVOMAX;
        }
      }
    }
    setServoPos(hServoPos,0);
    setServoPos(vServoPos,1);
  }
}
