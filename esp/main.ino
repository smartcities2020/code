#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <Servo.h>
#include <ArduinoJson.h>

 
const char* SSID = "xxx";
const char* PSK = "xxxxx";
const char* MQTT_BROKER = "xxx.xxx.xxx";
 
WiFiClient espClient;
PubSubClient client(espClient);
long lastMsg = 0;
char msg[50];
int value = 0;
 
const int analogInPin = A0;  // ESP8266 Analog Pin ADC0 = A0

int sensorValue = 0;  // value read from the pot
int outputValue = 0;  // value to output to a PWM pin

Servo servo0;
Servo servo1;

StaticJsonBuffer<200> jsonBuffer;

void setup() {
  // initialize serial communication at 115200
  Serial.begin(115200);
  setup_wifi();
  
  client.setServer(MQTT_BROKER, 1883);
  client.setCallback(callback);
      
  servo0.attach(2); 
  servo0.write(0);

  servo1.attach(13); 
  servo1.write(0);
}

void loop() {
  // read the analog in value
  sensorValue = analogRead(analogInPin);  
  // the analog value to 1 byte
  outputValue = map(sensorValue, 0, 1023, 0, 255);
    
  if (!client.connected()) {
      reconnect();
  }
  client.loop();

  snprintf (msg, 50, "%ld", outputValue);
  
  client.publish("/sensors/light", msg);
    
  delay(1000);
}


void callback(char* topic, byte* payload, unsigned int length) {

    char msg[length+1];
    for (int i = 0; i < length; i++) {
        Serial.print((char)payload[i]);
        msg[i] = (char)payload[i];
    }
    
    msg[length] = '\0';

    JsonObject& root = jsonBuffer.parseObject(payload);
    if (!root.success()) {
      Serial.println("parseObject() failed");
      return;
    }
    
    long pos = root["pos"];

    //decide on which servo to move
    if(strcmp(topic,"/commands/servo0")){
      servo0.write(pos);
    }    
    if(strcmp(topic,"/commands/servo1")){
      servo1.write(pos);
    }
    
    Serial.println(msg);
 
}


void setup_wifi() {
    delay(10);
    Serial.println();
    Serial.print("Connecting to ");
    Serial.println(SSID);
 
    WiFi.begin(SSID, PSK);
 
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }
 
    Serial.println("");
    Serial.println("WiFi connected");
    Serial.println("IP address: ");
    Serial.println(WiFi.localIP());
}
 
void reconnect() {
    while (!client.connected()) {
        Serial.print("Reconnecting...");
        if (!client.connect("ESP8266Client","xxxxx","xxxxxxxxx")) {
            Serial.print("failed, rc=");
            Serial.print(client.state());
            Serial.println(" retrying in 5 seconds");
            delay(5000);
        }
    }
    client.subscribe("/commands/servo0");
    client.subscribe("/commands/servo1");
    Serial.print("Connected");
}
