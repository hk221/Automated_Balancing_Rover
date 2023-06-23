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

class Wall {
  constructor(X, Y, Width, Height){
    this.X = X;
    this.Y = Y;
    this.Width = wallWidth;
    this.Height = wallHeight;
  }
}
let prevPosLog = [];
let Walls = [];


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

  socket.on("wallSize", function(data){
    wallWidth = data.width;
    wallHeight = data.height;
  })
    
  socket.on("addPos", function(data){
    prevPosLog.push(data.Pos);
  });


 socket.on("getWalls", function(){
  socket.emit("giveWalls", {walls: Walls});
 });

 socket.on("newWall", function(data){
  Walls.push(data.Wall)
 });

 // Handle Arduino messages (sent from Python OpenCV instance)
 socket.on("hello server", function(data){
  console.log("Arduino says: " + data.message);
});

  // Listen for socket disconnect
  socket.on("disconnect", function() {
    delete socket_list[socket.id];
  });
});



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
var serverInstance = http.listen(3001, "192.168.31.210", function() {
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