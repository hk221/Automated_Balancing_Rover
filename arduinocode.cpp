#define dirPin 12
#define stepPin 14
#define dirPin2 27
#define stepPin2 26
#define stepsPerRevolution 200
#include <math.h>
#include <SPI.h>
//dimensions of image - tbc
int height ; 
int width ; 
uint16_t** image;
uint8_t receiveDataFromFPGA() {
  SPI.beginTransaction(SPISettings(1000000, MSBFIRST, SPI_MODE0)); // Adjust parameters as per your requirements
  uint8_t data = SPI.transfer(0x00); // Send a dummy byte and receive data from FPGA
  SPI.endTransaction();
  return data;
}
void triangulation(int row, int col){
  reference_points[0] = Point(x1, y1);
  reference_points[1] = Point(x2, y2);
  reference_points[2] = Point(x3, y3);
  
  distances[0] = d1;
  distances[1] = d2;
  distances[2] = d3;

  // triangulation using gtsam but idt can do that here
  float x, y;
  x, y = triangulate(reference_points, distances);
}
void setup() {
  
  pinMode(stepPin, OUTPUT);
  pinMode(dirPin, OUTPUT);
  pinMode(stepPin2, OUTPUT);
  pinMode(dirPin2, OUTPUT);

  receiverDataFromFPGA();
  // Allocate memory for the image array from fpga and ensure heoght and wodth allocated properly 
  image = new uint16_t*[height];
  for (int row = 0; row < height; row++) {
    image[row] = new uint16_t[width];
  }
  // receive the image data from the FPGA and store it in the image array created above
  for (int row = 0; row < height; row++) {
    for (int col = 0; col < width; col++) {
      //using data from fpga assign bits
      uint8_t msb = receiveDataFromFPGA(); 
      uint8_t lsb = receiveDataFromFPGA(); 
      //combine bits in array to make image matrix
      image[row][col] = (msb << 8) | lsb;
    }
  }
}
void loop() {
  // iterate over the matrix rows and columns
  for (int row = 0; row < height; row++) {
    for (int col = 0; col < width; col++) {
      // get the pixel value from the matrix
      int pixelValue = image[row][col];
      //extract the red, green, and blue components from the pixel value
      int red = (pixelValue >> 16) & 0xFF;
      int green = (pixelValue >> 8) & 0xFF;
      int blue = pixelValue & 0xFF;
      //bools to determine the color of the pixel
      bool isWhite = (red == 255 && green == 255 && blue == 255);
      bool isBlack = (red <= 30 && green <= 30 && blue <= 30);
      //actions based on the color of the pixel
      if (isWhite) {
        // turn right then go to next image
        digitalWrite(dirPin, LOW);
        digitalWrite(dirPin2, HIGH);
        break;  
      } 
      else if (isBlack) {
        //move rover 5 revolutions
        digitalWrite(stepPin, HIGH);
        digitalWrite(stepPin2, HIGH);
        delayMicroseconds(2000);
        digitalWrite(stepPin, LOW);
        digitalWrite(stepPin2, LOW);
        continue;  
      } 
      else {
        continue;
      }
    }
  }
  for (int row = 0; row < height; row++) {
    for (int col = 0; col < width; col++) {
      int pixelValue = image[row][col];

      int red = (pixelValue >> 16) & 0xFF;
      int green = (pixelValue >> 8) & 0xFF;
      int blue = pixelValue & 0xFF;
      //bool for colour comparisons
      bool isRed = (red >= 200 && green < 200 && blue < 200);
      bool isBlue = (red < 200 && green < 200 && blue >= 200);
      bool isYellow = (red >= 200 && green >= 200 && blue < 50);
      //check if colours have appeared
      int colorCount = 0;
      //checl if colours have appeared 
      if (isRed) {
        colorCount++;
      }
      if (isBlue) {
        colorCount++;
      }
      if (isYellow) {
        colorCount++;
      }
      //if more than 2 colours appeared then do triangulation (idk 2 or 3????)
      if (colorCount == 2) {
        performTriangulation(row, col);
      }
    }
  }
  for (int row = 0; row < height; row++) {
    delete[] image[row];
  }
  delete[] image;
}
//////////////////triangulation not gonna work rn -  need to add coordinates///////////////////////////
      //this converts each pixel to greyscale but dont need rn 
      //int grayValue = (pixelValue >> 16 & 0xFF) * 0.2989 +
      //                (pixelValue >> 8 & 0xFF) * 0.5870 +
      //                (pixelValue & 0xFF) * 0.1140;

      // Update the pixel value with the processed value
      //image[row][col] = grayValue;