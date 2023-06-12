#include <WiFi.h>
#include <Arduino_JSON.h>
#include <ArduinoHttpClient.h>
#include <SoftwareSerial.h>

#define RX_PIN 18
#define TX_PIN 19

SoftwareSerial uart(RX_PIN, TX_PIN);

char ssid[] = "96 Dalling Road";
char pass[] = "Panda123";  // replace with your network password
char server[] = "44.203.134.46";
byte ip[] = { 44, 203, 134, 46 };
WiFiClient wifi;
HttpClient client = HttpClient(wifi, server, 3000);
int height; //480
int width; //640
uint16_t** image;

void setup() {
  Serial.begin(9600);
  uart.begin(9600);

  while (WiFi.status() != WL_CONNECTED) {
    Serial.print("Attempting to connect to SSID: ");
    Serial.println(ssid);
    int status = WiFi.begin(ssid, pass);
    delay(10000);
  }
  Serial.println("Connected to WiFi");
  printWifiStatus();
  Serial.println("\nStarting connection to server...");
  
  // Allocate memory for the image array from fpga and ensure height and width are properly allocated
  image = new uint16_t*[height];
  for (int row = 0; row < height; row++) {
    image[row] = new uint16_t[width];
  }
  
  // receive the image data from the FPGA and store it in the image array created above
  for (int row = 0; row < height; row++) {
    for (int col = 0; col < width; col++) {
      // using data from FPGA assign bits
      uint8_t msb = receiveDataFromFPGA();
      uint8_t lsb = receiveDataFromFPGA();
      // combine bits in array to make image matrix
      image[row][col] = (msb << 8) | lsb;
    }
  }
}

void loop() {
  uint8_t receivedData = receiveDataFromFPGA();
  Serial.println(receivedData); // Print the received data for debugging
  sendData();
}


uint8_t receiveDataFromFPGA() {
  uint8_t data = 0x00; // Initialize the data variable

  uart.write(0x00); // Send a dummy byte to request data from the FPGA

  if (uart.available()) { // Check if there is data available to read
    data = uart.read();  // Read the received data
  }

  return data;
}

void sendData() {
  while (!client.connected()) {
    Serial.println("Connecting to server...");
    if (client.connect(ip, 3000)) {
      Serial.println("Connected to server");
    } else {
      Serial.println("Connection failed");
    }
  }

  // Convert the image data to a JSON string
  JSONVar imageJson;
  for (int row = 0; row < height; row++) {
    JSONVar rowJson;
    for (int col = 0; col < width; col++) {
      rowJson[col] = image[row][col];
    }
    imageJson[row] = rowJson;
  }
  String accString = JSON.stringify(imageJson);

  // Send the image data to the server
  client.beginRequest();
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
