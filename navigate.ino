#include <AFMotor.h>
#include <opencv2/opencv.hpp>

// Define motor pins
#define MOTOR_LEFT_PIN 1
#define MOTOR_RIGHT_PIN 2

// Define maze dimensions
#define MAZE_WIDTH 2.8
#define MAZE_HEIGHT 3.6

// Create motor objects
AF_DCMotor motorLeft(MOTOR_LEFT_PIN);
AF_DCMotor motorRight(MOTOR_RIGHT_PIN);

// Function to control robot movement
void moveForward() {
  motorLeft.setSpeed(150);
  motorRight.setSpeed(150);
  motorLeft.run(FORWARD);
  motorRight.run(FORWARD);
  delay(1000); // Adjust the delay to control the robot's movement speed
  motorLeft.run(RELEASE);
  motorRight.run(RELEASE);
}

// Function to turn the robot left
void turnLeft() {
  motorLeft.setSpeed(150);
  motorRight.setSpeed(150);
  motorLeft.run(BACKWARD);
  motorRight.run(FORWARD);
  delay(500); // Adjust the delay to control the turn duration
  motorLeft.run(RELEASE);
  motorRight.run(RELEASE);
}

// Function to turn the robot right
void turnRight() {
  motorLeft.setSpeed(150);
  motorRight.setSpeed(150);
  motorLeft.run(FORWARD);
  motorRight.run(BACKWARD);
  delay(500); // Adjust the delay to control the turn duration
  motorLeft.run(RELEASE);
  motorRight.run(RELEASE);
}

// Function to process camera input and detect obstacles
bool detectObstacle() {
  // Capture camera frame
  cv::VideoCapture cap(0); // Replace '0' with the camera index if multiple cameras are connected
  if (!cap.isOpened()) {
    Serial.println("Failed to open camera");
    return false;
  }

  cv::Mat frame;
  cap.read(frame);

  // Apply image processing and obstacle detection logic here
  // ...

  // Return true if an obstacle is detected, false otherwise
  return false;
}

// Function to move the robot through the maze
void navigateMaze() {
  int currentX = 0;
  int currentY = 0;
  int currentDirection = 0; // 0 - North, 1 - East, 2 - South, 3 - West

  while (currentX < MAZE_WIDTH && currentY < MAZE_HEIGHT) {
    // Check available neighboring positions
    bool canMoveForward = !detectObstacle();
    bool canTurnLeft = !detectObstacle();
    bool canTurnRight = !detectObstacle();

    // Make a decision based on available options
    if (canMoveForward) {
      moveForward();
      if (currentDirection == 0) {
        currentY++;
      } else if (currentDirection == 1) {
        currentX++;
      } else if (currentDirection == 2) {
        currentY--;
      } else if (currentDirection == 3) {
        currentX--;
      }
    } else if (canTurnLeft) {
      turnLeft();
      currentDirection = (currentDirection + 3) % 4; // Update current direction
    } else if (canTurnRight) {
      turnRight();
      currentDirection = (currentDirection + 1) % 4; // Update current direction
    } else {
      // Handle dead-end or backtracking logic here
    }
  }
}

void setup() {
  // Initialize Serial communication if needed
  Serial.begin(9600);
}

void loop() {
  // Call the maze navigation function
  navigateMaze();
}
