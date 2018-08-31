#include <WiFi101.h>
#include <ArduinoJson.h>
#include <ArduinoHttpClient.h>

// TODO: Update this to your Wi-Fi network name (ssid) and password
const char WIFI_SSID[] = "your-wifi-ssid";
const char WIFI_PASS[] = "your-wifi-password";

// TODO: Update this to your device secret key.
// You can get this from the Wia dashboard (https://dashboard.wia.io).
// It should start with `d_sk`
const char* device_secret_key = "your-device-secret-key";

WiFiClient client;
int status = WL_IDLE_STATUS;

// Wia REST API parameters
char server[] = "api.wia.io";
char path[] = "/v1/events";
int port = 80;

HttpClient httpClient = HttpClient(client, server, port);

String dataStr;
StaticJsonDocument<200> jsonBuffer;
JsonObject& root = jsonBuffer.to<JsonObject>();

void setup() {
  // Initialize serial communications and wait for port to open
  Serial.begin(9600);

  while (!Serial) {
    ; // Wait for serial port to connect
  }

  Serial.println("Starting WiFI connection to Wia!.");

  // Attempt to connect to WiFi network
  while ( status != WL_CONNECTED) {
    Serial.print("Attempting to connect to SSID: ");
    Serial.println(WIFI_SSID);
    // Connect to WPA/WPA2 network. Change this line if using open or WEP network
    status = WiFi.begin(WIFI_SSID, WIFI_PASS);

    // Wait 5 seconds for connection
    delay(5000);
  }
}

void loop() {
  root["name"] = "temperature";
  root["data"] = 21.5;

  // If you get a connection, report back via serial
  if (client.connect(server, port)) {
    postToWia(root);
  } else {
    // If you didn't get a connection to the server
    Serial.println("Connection failed");
  }

  delay(5000); // Wait for 5 seconds to post again
}

void postToWia(JsonObject& data){
  dataStr = "";

  serializeJson(data, dataStr);

  httpClient.beginRequest();
  httpClient.post(path);
  httpClient.sendHeader("Content-Type", "application/json");
  httpClient.sendHeader("Content-Length", dataStr.length());
  httpClient.sendHeader("Authorization", "Bearer "  + String(device_secret_key));
  httpClient.beginBody();
  httpClient.print(dataStr);
  httpClient.endRequest();
}
