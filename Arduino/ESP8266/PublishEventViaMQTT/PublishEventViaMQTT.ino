/**
 * PublishEventViaMQTT.ino
 *
 *  Created on: 08.05.2018
 *
 */

#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <string.h>
#include <ArduinoJson.h>

const char* ssid = "your-ssid";
const char* password =  "your-password";
const String deviceId = "your-device-id";
const char* deviceSecretKey = "your-device-secret-key";

const char* mqttServer = "api.wia.io";
const int mqttPort = 1883;
String topic = "devices/" + deviceId + "/events/";

WiFiClient espClient;
PubSubClient client(espClient);
StaticJsonBuffer<200> jsonBuffer;
JsonObject& root = jsonBuffer.createObject();

void setup() {
  Serial.begin(115200);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println("Connecting to WiFi..");
  }
  Serial.println("Connected to the WiFi network");

  client.setServer(mqttServer, mqttPort);

  while (!client.connected()) {
    Serial.println("Connecting to MQTT...");

    if (client.connect("ESP8266Client", deviceSecretKey, " ")) {

      Serial.println("connected");  

    } else {

      Serial.print("failed with state ");
      Serial.print(client.state());
      delay(2000);

    }
  }
}

void loop() {
  char topicChar[256];
  topic.toCharArray(topicChar, topic.length());
  
  root["name"] = "temperature";
  root["data"] = 21.5; 
  size_t len = root.measureLength();
  size_t size = len+1;
  
  char message[256];
  root.printTo(message, sizeof(message));
  Serial.println(message);
  client.publish(topicChar, message);
  delay(5000);
}