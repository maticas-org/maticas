#include "/home/dave/Documents/univ/maticas_test/hive_connection/hive_connection.ino"

//librerías para los sensores
#include <Wire.h>
#include <SPI.h>
#include <BH1750.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BME280.h>

#define seaLevelPressure_Hpa (1013.25);
char *topics[] = {"Esp8266!D4ta/10370001/temp", "Esp8266!D4ta/10370001/hum",
                    "Esp8266!D4ta/10370001/pressure", "Esp8266!D4ta/10370001/lux"};

/*
 * EN ESTE CASO LOS MÓDULOS BME Y BH1750 SE VAN A USAR
 * EN CONEXIÓN I2C, EN EL ESP8266 LOS PINES SON:
 * D1 -> SCL
 * D2 -> SDA
 */

Adafruit_BME280 bme;          //I2C
BH1750 lightMeter(0x23);      //I2C

/*
 * Función que solicita las mediciones y después se las envía
 * al broker mqtt
 */
void sendata();


/*
 * Función que inicializa el bme280
 */
 
void setup_bme280(){
  // Inicializa el sensor con su dirección
  bool status = bme.begin(0x76);

  if (!status) {
    Serial.println("Could not find a valid BME280 sensor, check wiring, address, sensor ID!");
    Serial.print("SensorID was: 0x"); Serial.println(bme.sensorID(), 16);
    Serial.print("  ID of 0xFF probably means a bad address, a BMP 180 or BMP 085\n");
    Serial.print("  ID of 0x56-0x58 represents a BMP 280,\n");
    Serial.print("  ID of 0x60 represents a BME 280.\n");
    Serial.print("  ID of 0x61 represents a BME 680.\n");
  }  
}

/*
 *  Función que inicializa el bh1750
 */

void setup_bh1750(){

  // Pone la resolución más alta para el sensor BH1750
  if (lightMeter.begin(BH1750::CONTINUOUS_HIGH_RES_MODE_2)) {
    Serial.println(F("BH1750 Advanced begin"));
  } else {
    Serial.println(F("Error initialising BH1750"));
  }
}


/*
 * Función de inicialización de todo en el esp8266
 */

void setup() {
  setup_connection();
  
  // Inicializa el canal I2C (la librería BH1750 no hace esto directamente)
  Wire.begin();
  
  setup_bme280();
  setup_bh1750();
}

/*
 * Main loop
 */
 
void loop() {
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


/*
 * Función para enviar los datos
 */

#define MSG_BUFFER_SIZE_2 (800)
char topic[MSG_BUFFER_SIZE_2];

void sendata() {


  //mediciones: [temperatura, humedad, presión en hPa, lux]
  double measurement[5] = {bme.readTemperature(), bme.readHumidity(),
                            bme.readPressure()/100.0F,
                            lightMeter.readLightLevel()};

  for(int i = 0; i < 4; i++){
    
    //crea un mensaje y lo guarda en la variable msg 
    //sin imprimirlo
    snprintf(msg, MSG_BUFFER_SIZE, "%10.2f", measurement[i]);
    snprintf(topic, MSG_BUFFER_SIZE_2, "%s", topics[i]);

    
    Serial.println();
    Serial.print(topic);
    Serial.print("/");
    Serial.print(msg);
    Serial.println();

    client->publish(topic, msg);


  }
 
}
