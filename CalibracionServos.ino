#include <SoftwareSerial.h>
#include <Servo.h>
Servo myServos[6];
int  PosicionInicial[6] = {90, 90, 90, 90, 90, 180}; 
int PosicionFinal[6] = {90, 90, 90, 90, 90, 0}; 
void setup() {
    myServos[0].attach(11);
    myServos[1].attach(10);
    myServos[2].attach(9);
    myServos[3].attach(6);
    myServos[4].attach(5);
    myServos[5].attach(3);
    Serial.begin(9600); 
    delay(20);
    
    for( int i = 0; i<6; i++)
    {
        myServos[i].write(PosicionInicial[i]);
    }
}

void loop() {
  // Se coloca al robot en la posicion inicial
        //memmove(PosicionInicial,PosicionFinal, sizeof(PosicionFinal));
        MoverServo(PosicionInicial, PosicionFinal, myServos);
        delay(1000);
        MoverServo(PosicionFinal, PosicionInicial, myServos);
        //memmove(servoPPos,servoPos, sizeof(servoPos));
}

void MoverServo(int (& servoPreviousPos)[6], int (& servoPosAct)[6], Servo (& servo)[6]) {
  for(int s=0; s<6; s++){
    if (servoPreviousPos[s] > servoPosAct[s]) {
          for ( int j = servoPreviousPos[s]; j >= servoPosAct[s]; j--) {
            servo[s].write(j);
            delay(20);
          }
      }
      if (servoPreviousPos[s] < servoPosAct[s]) {
        for ( int j = servoPreviousPos[s]; j <= servoPosAct[s]; j++) {
          servo[s].write(j);
          delay(20);
        }
      }
      //servoPreviousPos[s] = servoPosAct[s];  
  }
  }
