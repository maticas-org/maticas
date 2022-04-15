#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <time.h>
#include <TZ.h>
#include <FS.h>
#include <LittleFS.h>
#include <CertStoreBearSSL.h>

#include <Wire.h>


// The following pins are selected for controling 
// the relays from the peristaltic pump 

// Pins of the corresponding peristaltic pumps:
//                   { ph_acid_pin, ph_basic_pin, ec_a_pin, ec_b_pin}
//                   { D5, D6, D7, D8 }  
const int pins[4] =  { 14, 12, 13, 15 };

char *topics[4] = {"Esp8266!D4ta/10370007/pump/ph/acid", 
                   "Esp8266!D4ta/10370007/pump/ph/basic",
                   "Esp8266!D4ta/10370007/pump/ec/a",
                   "Esp8266!D4ta/10370007/pump/ec/b"
                  };



// Update these with values suitable for your network.
const char* ssid = "Nombre de la red wifi";
const char* password = "Clave de la red wifi";
const char* mqtt_server = "Url del broker";

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

//***********************************************************************//
//                            SetDateTime
//***********************************************************************//


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


//***********************************************************************//
//                            Callback
//***********************************************************************//


void callback(char* topic, byte* payload, unsigned int length) {
	Serial.print("Message arrived [");
	Serial.print(topic);
	Serial.print("] ");
  Serial.println();

	char* payload_char = (char*)payload;

  Serial.print("Message: ");
  Serial.print(payload_char);
  Serial.println();

  for (int i = 0; i < 4; i++){

    char txt_buffer[40];
    sprintf(txt_buffer, "Tema numero %d, %s", i, topics[i]);
    Serial.println(txt_buffer);
    
    String t1 =  (String)topic; 
    String t2 =  (String)(char *)topics[i];
    
    // checks whether the topic is in the topics list 
    // and which of all topics it is
    if (t1 == t2){
       
        // Switch on the LED if the first character is present
        if (payload_char[0] != NULL) {

          Serial.print("Si hay mensaje ...");
          digitalWrite(LED_BUILTIN, LOW);   // Turn the LED on (Note that LOW is the voltage level
                                            // but actually the LED is on; this is because
                                            // it is active low on the ESP-01)
          delay(500);
          digitalWrite(LED_BUILTIN, HIGH);  // Turn the LED off by making the voltage HIGH
      
          Serial.print("PAYLOAD en enteros: ");
          Serial.println(payload_char);
          Serial.println(payload_char[0]);
      

          // turns on or off the selected pump
          if(payload_char[0] == '1'){
            digitalWrite(pins[i], HIGH);
            sprintf(txt_buffer, "Encendiendo bomba número %d", i);
            Serial.println(txt_buffer);
                  
          }else if(payload_char[0] == '0'){
      
            digitalWrite(pins[i], LOW);
            sprintf(txt_buffer, "Apagando bomba número %d", i);
            Serial.println(txt_buffer);
      
          }

          break;
          
        } else {
      
          digitalWrite(LED_BUILTIN, HIGH); // Turn the LED off by making the voltage HIGH
      
        }

        Serial.println();
        Serial.println("---------------------------------");
    }
    
  } //end of for loop



	
} //end of function declaration


//***********************************************************************//
//                            Reconnect
//***********************************************************************//


void reconnect() {
  
	// Loop until we’re reconnected
	while (!client->connected()) {

		Serial.print("Attempting MQTT connection…");
		String clientId = "Identificador del usuario mqtt o cliente mqtt";

		// Attempt to connect
		// Insert your password

		if (client->connect(clientId.c_str(), "Nombre de usuario mqtt", "Contraseña de usuario mqtt")) {
			Serial.println("connected");

			// Once connected
			// … resubscribe


      client->subscribe(topics[0]);
      client->subscribe(topics[1]);
      client->subscribe(topics[2]);
      client->subscribe(topics[3]);


		} else {
			Serial.print("failed, rc = ");
			Serial.print(client->state());
			Serial.println(" try again in 5 seconds");
			// Wait 5 seconds before retrying
			delay(5000);

		}
	}
  
}



//***********************************************************************//
//                            Setup Connection
//***********************************************************************//


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





//**************************************************************//
//                            Setup
//**************************************************************//


void setup() {
  
	setup_connection();

  // Initialize pin as an output

  for (int i = 0; i < 4; i++){
    pinMode(pins[i], OUTPUT);

    //Turns off and on the pin, to test if all alright
    digitalWrite(pins[i], HIGH);
    delay(700);
    digitalWrite(pins[i], LOW);
  }


	// Inicializa el canal I2C (la librería BH1750 no hace esto directamente)
	Wire.begin();
}




//**************************************************************//
//                            Loop
//**************************************************************//

void loop() {
	if (!client->connected()) {
		reconnect();
	}
	client->loop();
}
