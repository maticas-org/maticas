#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <time.h>
#include <TZ.h>
#include <FS.h>
#include <LittleFS.h>
#include <CertStoreBearSSL.h>


// Update these with values suitable for your network.
const char* ssid = "Movistarfibra";
const char* password = "Contraseña de la red wifi";
const char* mqtt_server = "http://367b0404af444e90a3cf6e47443a0a6b.s1.eu.hivemq.cloud/";

// A single, global CertStore which can be used by all connections.
// Needs to stay live the entire time any of the WiFiClientBearSSLs
// are present.
BearSSL::CertStore certStore;

WiFiClientSecure espClient;
PubSubClient * client;
unsigned long lastMsg = 0;
#define MSG_BUFFER_SIZE (500)
char msg[MSG_BUFFER_SIZE];
int value = 0;

void setup_wifi() {
  
  delay(10);
  // We start by connecting to a WiFi network
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  randomSeed(micros());

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}


void setDateTime() {
  // You can use your own timezone, but the exact time is not used at all.
  // Only the date is needed for validating the certificates.
  configTime(TZ_Europe_Berlin, "pool.ntp.org", "time.nist.gov");

  Serial.print("Waiting for NTP time sync: ");
  time_t now = time(nullptr);
  while (now < 8 * 3600 * 2) {
    delay(100);
    Serial.print(".");
    now = time(nullptr);
  }
  Serial.println();

  struct tm timeinfo;
  gmtime_r(&now, &timeinfo);
  Serial.printf("%s %s", tzname[0], asctime(&timeinfo));
}


void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Message arrived [");
  Serial.print(topic);
  Serial.print("] ");
  
  for (int i = 0; i < length; i++) {
    Serial.print((char)payload[i]);
  }
  Serial.println();

  // Switch on the LED if the first character is present
  if ((char)payload[0] != NULL) {
    digitalWrite(LED_BUILTIN, LOW); // Turn the LED on (Note that LOW is the voltage level
    // but actually the LED is on; this is because
    // it is active low on the ESP-01)
    delay(500);
    digitalWrite(LED_BUILTIN, HIGH); // Turn the LED off by making the voltage HIGH
  } else {
    digitalWrite(LED_BUILTIN, HIGH); // Turn the LED off by making the voltage HIGH
  }
  
}


void reconnect() {
  
  // Loop until we’re reconnected
  while (!client->connected()) {
    
    Serial.print("Attempting MQTT connection…");
    String clientId = "SensorEC";
    
    // Attempt to connect
    // Insert your password
    if (client->connect(clientId.c_str(), "numbre de usuario", "contraseña")) {
      Serial.println("connected");

      // Once connected, publish an announcement…
      //client->publish("testTopic", "hello world");
      // … and resubscribe
      //client->subscribe("testTopic");
    
    } else {
      Serial.print("failed, rc = ");
      Serial.print(client->state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    
    }
  }
  
}


void setup_connection() {
  delay(500);
  // When opening the Serial Monitor, select 9600 Baud
  Serial.begin(9600);
  delay(500);

  LittleFS.begin();
  setup_wifi();
  setDateTime();

  pinMode(LED_BUILTIN, OUTPUT); // Initialize the LED_BUILTIN pin as an output

  // you can use the insecure mode, when you want to avoid the certificates
  //espclient->setInsecure();

  int numCerts = certStore.initCertStore(LittleFS, PSTR("/certs.idx"), PSTR("/certs.ar"));
  Serial.printf("Number of CA certs read: %d\n", numCerts);
  if (numCerts == 0) {
    Serial.printf("No certs found. Did you run certs-from-mozilla.py and upload the LittleFS directory before running?\n");
    return; // Can't connect to anything w/o certs!
  }

  BearSSL::WiFiClientSecure *bear = new BearSSL::WiFiClientSecure();
  // Integrate the cert store with this connection
  bear->setCertStore(&certStore);

  client = new PubSubClient(*bear);

  client->setServer(mqtt_server, 8883);
  client->setCallback(callback);
}

#include <OneWire.h>
#include <DallasTemperature.h>

char *topics[] = {"Esp8266!D4ta/10370001/RC","Esp8266!D4ta/10370001/EC",
                  "Esp8266!D4ta/10370001/ppm","Esp8266!D4ta/10370001/temp"};

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

  Serial.println("ElCheapo Arduino EC-PPM measurments");
  Serial.println("By: Michael Ratcliffe  Mike@MichaelRatcliffe.com");
  Serial.println("Free software: you can redistribute it and/or modify it under GNU ");
  Serial.println("");
  Serial.println("Make sure Probe and Temp Sensor are in Solution and solution is well mixed");
  Serial.println("");
  Serial.println("Measurments at 5's Second intervals [Dont read Ec morre than once every 5 seconds]:");
};

//******************************************* End of Setup **********************************************************************//

 

//************************************* Main Loop - Runs Forever ***************************************************************//
//Moved Heavy Work To subroutines so you can call them from main loop without cluttering the main loop
void loop(){
  GetEC();          //Calls Code to Go into GetEC() Loop [Below Main Loop] dont call this more that 1/5 hhz [once every five seconds] or you will polarise the water
  PrintReadings();  // Cals Print routine [below main loop]
  delay(5000);
  if (!client->connected()) {
    reconnect();
  }
  client->loop();

  unsigned long now = millis();
  if (now - lastMsg > 10000) {
    lastMsg = now;
    sendata();
  }
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
  double measurement[5] = {Rc, EC25, ppm, Temperature};

  for(int i = 0; i < 4; i++){
   snprintf(msg, MSG_BUFFER_SIZE, "%10.2f", measurement[i]);
   snprintf(topic, MSG_BUFFER_SIZE_2, "%s", topics[i]);
  }

  Serial.println();
  Serial.print(topic);
  Serial.print("/");
  Serial.print(msg);
  Serial.println();

  client->publish(topic, msg);

};
