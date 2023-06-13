#include <WiFi.h>
#include <Arduino_JSON.h>
#include <ArduinoHttpClient.h>
#include <HardwareSerial.h>

#define RX_PIN 16
#define TX_PIN 17

HardwareSerial SerialPort(2);

char ssid[] = "96 Dalling Road";
char pass[] = "Panda123";
char server[] = "54.227.172.163";
byte ip[] = {54, 227, 172, 163};
WiFiClient wifi;
HttpClient client = HttpClient(wifi, server, 3000);

float x = 250;

void setup() {
  Serial.begin(9600);
  Serial2.begin(9600);
  SerialPort.begin(9600,SERIAL_8N1, 16,17);

  while (WiFi.status() != WL_CONNECTED) {
    Serial.print("Attempting to connect to SSID: ");
    Serial.println(ssid);
    WiFi.begin(ssid, pass);
    delay(10000);
  }
  Serial.println("Connected to WiFi");
  printWifiStatus();
  Serial.println("\nStarting connection to server...");
}

void loop() {
  x=receiveDataFromFPGA();
  Serial.println("Received coordinates: ");
  Serial.println(x);
  sendData(x);
}

float receiveDataFromFPGA() {
  while (Serial2.available()) {
    // Wait until at least 1 byte is available to read
    //Serial.println("hrello");
  }

  return float(Serial2.read());
}

void sendData(float y) {
  while (!client.connected()) {
    Serial.println("Connecting to server...");
    if (client.connect(ip, 3000)) {
      Serial.println("Connected to server");
    } else {
      Serial.println("Connection failed");
    }
  }

  JSONVar imageJson;
  imageJson["accX"] = x;
  String accString = JSON.stringify(imageJson);

  // Send the image data to the server
  client.post("/acc", "application/json", accString);
  String response = client.responseBody();
  Serial.println(response);
}

void printWifiStatus() {
  Serial.print("SSID: ");
  Serial.println(WiFi.SSID());
  IPAddress ip = WiFi.localIP();
  Serial.print("IP Address: ");
  Serial.println(ip);
  long rssi = WiFi.RSSI();
  Serial.print("Signal strength (RSSI):");
  Serial.print(rssi);
  Serial.println(" dBm");
}
