#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <Wire.h>
#include <freertos/FreeRTOS.h>
#include <freertos/task.h>

Adafruit_MPU6050 mpu;

const float dt = 0.01;  // Time interval between readings (in seconds)
float angle = 0.0;      // Current angle
bool isInitialized = false;  // Flag to track initialization

// Motor pins
#define dirPin 12
#define stepPin 14
#define stepsPerRevolution 50
#define dirPin2 26
#define stepPin2 27
// Task handles
TaskHandle_t gyroTaskHandle;
TaskHandle_t motorTaskHandle;

void setup() {
  Serial.begin(115200);
  Wire.begin();

  if (!mpu.begin()) {
    Serial.println("Failed to find MPU6050 chip");
    while (1) {
      delay(10);
    }
  }

  pinMode(stepPin, OUTPUT);
  pinMode(dirPin, OUTPUT);
  pinMode(stepPin2, OUTPUT);
  pinMode(dirPin2, OUTPUT);
  // Create the tasks
  xTaskCreatePinnedToCore(gyroTask, "Gyro Task", 10000, NULL, 1, &gyroTaskHandle, 0);
  delay(500); 
  xTaskCreatePinnedToCore(motorTask, "Motor Task", 10000, NULL, 1, &motorTaskHandle, 1);
  delay(500); 
}

// Gyro task
void gyroTask(void* parameter) {
  unsigned long startTime = millis();  // Start time of the program

  while (true) {
    // Check if the initialization period has passed
    if (millis() - startTime > 5000 && !isInitialized) {
      angle = 0.0;  // Initialize the angle
      isInitialized = true;  // Set the flag to true
    }

    sensors_event_t gyro;
    mpu.getGyroSensor()->getEvent(&gyro);

    // Integrate the angular velocity to estimate the angle
    angle += gyro.gyro.y * dt;

    vTaskDelay(pdMS_TO_TICKS(10));  // Delay for 10 milliseconds
  }
}

// PID controller variables
float targetAngle = 0.0;    // Desired angle for balancing
float Kp = 5.0;             // Proportional gain
float Ki = 0.5;             // Integral gain
float Kd = 5;             // Derivative gain
float integralTerm = 0.0;   // Integral term for PID
float prevError = 0.0;      // Previous error term for PID
float pidOutput = 0.0;      // PID control signal

// Motor task
void motorTask(void* parameter) {
  while (true) {
    // Print the angle if the initialization period has passed
    if (isInitialized) {
      Serial.print("Angle: ");
      Serial.println(angle);

      // Calculate the error term for PID
      float error = targetAngle - angle;

      // Update the integral term for PID
      integralTerm += error * dt;

      // Calculate the derivative term for PID
      float derivativeTerm = (error - prevError) / dt;

      // Calculate the PID control signal
      pidOutput = Kp * error + Ki * integralTerm + Kd * derivativeTerm;

      // Update the previous error term
      prevError = error;

      // Determine the direction based on the PID control signal
      if (pidOutput > 0) {
        digitalWrite(dirPin, HIGH);
        digitalWrite(dirPin2, LOW);
        Serial.println("Moving forward");
      } else if (pidOutput < 0) {
        digitalWrite(dirPin, LOW);
        digitalWrite(dirPin2, HIGH);
        Serial.println("Moving backward");
      } else {
        digitalWrite(dirPin, LOW);
        digitalWrite(dirPin2, LOW);
        Serial.println("No movement");
      }

      // Toggle the step pins to generate step signals
      digitalWrite(stepPin, HIGH);
      digitalWrite(stepPin2, HIGH);
      delayMicroseconds(2000);
      digitalWrite(stepPin, LOW);
      digitalWrite(stepPin2, LOW);
      Serial.println("Moving");

    }

    vTaskDelay(pdMS_TO_TICKS(10));  // Delay for 10 milliseconds
  }
  printSensorValues();
}
void printSensorValues() {
  sensors_event_t a, g, temp;
  mpu.getEvent(&a, &g, &temp);

  Serial.print("Accelerometer (m/s^2): ");
  Serial.print("X = ");
  Serial.print(a.acceleration.x);
  Serial.print(", Y = ");
  Serial.print(a.acceleration.y);
  Serial.print(", Z = ");
  Serial.println(a.acceleration.z);

  Serial.print("Gyroscope (deg/s): ");
  Serial.print("X = ");
  Serial.print(g.gyro.x);
  Serial.print(", Y = ");
  Serial.print(g.gyro.y);
  Serial.print(", Z = ");
  Serial.println(g.gyro.z);
}

void loop() {
  // Empty loop
}
