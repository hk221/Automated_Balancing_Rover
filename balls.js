const express = require("express");
const app = express();
const http = require("http").createServer(app);
const bodyParser = require("body-parser");
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));
app.use(express.json());


//receivers arduino data processes it and prints it 
app.post("/acc", (req, res) => {
  const now = new Date();
  const hours = now.getHours().toString().padStart(2, "0");
  const minutes = now.getMinutes().toString().padStart(2, "0");
  const seconds = now.getSeconds().toString().padStart(2, "0");
  console.log(`${hours}:${minutes}:${seconds}`);
  acc = JSON.stringify(req.body); // Assign value to the global variable acc
  console.log("got acc" + JSON.stringify(req.body));
  res.writeHead(200, { "Content-Type": "text/plain" });
  res.end("Got Acc");
});


app.get("/acc", (req, res) => {

      res.send(acc);
});

//let htmlContent = `<!DOCTYPE html>
//<html>
//<head>
//  <title>My Website</title>
//</head>
//<body>
//  <h1>!!!!</h1>
//  <p>-Junaid</p>
//</body>
//</html>`;


app.listen(3000, "0.0.0.0", () => {
  console.log("started");
});