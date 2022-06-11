
#include "C:\Users\panda\Documents\Arduino\hive_conection\hive_conection.ino"


#include <OneWire.h>
#include <DallasTemperature.h>

char *topics[] = {"Esp8266!D4ta/10370001/EC", "Esp8266!D4ta/10370001/temp"};

int R1= 1000;
int Ra=25; //Resistance of powering Pins
int ECPin= A0;
int ECGround=4;
int ECPower =5;

//*********** Converting to ppm [Learn to use EC it is much better**************//
// Hana      [USA]        PPMconverion:  0.5
// Eutech    [EU]          PPMconversion:  0.64
//Tranchen  [Australia]  PPMconversion:  0.7

float PPMconversion=0.7;


//*************Compensating for temperature ************************************//
//The value below will change depending on what chemical solution we are measuring
//0.019 is generaly considered the standard for plant nutrients [google "Temperature compensation EC" for more info
float TemperatureCoef = 0.019; //this changes depending on what chemical we are measuring


//********************** Cell Constant For Ec Measurements *********************//
//Mine was around 2.9 with plugs being a standard size they should all be around the same
//But If you get bad readings you can use the calibration script and fluid to get a better estimate for K

float K=2.88;

 

//************ Temp Probe Related *********************************************//

#define ONE_WIRE_BUS 13          // Data wire For Temp Probe is plugged into pin 10 on the Arduino
const int TempProbePossitive = 14;  //Temp Probe power connected to pin 9
const int TempProbeNegative  = 2 ;    //Temp Probe Negative connected to pin 8
 
void sendata(); 

//***************************** END Of Recomended User Inputs *****************************************************************//

OneWire oneWire(ONE_WIRE_BUS);// Setup a oneWire instance to communicate with any OneWire devices

DallasTemperature sensors(&oneWire);// Pass our oneWire reference to Dallas Temperature.

float Temperature=10;
float EC=0;
float EC25 =0;
int ppm =0;
 
float raw= 0;
float Vin= 5;
float Vdrop= 0;
float Rc= 0;
float buffer=0;

//*********************************Setup - runs Once and sets pins etc ******************************************************//

void setup()
{
  setup_connection();
  
  Serial.begin(9600);
  pinMode(TempProbeNegative , OUTPUT ); //seting ground pin as output for tmp probe
  digitalWrite(TempProbeNegative , LOW );//Seting it to ground so it can sink current
  pinMode(TempProbePossitive , OUTPUT );//ditto but for positive
  digitalWrite(TempProbePossitive , HIGH );
  pinMode(ECPin,INPUT);
  pinMode(ECPower,OUTPUT);//Setting pin for sourcing current
  pinMode(ECGround,OUTPUT);//setting pin for sinking current
  digitalWrite(ECGround,LOW);//We can leave the ground connected permanantly
  delay(100);// gives sensor time to settle

  sensors.begin();

  delay(100);

  //** Adding Digital Pin Resistance to [25 ohm] to the static Resistor *********//

  // Consule Read-Me for Why, or just accept it as true

  R1=(R1+Ra);// Taking into acount Powering Pin Resitance
};

//******************************************* End of Setup **********************************************************************//

 

//************************************* Main Loop - Runs Forever ***************************************************************//
//Moved Heavy Work To subroutines so you can call them from main loop without cluttering the main loop
void loop(){
  GetEC();          //Calls Code to Go into GetEC() Loop [Below Main Loop] dont call this more that 1/5 hhz [once every five seconds] or you will polarise the water
  //PrintReadings();  // Cals Print routine [below main loop]
  
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

//************************************** End Of Main Loop **********************************************************************//

//************ This Loop Is called From Main Loop************************//

void GetEC(){
  //*********Reading Temperature Of Solution *******************//
  sensors.requestTemperatures();// Send the command to get temperatures
  Temperature=sensors.getTempCByIndex(0); //Stores Value in Variable
  //************Estimates Resistance of Liquid ****************//
 
  digitalWrite(ECPower,HIGH);
  raw= analogRead(ECPin);
  digitalWrite(ECPower,LOW);
  
  //***************** Converts to EC **************************//
  Vdrop= (Vin*raw)/1024.0;
  Rc=(Vdrop*R1)/(Vin-Vdrop);
  Rc=Rc-Ra; //acounting for Digital Pin Resitance
  EC = 1000/(Rc*K);

//*************Compensating For Temperaure********************//
  EC25  =  EC/ (1+ TemperatureCoef*(Temperature-25.0));
  ppm=(EC25)*(PPMconversion*1000);

;}

//************************** End OF EC Function ***************************//
//***This Loop Is called From Main Loop- Prints to serial usefull info ***//

void PrintReadings(){
  Serial.print("Rc: ");
  Serial.print(Rc);
  Serial.print(" EC: ");
  Serial.print(EC25);
  Serial.print(" Simens  ");
  Serial.print(ppm);
  Serial.print(" ppm  ");
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
