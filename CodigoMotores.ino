#include <SoftwareSerial.h>
#include <Servo.h>
Servo myServos[6];
int estado=0; //Si es 0 no se mueve, si es 1 debe recoger un medicamento para entrega, si es 2 debe reponer el medicamento, 3 es que ya esta listo
int servoPos[6]; // Posicion actual
int servoPPos[6]; // Posicion anterior
int servoPosEstante[6]={-90, 20, 30, 50, 30, 45}; // Posicion del estante DEFINIR
int servoPosMedicamento[6]={70, 70, 70, 70, 70, 70};//Posicion en la que abre la garra y cierra
int servoPosEntregaCerrado[6]={90, 90, 90, 90, 90, 90}; //Posicion del reponedor
int servoPosEntregaAbierto[6]={90, 90, 90, 150, 150, 150}; //Posicion del reponedor
int servoPosReponedorCerrado[6]={70, 70, 70, 70, 70, 70}; //Posicion reponedor sin agarrar el medicamento
int servoPosReponedorAbierto[6]={70, 70, 70, 100, 100, 100}; //Posicion reponedor sin agarrar el medicamento
int PosicionInicial[6]={90, 150, 35, 140, 85, 80};
int servoPosCinta[6]= {20, 20, 20, 20, 20, 20};
int servoPosCerrarPinza[6]= {10, 10, 10, 10, 10, 10};
int aux[6];
String incomingData, Cantidad, Medicamento, recepcion;
int PosMed[16][6]={{10, 10, 10, 10, 10, 10},
                  {10, 10, 10, 10, 10, 10},
                  {10, 10, 10, 10, 10, 10},
                  {10, 10, 10, 10, 10, 10},
                  {10, 10, 10, 10, 10, 10},
                  {10, 10, 10, 10, 10, 10},
                  {10, 10, 10, 10, 10, 10},
                  {10, 10, 10, 10, 10, 10},
                  {10, 10, 10, 10, 10, 10},
                  {10, 10, 10, 10, 10, 10},
                  {10, 10, 10, 10, 10, 10},
                  {10, 10, 10, 10, 10, 10},
                  {10, 10, 10, 10, 10, 10},
                  {10, 10, 10, 10, 10, 10},
                  {10, 10, 10, 10, 10, 10},
                  {10, 10, 10, 10, 10, 10}};
