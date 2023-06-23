const express = require("express");
const app = express();
const http = require("http").createServer(app);
const bodyParser = require("body-parser");
const path = require("path");
const cors = require("cors");

app.use(cors({ origin: '*' }));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));
app.use(express.json());

const HEIGHT = 480;
const WIDTH = 640;
let matrix = createEmptyMatrix();
let coordinates = [];

function createEmptyMatrix() {
  const emptyMatrix = [];
  for (let i = 0; i < HEIGHT; i++) {
    const row = new Array(WIDTH).fill(0);
    emptyMatrix.push(row);
  }
  return emptyMatrix;
}

app.post("/acc", (req, res) => {
  const now = new Date();
  const hours = now.getHours().toString().padStart(2, "0");
  const minutes = now.getMinutes().toString().padStart(2, "0");
  const seconds = now.getSeconds().toString().padStart(2, "0");
  console.log(`${hours}:${minutes}:${seconds}`);

  const receivedData = req.body;
  const xCoordinates = [];
  const yCoordinates = [];
  if (receivedData.receivedData === "WBB") {
    for (let i = 0; i < 4; i++) {
      const xCoordinate = parseInt(receivedData[`x${i}`]);
      const yCoordinate = parseInt(receivedData[`y${i}`]);
  
      if (xCoordinate >= 0 && xCoordinate < WIDTH && yCoordinate >= 0 && yCoordinate < HEIGHT) {
        xCoordinates.push(xCoordinate);
        yCoordinates.push(yCoordinate);
      }
    }
    return;
  }  

  const newMatrix = createEmptyMatrix();

  for (let i = 0; i < 4; i++) {
    const xCoordinate = xCoordinates[i];
    const yCoordinate = yCoordinates[i];

    if (xCoordinate >= 0 && xCoordinate < WIDTH && yCoordinate >= 0 && yCoordinate < HEIGHT) {
      newMatrix[yCoordinate][xCoordinate] = 1;
    }
  }

  // Fill the matrix between the four coordinates with the same numbers
  const minX = Math.min(...xCoordinates);
  const maxX = Math.max(...xCoordinates);
  const minY = Math.min(...yCoordinates);
  const maxY = Math.max(...yCoordinates);

  for (let y = minY + 1; y < maxY; y++) {
    for (let x = minX + 1; x < maxX; x++) {
      newMatrix[y][x] = 1;
    }
  }

  matrix = newMatrix;
  coordinates.push({ x: xCoordinates, y: yCoordinates, time: `${hours}:${minutes}:${seconds}` });

  // Send the filled matrix to the server
  fetch("/matrix", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(matrix)
  })
  .then(response => response.text())
  .then(data => {
    console.log("Server response:", data);
  })
  .catch(error => {
    console.log("Error:", error);
  });

  console.log("Received acc data:", receivedData);
  res.writeHead(200, { "Content-Type": "text/plain" });
  res.end("Got Acc");
});

app.get("/matrix", (req, res) => {
  res.json(matrix);
});

app.get("/coordinates", (req, res) => {
  res.json(coordinates);
});

let htmlContent = `<!DOCTYPE html>
<html>
<head>
  <title>My Website</title>
  <script src="/script.js"></script>
</head>
<body>
  <h1>My Website</h1>
  <h2>Accelerometer Readings</h2>
  <p id="acc"></p>
  <button onclick="getCoordinates()">Get Coordinates</button>
  <script>
    function getCoordinates() {
      fetch("/coordinates")
        .then(response => response.json())
        .then(data => {
          const accElement = document.getElementById("acc");
          accElement.textContent = JSON.stringify(data);
        });
    }
  </script>
</body>
</html>`;

app.get("/", (req, res) => {
  res.send(htmlContent);
});

app.listen(3000, "0.0.0.0", () => {
  console.log("Server started");
});
//need to process matrix to move rover into 0s