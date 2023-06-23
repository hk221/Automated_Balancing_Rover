#include <Arduino.h>

// Motor pins
#define dirPin 12
#define stepPin 14
#define stepsPerRevolution 200

#define dirPin2 26
#define stepPin2 27

// LDR pins
const int analogPin1 = 35;  // GPIO 36 corresponds to analog input 0
const int analogPin2 = 34;  // GPIO 39 corresponds to analog input 1
const int analogPin3 = 32;  // GPIO 32 corresponds to analog input 2
const int analogPin4 = 33;  // GPIO 33 corresponds to analog input 3

void setup() {
  Serial.begin(115200);
  
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
}


void loop() {
  // Read voltage values from LDR pins
  int value1 = analogRead(analogPin1);
  int value2 = analogRead(analogPin2);
  int value3 = analogRead(analogPin3);
  int value4 = analogRead(analogPin4);

  // Set the corresponding bit to 1 if the analog value is higher than 2500
  byte bits = 0;
  if (value1 > 4000) {
    bits |= 0b0001;
  }
  if (value2 > 4000) {
    bits |= 0b0010;
  }
  if (value3 > 4000) {
    bits |= 0b0100;
  }
  if (value4 > 4000) {
    bits |= 0b1000;
  }

 // Print the 4-bit number to Serial Monitor
  Serial.print("Analog Inputs: ");
  Serial.println(bits, BIN);
  // 0001 -> front ldr(bluepin35), 0010 -> back ldr (yellowpin34), 0100 ->right ldr(purplepin32), 1000 -> left ldr (orangepin33)
  if (bits == 0b1001){
    //turn right at corner
    for(int i=0;i<200;i++){
      turnRight();
    }
    Serial.print("if statemet moveback");
  }
  else if (bits == 0b0101){
    //turn left at corner
    for(int i=0;i<200;i++){
      turnLeft();
    }
    Serial.print("if statemet moveback");
  }
  else if (bits == 0b1101 || bits == 0b1111){
    //deadend -> server needs to tell esp to do opposite of recorded motor movements in branch 
   Serial.print("else if statemet backldr");
  }
  else if (bits == 0b1100){
      //left and right high -> go forward
    for(int i=0;i<200;i++){
      performStep();
    }
   Serial.print("if statemetright");
  }
  else if (bits == 0b1000 || bits== 0b0100 || bits == 0b0001 || bits == 0b0010){
    //left or right high -> check server
    //tell server theres a new node, ask which way to go
    for(int i=0;i<200;i++){
      performStep();
    }
   Serial.print("if statemet leftldr");
  }
  else{
    performStep();
   Serial.print("no movement");
  }
}

void turnLeft(){
  digitalWrite(stepPin, HIGH);
  digitalWrite(stepPin2, LOW);
  delayMicroseconds(2000);
  digitalWrite(stepPin, LOW);
  digitalWrite(stepPin2, LOW);
  delayMicroseconds(2000);
}
void turnRight(){
  digitalWrite(stepPin, LOW);
  digitalWrite(stepPin2, HIGH);
  delayMicroseconds(2000);
  digitalWrite(stepPin, LOW);
  digitalWrite(stepPin2, LOW);
  delayMicroseconds(2000);
}
void performStep() {
  //move forward
  digitalWrite(dirPin, LOW);
  digitalWrite(dirPin2, LOW);
  delayMicroseconds(2000);
  digitalWrite(stepPin, HIGH);
  digitalWrite(stepPin2, HIGH);
  delayMicroseconds(2000);
  digitalWrite(stepPin, LOW);
  digitalWrite(stepPin2, LOW);
  delayMicroseconds(2000);
}
void reverseStep(){
  digitalWrite(dirPin, HIGH);
  digitalWrite(dirPin2, HIGH);
  delayMicroseconds(2000);
  digitalWrite(stepPin, HIGH);
  digitalWrite(stepPin2, HIGH);
  delayMicroseconds(2000);
  digitalWrite(stepPin, LOW);
  digitalWrite(stepPin2, LOW);
  delayMicroseconds(2000);
}