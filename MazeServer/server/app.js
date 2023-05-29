// Import the required modules
var express = require("express");
var server = express();
server.use(express.static(__dirname));

var http = require("http").Server(server);
var io = require("socket.io")(http);

var socket_list = {};
var x = 0;
var y = 0;

class prevPos {
  constructor(X, Y, Angle){
    this.X = X;
    this.Y = Y;
    this.angle = Angle;
  }
}
let prevPosLog = [];

// Configure bodyParser middleware
server.use(express.json());
server.use(express.urlencoded({ extended: true }));

// Handle new client connections
io.on("connection", function(socket) {
  console.log("New socket connection");

  // Assign random id to new connection
  socket.id = Math.random();
  socket.x = 0;
  socket.y = 1;

  // Append to connection list
  socket_list[socket.id] = socket;

  
  socket.on("serverUpdateRotate", function(data){

    io.sockets.emit("clientUpdateRotate", {angle: data.angle});
  });

  socket.on("serverUpdateCoordsAbs", function(data){

    io.sockets.emit("clientUpdateCoordsAbs", {x: data.x, y: data.y});
  });

  socket.on("moveRelDirection", function(data){

    io.sockets.emit("moveRelDirection", {direction: data.direction, distance: data.distance});
  });

  socket.on("requestTrail", function(){
    socket.emit("prevPosLog", {prevPosLog:prevPosLog});
  });
    
  socket.on("addPos", function(data){
    prevPosLog.push(data.Pos);
  });


 

  // Listen for socket disconnect
  socket.on("disconnect", function() {
    delete socket_list[socket.id];
  });
});

// Handle Arduino HTTP requests
// server.post("/update", function(req, res) {
//   x = req.body.x;
//   y = req.body.y;
//   res.sendStatus(200);
// });

// Send Variable Update to clients
setInterval(function() {
  for (var i in socket_list) {
    var socket = socket_list[i];
    socket.x = x;
    socket.y = y;
    socket.emit("newvar", { x: socket.x, y: socket.y });
  }
});

// Serve HTML to client
server.get("/", function(req, res) {
  res.sendFile(__dirname + "/client/index.html");
});

// Start the server
var serverInstance = http.listen(3000, "0.0.0.0", function() {
  var host = serverInstance.address().address;
  var port = serverInstance.address().port;
  console.log("Server is running on http://%s:%s", host, port);
});


// Listen for the Enter key press to terminate the script
var readline = require("readline");
var rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

rl.on("line", function(input) {
  if (input === "") {
    console.log("Terminating the script...");
    rl.close();
    process.exit();
  }
});