 #include "/home/dave/Documents/univ/maticas_test/hive_connection/hive_connection.ino"

// ***************************************
// *      Variables MQTT
// ****************************************
char *topics[] = {"Esp8266!D4ta/10370006/ph"};


// ***************************************
// *      Variables del sensor
// ****************************************

float calibration = 1.50; //change this value to calibrate
const int analogInPin = A0 ;
int sensorValue = 0;
unsigned long int avgValue;
float b;

int nmeasurements = 60;
int buf[60];
int temp;

/// ***************************************
// *      ordena el array y saca una media
// ****************************************

int sort_and_get_mean(int a[], int sz);


// **********************************
// *      obtiene el valor de ph
// **********************************
float get_ph();

// **********************************
// *      envia el valor de ph
// **********************************

bool send_ph_data();

void setup() {
  Serial.begin(9600);
  setup_connection();
  
}



void loop() {
  if (!client->connected()) {
    reconnect();
  }
  client->loop();

  unsigned long now = millis();
  if (now - lastMsg > 60000) {
    lastMsg = now;
    Serial.println("Iniciando proceso de toma de medidas ...");
    Serial.println();
    send_ph_data();
  }

  if (now % 10000 == 0){
    Serial.print(".");   
  }
  

}


#define MSG_BUFFER_SIZE_2 (800)
char topic[MSG_BUFFER_SIZE_2];

bool send_ph_data() {


  //mediciones: [ph]
  double measurement[1]  = { get_ph() };
  
  for(int i = 0; i < 1; i++){
    
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

  return true;
 
}



float get_ph(){
  
  Serial.println("Tomando medidas ...");
  
  for(int i=0;i< nmeasurements;i++){
    buf[i] = analogRead(analogInPin);
    delay(100);
    //delay(1000);
  }
  
  Serial.println("Medidas tomadas ...");
  Serial.println(" ");
  
  avgValue = sort_and_get_mean(buf, nmeasurements);
  Serial.println(" ");
    
  
  float pHVol=(float)avgValue*3.3/1024;
  float phValue = 3.5 * pHVol + calibration;
  
  Serial.print("sensor = ");
  Serial.println(phValue);

  return phValue;
  
}


int sort_and_get_mean(int a[], int sz){

    Serial.print("Ordenando ...");
  
    for(int i=0; i<(sz-1); i++) {
        for(int o=0; o<(sz-(i+1)); o++) {
                if(a[o] > a[o+1]) {
                    int t = a[o];
                    a[o] = a[o+1];
                    a[o+1] = t;
                }
        }
    }

    
    for(int i=0; i< sz; i++){
      Serial.print(a[i]);
      Serial.print(" ");
    }
    
    
    int mid_ini =   int(sz/4);
    int mid_end = 3*int(sz/4);
    int avg = 0;
    
    for(int i = mid_ini; i < mid_end; i++){
      avg += buf[i];
    }
    
    avg = (int) (avg/(mid_ini*2));

    return avg;
}
