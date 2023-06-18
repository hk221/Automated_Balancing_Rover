#include <ArduinoJson.h>
#include <ArduinoJson.hpp>
#include <Arduino_JSON.h>
#include <WiFi.h>
#include <ArduinoHttpClient.h>
#include <HardwareSerial.h>
#include <string.h>
#include <math.h>
#include <Arduino.h>

// Motor pins
#define dirPin 12
#define stepPin 14
#define dirPin2 26
#define stepPin2 27
int xCoordinate;
int yCoordinate;

// LDR pins
const int analogPin1 = 36;  // GPIO 36 corresponds to analog input 0
const int analogPin2 = 39;  // GPIO 39 corresponds to analog input 1
const int analogPin3 = 32;  // GPIO 32 corresponds to analog input 2
const int analogPin4 = 33;  // GPIO 33 corresponds to analog input 3

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
  // Configure motor pins as outputs
  pinMode(dirPin, OUTPUT);
  pinMode(stepPin, OUTPUT);
  pinMode(dirPin2, OUTPUT);
  pinMode(stepPin2, OUTPUT);
  
  // Configure LDR pins as inputs
  pinMode(analogPin1, INPUT);
  pinMode(analogPin2, INPUT);
  pinMode(analogPin3, INPUT);
  pinMode(analogPin4, INPUT);

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
void performStep() {
  digitalWrite(stepPin, HIGH);
  digitalWrite(stepPin2, HIGH);
  delayMicroseconds(2000);
  digitalWrite(stepPin, LOW);
  digitalWrite(stepPin2, LOW);
  delayMicroseconds(2000);
}
void loop() {
    // Read voltage values from LDR pins
  int value1 = analogRead(analogPin1);
  int value2 = analogRead(analogPin2);
  int value3 = analogRead(analogPin3);
  int value4 = analogRead(analogPin4);

  // Set the corresponding bit to 1 if the analog value is higher than 2500
  byte bits = 0;
  if (value1 > 2500) {
    bits |= 0b0001;
  }
  if (value2 > 2500) {
    bits |= 0b0010;
  }
  if (value3 > 2500) {
    bits |= 0b0100;
  }
  if (value4 > 2500) {
    bits |= 0b1000;
  }

// Print the 4-bit number to Serial Monitor
  Serial.print("Analog Inputs: ");
  Serial.println(bits, BIN);
  if (bits == 0b0001){
    // These four lines result in 1 step:
    digitalWrite(dirPin, HIGH);
    digitalWrite(dirPin2, HIGH);
    digitalWrite(stepPin, HIGH);
    digitalWrite(stepPin2, HIGH);
    delayMicroseconds(2000);
    digitalWrite(stepPin, LOW);
    digitalWrite(stepPin2, LOW);
    delayMicroseconds(2000);
    Serial.print("if statemet");
  }
  else if(bits == 0b0010){
    digitalWrite(dirPin, LOW);
    digitalWrite(dirPin2, LOW);
    digitalWrite(stepPin, HIGH);
    digitalWrite(stepPin2, HIGH);
    delayMicroseconds(2000);
    digitalWrite(stepPin, LOW);
    digitalWrite(stepPin2, LOW);
    delayMicroseconds(2000);
    Serial.print("else if statemet");
  }
  else if (bits == 0b0100){
    // These four lines result in 1 step:
    digitalWrite(stepPin, HIGH);
    digitalWrite(stepPin2, LOW);
    delayMicroseconds(2000);
    digitalWrite(stepPin, LOW);
    digitalWrite(stepPin2, LOW);
    delayMicroseconds(2000);
    Serial.print("if statemet");
  }
  else if (bits == 0b1000){
    digitalWrite(stepPin, LOW);
    digitalWrite(stepPin2, HIGH);
    delayMicroseconds(2000);
    digitalWrite(stepPin, LOW);
    digitalWrite(stepPin2, LOW);
    delayMicroseconds(2000);
    Serial.print("if statemet");
  }
  else{
    digitalWrite(stepPin, HIGH);
    digitalWrite(stepPin2, HIGH);
    delayMicroseconds(2000);
    digitalWrite(stepPin, LOW);
    digitalWrite(stepPin2, LOW);
    delayMicroseconds(2000);
    Serial.print("else statemet");

  }
  delay (1000);

  receiveDataFromFPGA();
  sendData(xCoordinate, yCoordinate);
}

void receiveDataFromFPGA() {
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

void receiveDataFromServer(int& x, int& y) {
  // Make a GET request to fetch the coordinates from the server
  client.get("/coordinates");

  // Read the response from the server
  String response = client.responseBody();

  // Parse the JSON response
  DynamicJsonDocument doc(1024); // Adjust the size based on your JSON payload size
  DeserializationError error = deserializeJson(doc, response);

  // Check if parsing succeeded
  if (error) {
    Serial.print("Error parsing JSON: ");
    Serial.println(error.c_str());
    return;
  }
  // Check if the JSON response is an array and has at least one element
  if (doc.is<JsonArray>() && doc.size() >= 1) {
    // Extract the first set of coordinates
    JsonObject firstCoordinates = doc[0].as<JsonObject>();

    // Check if the extracted coordinates are objects
    if (firstCoordinates.containsKey("x") && firstCoordinates.containsKey("y")) {
      // Retrieve the x and y coordinates from the JSON object
      x = firstCoordinates["x"].as<int>();
      y = firstCoordinates["y"].as<int>();
    }
  }
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
