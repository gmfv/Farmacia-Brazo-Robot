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
int PosicionInicial[6]={90, 90, 90, 90, 90, 90};
int servoPosCinta[6]= {100, 100, 100, 100, 100, 100};
//int servoPosCerrarPinza[6]= {10, 10, 10, 10, 10, 10};
int aux[6];
String incomingData, Cantidad, Medicamento, recepcion, StockActual, ID;
int PosMed[16][6]={{100, 100, 100, 100, 100, 100},
                  {100, 100, 100, 100, 100, 100},
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
String modo = "Cliente";
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
      if(digitalRead(botonR) == HIGH){
        digitalWrite(ledPIN_run, HIGH);
        digitalWrite(ledPIN_stop, HIGH);
        while(digitalRead(botonR) != LOW){ //Sale del while cuando suelta la primera vez
          delay(10);
        }
        Serial.println("P");
        while(digitalRead(botonR) != HIGH){
          delay(10);
        }
        while(digitalRead(botonR) != HIGH){
          delay(10);
        }
        modo = "Reposicion";
        Serial.println("R1");
      }
      if (modo == "Reposicion"){
        digitalWrite(ledPIN_stop, LOW);
      }
      
      if(Serial.available()>0){
            recepcion=Serial.readString();
            Serial.println(recepcion);
            digitalWrite(ledPIN_stop, LOW);
            digitalWrite(ledPIN_run, LOW);
            if (recepcion[0]=='R'){
               Serial.println("RRRR"); //Se debe avisar que se esta reponiendo
               //Serial.println(recepcion);
               incomingData=recepcion.substring(1);
               StockActual = getValue(incomingData, 'M', 0);
               ID = getValue(incomingData, 'M', 1);
               Serial.println(StockActual+'S'+ID);
              //digitalWrite(ledPIN_run, HIGH);
              //digitalWrite(ledPIN_stop, LOW);
              
            //Definimos la posicion a la que debe ir como la de entrega y movemos los servos a la posicion de entreg
               Serial.println("M1") ;
               memmove(servoPos,servoPosCinta, sizeof(servoPos));
               MoverServo(servoPPos, servoPos, myServos);
               memmove(servoPPos,servoPos, sizeof(servoPos));
               //Serial.println("M2") ;
               Serial.println(40);
               
               //Se debe mover la servos especificos para agarrar el medicamento (Cierra la pinza)
               servoPos[4]=120;//Definir posicion de la pinza para cerrar
               servoPos[5]=120;
               AyCPinza(servoPPos[4], servoPos[4], myServos[4]);
               AyCPinza(servoPPos[5], servoPos[5], myServos[5]);
               servoPPos[4]=servoPos[4]; //Se actualiza la posicion previa a la que se encuentra actualmente
               servoPPos[5]=servoPos[5];
               Serial.println(60);
               
               for (int i=0; i<16; i++){
                  if (ID.toInt()-1 == i){
                    for(int j=0; j<6; j++){aux[j]=PosMed[i][j];}
                  }
                }

               memmove(servoPosMedicamento,aux, sizeof(servoPosMedicamento));
                          
               //Se mueve al estante del medicamento
               memmove(servoPos,servoPosMedicamento, sizeof(servoPos));
               MoverServo(servoPPos, servoPos, myServos);
               memmove(servoPPos,servoPos, sizeof(servoPos));
               Serial.println(80);
                
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
               Serial.println(100);
               modo = "Cliente";
               delay(20);
               Serial.println("RF");
               
          }else if (recepcion[0]='C'){
            modo = "Cliente";
            Serial.println("CC");
            Serial.println(recepcion);
            incomingData=recepcion.substring(1);
            Medicamento = getValue(incomingData, 'M', 1);
            Cantidad = getValue(incomingData, 'M', 0);
          
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
               evolution=((100/Cantidad.toInt())/5)*(contador+1);
               Serial.println(evolution);
               
               //Se debe mover la servos especificos para agarrar el medicamento (Posicion del estante con agarre)
               memmove(servoPos, servoPosMedicamento, sizeof(servoPos));
               MoverServo(servoPPos, servoPos, myServos);
               memmove(servoPPos,servoPos, sizeof(servoPos));
               evolution=((100/Cantidad.toInt())/5)*2*(contador+1);
               //Debe enviar mensaje de 40%
               Serial.println(evolution);
               
               //Se debe volver a la posicion del estante sin agarre
               memmove(servoPos,servoPosEntregaAbierto, sizeof(servoPos));
               MoverServo(servoPPos, servoPos, myServos);
               memmove(servoPPos,servoPos, sizeof(servoPos));
               evolution=((100/Cantidad.toInt())/5)*3*(contador+1);
               //Debe enviar mensaje de 60%
               Serial.println(evolution);
               
               //Se mueven los servos para dejar el medicamento en la zona de entregas
               memmove(servoPos,servoPosEntregaCerrado, sizeof(servoPos));
               MoverServo(servoPPos, servoPos, myServos);
               memmove(servoPPos,servoPos, sizeof(servoPos));
               
               //La pinza suelta los medicamentos
               //Debe enviar mensaje de 80%
               evolution=((100/Cantidad.toInt())/5)*4*(contador+1);
               Serial.println(evolution);
               
               //Vuelve a la posicion inicial
               memmove(servoPos,PosicionInicial, sizeof(servoPos));
               MoverServo(servoPPos, servoPos, myServos);
               memmove(servoPPos,servoPos, sizeof(servoPos));
               //Debe enviar mensaje de 99.9%
               evolution=(100/Cantidad.toInt())*(contador+1);
               Serial.println(evolution);
               contador=contador+1;
            }
               Serial.println(100);
      }              
    }
    digitalWrite(ledPIN_run, LOW);
    digitalWrite(ledPIN_stop, HIGH);
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
  
