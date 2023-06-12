const express = require("express");
const app = express();
const http = require("http").createServer(app);
const bodyParser = require("body-parser");
const path = require("path"); // Import the 'path' module
const cors = require("cors");


app.use(cors({origin:'*'}));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));
app.use(express.json());

let acc = ""; // Declare the global variable acc

// Receives Arduino data, processes it, and stores it in the acc variable
app.post("/acc", (req, res) => {
  const now = new Date();
  const hours = now.getHours().toString().padStart(2, "0");
  const minutes = now.getMinutes().toString().padStart(2, "0");
  const seconds = now.getSeconds().toString().padStart(2, "0");
  console.log(`${hours}:${minutes}:${seconds}`);
  acc = JSON.stringify(req.body); // Assign value to the global variable acc
  console.log("got acc" );
  res.writeHead(200, { "Content-Type": "text/plain" });
  res.end("Got Acc");
});

// Serve the script.js file
// app.get("/bad.js", (req, res) => {
//   const scriptPath = path.join(__dirname, "bad.js");
//   res.sendFile(scriptPath);
// });



// Displays the acc readings on the website
app.get("/acc", (req, res) => {
  const now = new Date();
  const hours = now.getHours().toString().padStart(2, "0");
  const minutes = now.getMinutes().toString().padStart(2, "0");
  const seconds = now.getSeconds().toString().padStart(2, "0");
  let c = hours + minutes + seconds + ":" + acc;
  res.send(c);
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
</body>
</html>`;

app.get("/", (req, res) => {
   res.send(htmlContent);
 });

app.listen(3000, "0.0.0.0", () => {
  console.log("Server started");
});
