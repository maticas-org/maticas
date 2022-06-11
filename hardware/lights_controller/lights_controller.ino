#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <time.h>
#include <TZ.h>
#include <FS.h>
#include <LittleFS.h>
#include <CertStoreBearSSL.h>

#include <Wire.h>

// Pin D6 from esp866 is selected for controlling 
// the relay
#define relay_pin 12


// Update these with values suitable for your network.
const char* ssid = "Nombre de la red wifi";
const char* password = "Clave de la red wifi";
const char* mqtt_server = "Url del broker wifi";

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

	for (int i = 0; i < length; i++) {
		Serial.print((char)payload[i]);
	}

	Serial.println();
	Serial.println();

	char* payload_char = (char*)payload;


	// Switch on the LED if the first character is present
	if (payload_char[0] != NULL) {

		digitalWrite(LED_BUILTIN, LOW); // Turn the LED on (Note that LOW is the voltage level
		// but actually the LED is on; this is because
		// it is active low on the ESP-01)
		delay(500);
		digitalWrite(LED_BUILTIN, HIGH); // Turn the LED off by making the voltage HIGH

		Serial.print("PAYLOAD en enteros: ");
		Serial.println(payload_char);
		Serial.println(payload_char[0]);


		if(payload_char[0] == '1'){
			digitalWrite(relay_pin, HIGH);
			Serial.println("Encendiendo luces...");

		}else if(payload_char[0] == '0'){

			digitalWrite(relay_pin, LOW);
			Serial.println("Apagando  luces...");

		}
    
	} else {

		digitalWrite(LED_BUILTIN, HIGH); // Turn the LED off by making the voltage HIGH

	}
}


//***********************************************************************//
//                            Reconnect
//***********************************************************************//


void reconnect() {
  
	// Loop until we’re reconnected
	while (!client->connected()) {

		Serial.print("Attempting MQTT connection…");
		String clientId = "Identificador del cliente";

		// Attempt to connect
		// Insert your password

		if (client->connect(clientId.c_str(), "Nombre de usuario", "Clave del usuario")) {
			Serial.println("connected");

			// Once connected
			// … resubscribe

			client->subscribe("Esp8266!D4ta/10370005/lights");

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
	pinMode(relay_pin, OUTPUT); // Initialize pin as an output

	digitalWrite(relay_pin, HIGH);
	delay(1000);
	digitalWrite(relay_pin, LOW);


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