const int ledPIN_run = 2; //VERIFICAR PINES PARA CONEXION
const int ledPIN_stop = 4;
int evolution, incomingData1;
int botonR = 7;
void setup() {
    myServos[0].attach(3);
    myServos[1].attach(5);
    myServos[2].attach(6);
    myServos[3].attach(9);
    myServos[4].attach(10);
    myServos[5].attach(11);
    pinMode(ledPIN_run , OUTPUT); 
    pinMode(ledPIN_stop , OUTPUT);
    pinMode(botonR , INPUT_PULLUP);
    Serial.begin(115200); 
    delay(20);
    pinMode(botonR , INPUT);
    // Se coloca al robot en la posicion inicial
     memmove(servoPPos, PosicionInicial, sizeof(servoPosEstante));
    for( int i = 0; i<6; i++)
    {
        myServos[i].write(servoPPos[i]);
    }
    delay(20);
}
void loop() {
    //if (digitalRead(botonR) == LOW) Serial.println("R");
    //if (digitalRead(botonR) == HIGH) Serial.println("H");
      //if(digitalRead(botonR) == LOW){
          if(Serial.available()>0){
            
            recepcion=Serial.readString();
            Serial.println(recepcion);
            if (recepcion[0]=='R'){
              Serial.println("RR"); //Se debe avisar que se esta reponiendo
              digitalWrite(ledPIN_run, HIGH);
              digitalWrite(ledPIN_stop, LOW);
            //Definimos la posicion a la que debe ir como la de entrega y movemos los servos a la posicion de entreg
               do {
                  incomingData1 = recepcion[1]-'0';
                }while(incomingData1!=1 || incomingData1!=2 || incomingData1!=3 || incomingData1!=4 ||incomingData1!=5 ||incomingData1!=6 || incomingData1!=7 || incomingData1!=8 || incomingData1!=9 || incomingData1!=10 || incomingData1!=11 || incomingData1!=12 || incomingData1!=13 || incomingData1!=14 || incomingData1!=15 || incomingData1!=16); //Esperamos que la lectura sea una valida
               Serial.println("S") ;
               memmove(servoPos,servoPosCinta, sizeof(servoPos));
               MoverServo(servoPPos, servoPos, myServos);
               memmove(servoPPos,servoPos, sizeof(servoPos));
               
               //Se debe mover la servos especificos para agarrar el medicamento (Cierra la pinza)
               servoPos[4]=120;//Definir posicion de la pinza para cerrar
               servoPos[5]=120;
               AyCPinza(servoPPos[4], servoPos[4], myServos[4]);
               AyCPinza(servoPPos[5], servoPos[5], myServos[5]);
               servoPPos[4]=servoPos[4]; //Se actualiza la posicion previa a la que se encuentra actualmente
               servoPPos[5]=servoPos[5];
             
               for (int i=0; i<16; i++){
                  if (incomingData1 == i){
                    for(int j=0; j<6; j++){
                      aux[j]=PosMed[i][j];
                      }
                    memmove(servoPosMedicamento,aux, sizeof(servoPosMedicamento));
                  }
                }
                          
               //Se mueve al estante del medicamento
                memmove(servoPos,servoPosMedicamento, sizeof(servoPos));
               MoverServo(servoPPos, servoPos, myServos);
                memmove(servoPPos,servoPos, sizeof(servoPos));
    
               //Se abre la pinza
               servoPos[4]=120;//Definir posicion de la pinza para abrir
               servoPos[5]=120;
               AyCPinza(servoPPos[4], servoPos[4], myServos[4]);
               AyCPinza(servoPPos[5], servoPos[5], myServos[5]);
               servoPPos[4]=servoPos[4]; //Se actualiza la posicion previa a la que se encuentra actualmente
               servoPPos[5]=servoPos[5];
               
                //Vuelve a la posicion inicial
               memmove(servoPos,PosicionInicial, sizeof(servoPos));
               MoverServo(servoPPos, servoPos, myServos);
                memmove(servoPPos,servoPos, sizeof(servoPos));
      }
      else if (recepcion[0]='C'){
        Serial.println("CC");
        Serial.println(recepcion);
        incomingData=recepcion.substring(1);
      //Serial.println(Serial.available());
    //if (Serial.available() > 1) {
      //delay(10);
      Medicamento = getValue(incomingData, 'M', 0);
      Cantidad = getValue(incomingData, 'M', 1);
      
      //if (Medicamento == "1" || Medicamento == "2" || Medicamento == "3" || Medicamento == "4" || Medicamento == "5" || Medicamento == 6 || Medicamento == 7 || Medicamento == 8 || Medicamento == 9 ||Medicamento == 10 ||Medicamento == 11 ||Medicamento == 12 ||Medicamento == 13 ||Medicamento == 14 ||Medicamento == 15 ||Medicamento == 16 ){
       Serial.println(Medicamento+'S'+Cantidad);
       //digitalWrite(ledPIN_run, HIGH);
       //digitalWrite(ledPIN_stop, LOW);
       int contador=0;
       while (contador<Cantidad.toInt()){
          //Definimos la posicion a la que debe ir como la de el estante y movemos los servos a la posicion del estante sin agarre
           memmove(servoPos, servoPosEstante, sizeof(servoPosEstante));
           MoverServo(servoPPos, servoPos, myServos);
           memmove(servoPPos, servoPos, sizeof(servoPosEstante));
           //Debe enviar mensaje de 20%
           evolution=20*(contador+1/Cantidad.toInt())
           Serial.println(evolution);
           
           //Se debe mover la servos especificos para agarrar el medicamento (Posicion del estante con agarre)
           memmove(servoPos, servoPosMedicamento, sizeof(servoPos));
           MoverServo(servoPPos, servoPos, myServos);
           memmove(servoPPos,servoPos, sizeof(servoPos));
           evolution=40*(contador+1/Cantidad.toInt())
           //Debe enviar mensaje de 40%
           Serial.println(40);
           
           //Se debe volver a la posicion del estante sin agarre
           memmove(servoPos,servoPosEntregaAbierto, sizeof(servoPos));
           MoverServo(servoPPos, servoPos, myServos);
           memmove(servoPPos,servoPos, sizeof(servoPos));
           evolution=60*(contador+1/Cantidad.toInt())
           //Debe enviar mensaje de 60%
           Serial.println(evolution);
           
           //Se mueven los servos para dejar el medicamento en la zona de entregas
           memmove(servoPos,servoPosEntregaCerrado, sizeof(servoPos));
           MoverServo(servoPPos, servoPos, myServos);
           memmove(servoPPos,servoPos, sizeof(servoPos));
           //La pinza suelta los medicamentos
           //Debe enviar mensaje de 80%
           evolution=80*(contador+1/Cantidad.toInt())
           Serial.println(evolution);
           //Vuelve a la posicion inicial
           memmove(servoPos,PosicionInicial, sizeof(servoPos));
           MoverServo(servoPPos, servoPos, myServos);
           memmove(servoPPos,servoPos, sizeof(servoPos));
           //Debe enviar mensaje de 99.9%
           evolution=99*(contador+1/Cantidad.toInt())
           Serial.println(evolution);
           contador=contador+1;
        }
           Serial.println(100);
      }              
    }
}
//Funcion que recibe las posiciones de los servos a la que desea llegar, la que se encuentra actualmente y los servos
void MoverServo(int (& servoPreviousPos)[6], int (& servoPosAct)[6], Servo (& servo)[6]) {
  for(int s=0; s<6; s++){
    if (servoPreviousPos[s] > servoPosAct[s]) {
          for ( int j = servoPreviousPos[s]; j >= servoPosAct[s]; j--) {
            servo[s].write(j);
            delay(30);
          }
      }
      if (servoPreviousPos[s] < servoPosAct[s]) {
        for ( int j = servoPreviousPos[s]; j <= servoPosAct[s]; j++) {
          servo[s].write(j);
          delay(30);
        }
      }
      //servoPreviousPos[s] = servoPosAct[s];  
  }
  }

void AyCPinza(int pos5p, int pos5, Servo servo) {
    if (pos5p > pos5) {
          for ( int j = pos5p; j >= pos5; j--) {
            servo.write(j);
            delay(30);
          }
      }
      if (pos5p < pos5) {
        for ( int j = pos5p; j <= pos5 ; j++) {
          servo.write(j);
          delay(30);
        }
      }
      //servoPreviousPos[s] = servoPosAct[s];  
  }

String getValue(String data, char separator, int index)
{
    int found = 0;
    int strIndex[] = { 0, -1 };
    int maxIndex = data.length() - 1;

    for (int i = 0; i <= maxIndex && found <= index; i++) {
        if (data.charAt(i) == separator || i == maxIndex) {
            found++;
            strIndex[0] = strIndex[1] + 1;
            strIndex[1] = (i == maxIndex) ? i+1 : i;
        }
    }
    return found > index ? data.substring(strIndex[0], strIndex[1]) : "";
}
  
