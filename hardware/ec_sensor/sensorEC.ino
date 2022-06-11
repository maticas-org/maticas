#include "C:\Users\panda\Documents\Arduino\hive_conection\hive_conection.ino"
//librerías para el DS18B20
#include <OneWire.h>
#include <DallasTemperature.h>

char *topics[] = {"Esp8266!D4ta/10370001/EC", "Esp8266!D4ta/10370001/temp"};

int R1= 1000;
int Ra=25;
int ECPin= A0;
int ECGround=4; //02 pin
int ECPower =5; //01 pin
float TemperatureCoef = 0.019; //Compensación de la temperatura sobre los nutrientes
float K=2.88; //constante de celda
//DS18B20
#define ONE_WIRE_BUS 14          //05 pin
const int TempProbePossitive = 13;  //07 pin
const int TempProbeNegative  = 2 ;    //04 pin
 
void sendata(); 

OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);

float Temperature=10;
float EC=0;
float EC25 =0;
float raw= 0;
float Vin= 5;
float Vdrop= 0;
float Rc= 0;
float buffer=0;


void setup()
{
  setup_connection(); //establecer conexión con el broker
  
  Serial.begin(9600);
  //configuraciones para el DS18B20
  pinMode(TempProbeNegative , OUTPUT );
  digitalWrite(TempProbeNegative , LOW );
  pinMode(TempProbePossitive , OUTPUT );
  digitalWrite(TempProbePossitive , HIGH );
  //configuraciones para el EC
  pinMode(ECPin,INPUT);
  pinMode(ECPower,OUTPUT);
  pinMode(ECGround,OUTPUT);
  digitalWrite(ECGround,LOW);
  
  delay(100);

  sensors.begin();

  delay(100);

  R1=(R1+Ra);//Resistencia estática
};


void loop(){
  GetEC(); //calcular el EC
  //PrintReadings();  //imprimir los datos en el monitor de arduino
  
  if (!client->connected()) {
    reconnect();
  }
  client->loop();

  unsigned long now = millis();
  if (now - lastMsg > 10000) {
    lastMsg = now;
    sendata();
  }
  delay(5000);
}


void GetEC(){
  //lectura de la temperatura
  sensors.requestTemperatures();
  Temperature=sensors.getTempCByIndex(0); 
  
  //lectura del EC
  digitalWrite(ECPower,HIGH);
  raw= analogRead(ECPin);
  digitalWrite(ECPower,LOW);
  
  //Conversión del EC, con resistencia y voltaje
  Vdrop= (Vin*raw)/1024.0;
  Rc=(Vdrop*R1)/(Vin-Vdrop);
  Rc=Rc-Ra;
  EC = 1000/(Rc*K);

  //EC en base a la temperatura
  EC25  =  EC/ (1+ TemperatureCoef*(Temperature-25.0));
;}


void PrintReadings(){
  Serial.print(" EC: ");
  Serial.print(EC25);
  Serial.print(" Simens  ");
  Serial.print(Temperature);
  Serial.println(" *C ");
};

#define MSG_BUFFER_SIZE_2 (800)
char topic[MSG_BUFFER_SIZE_2];

void sendata() {
  double measurement[3] = {EC25, Temperature};

  for(int i = 0; i < 2; i++){
   snprintf(msg, MSG_BUFFER_SIZE, "%10.2f", measurement[i]);
   snprintf(topic, MSG_BUFFER_SIZE_2, "%s", topics[i]);

   Serial.println();
   Serial.print(topic);
   Serial.print("/");
   Serial.print(msg);
   Serial.println();
    
   client->publish(topic, msg);
  }

};
