const int analogPin1 = 36;  // GPIO 36 corresponds to analog input 0
const int analogPin2 = 39;  // GPIO 39 corresponds to analog input 1
const int analogPin3 = 32;  // GPIO 32 corresponds to analog input 2
const int analogPin4 = 33;  // GPIO 33 corresponds to analog input 3

void setup() {
  // Setup Serial communication for debugging (optional)
  Serial.begin(9600);
  
  // Configure analog pins as inputs
  pinMode(analogPin1, INPUT);
  pinMode(analogPin2, INPUT);
  pinMode(analogPin3, INPUT);
  pinMode(analogPin4, INPUT);
}

void loop() {
  // Read voltage values from analog pins
  int value1 = analogRead(analogPin1);
  int value2 = analogRead(analogPin2);
  int value3 = analogRead(analogPin3);
  int value4 = analogRead(analogPin4);

  // Process the voltage values
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

  delay(1000); // Delay between readings (adjust as needed)
}