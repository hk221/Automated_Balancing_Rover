#include <WiFi.h>
#include <Arduino_JSON.h>
#include <ArduinoHttpClient.h>
#include <HardwareSerial.h>
#include <string.h>
#include <math.h>

#define RX_PIN 16
#define TX_PIN 17

HardwareSerial SerialPort(2);

char ssid[] = "96 Dalling Road";
char pass[] = "Panda123";
char server[] = "18.212.197.92";
byte ip[] = { 18, 212, 197, 92 };
WiFiClient wifi;
HttpClient client = HttpClient(wifi, server, 3000);

void setup() {
  Serial.begin(115200, SERIAL_8N1, 16, 17);

  while (WiFi.status() != WL_CONNECTED) {
    Serial.print("Attempting to connect to SSID: ");
    Serial.println(ssid);
    WiFi.begin(ssid, pass);
    delay(10000);
  }
  Serial.println("Connected to WiFi");
  printWifiStatus();
  Serial.println("\nStarting connection to server...");
  while (!client.connected()) {
    Serial.println("Connecting to server...");
    if (client.connect(ip, 3000)) {
      Serial.println("Connected to server");
    } 
    else {
      Serial.println("Connection failed");
    }
  }
}

void loop() {
  int x, y;
  receiveDataFromFPGA(x, y);
  // Use the received x and y coordinates as needed
  sendData(x, y);
  receiveDataFromServer(matrix);
}

void receiveDataFromFPGA(int& Coordinate) {
  if (Serial.available()) {
    String receivedData = Serial.readStringUntil('\n');
    Serial.println("Received coordinates: ");
    Serial.println(receivedData);
    
    String xString = receivedData.substring(5, 9); // Extract characters 5 to 8 (x coordinate)
    String yString = receivedData.substring(9);    // Extract characters 9 onwards (y coordinate)
  
    // Convert the extracted strings into integers
    xCoordinate = xString.toInt();
    yCoordinate = yString.toInt();
  }
}
void receiveDataFromServer(int& matrix) {
  // Make a GET request to fetch the coordinates from the server
  client.get("/matrix");

  // Read the response from the server
  String response = client.responseBody();

  // Parse the JSON response
  JSONVar coordinatesJson = JSON.parse(response);
  if (JSON.typeof(coordinatesJson) == JSON_ARRAY && coordinatesJson.length() >= 1) {
    // Extract the first set of coordinates
    JSONVar firstCoordinates = coordinatesJson[0];
    if (JSON.typeof(firstCoordinates) == JSON_OBJECT) {
      // Retrieve the x and y coordinates from the JSON object
      x = firstCoordinates["x"];
      y = firstCoordinates["y"];
    }
  }
}
void motoTask(int& x, int& y){
  
}
void sendData(int x, int y) {
  JSONVar imageJson;
  imageJson["x"] = xCoordinate;
  imageJson["y"] = yCoordinate;
  String accString = JSON.stringify(imageJson);
  // Send the image data to the server
  client.post("/acc", "application/json", accString);
  String response = client.responseBody();
  Serial.println(response);
}

void printWifiStatus() {
  Serial.print("SSID: ");
  Serial.println(WiFi.SSID());
  IPAddress ipAddress = WiFi.localIP();
  Serial.print("IP Address: ");
  Serial.println(ipAddress);
  long rssi = WiFi.RSSI();
  Serial.print("Signal strength (RSSI):");
  Serial.print(rssi);
  Serial.println(" dBm");
}

