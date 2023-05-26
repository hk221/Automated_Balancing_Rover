var socket = io();
var canvas = document.getElementById("ctx");
var c = canvas.getContext("2d");
//-----MAZE CANVAS AND MAINTENANCE----//
// Set dimensions based on the window size


var bugWidth, bugHeight, mm, bugX, bugY, bugAngle, numCellsY, numCellsX, cellSize;
let mazeMatrix = [];



function screenSize(){

  if ((2.4/3.6)*window.innerWidth >= window.innerHeight){
    canvas.height = window.innerHeight*0.85;
    canvas.width = canvas.height*(3.6/2.4);
  }
  else{
    canvas.width = window.innerWidth*0.85;
    canvas.height = canvas.width*(2.4/3.6);
  }
  //Calibrate units
  mm = canvas.width/3600;
  bugWidth = 300*mm;
  bugHeight = 300*mm;
  c.fillStyle = "lightgrey";
  c.fillRect(0, 0, canvas.width, canvas.height);
  cellSize = 20;  // Size of each cell in the maze, in mm. e.g. If cellsize = 20mm, maze dimensions will be 3600/20 = 180cells wide, 2400/20 =120cells height

  if (mazeMatrix.length==0){// Initialize a matrix to represent the maze.
    console.log("init maze matrix");
    numCellsX = 3600/cellSize;;//Math.floor(canvas.width / (cellSize * mm)); // Number of cells in the x direction.
    numCellsY = 2400/cellSize;//Math.floor(canvas.height / (cellSize * mm)); // Number of cells in the y direction.
    for (var i = 0; i < numCellsY; i++) {
      mazeMatrix[i] = [];
      for (var j = 0; j < numCellsX; j++) {
        mazeMatrix[i][j] = 0; // Initialize all cells as open space.
      }
    }
    for (var y = 0; y < numCellsY; y++) {
      for (var x = 0; x < numCellsX; x++) {
        if (mazeMatrix[y][x] === 1) {
          // Draw a wall.
          c.fillStyle = 'red';
          c.fillRect(x * cellSize * mm, y * cellSize * mm, cellSize * mm, cellSize * mm);
        } else {
          // Draw an open space.
          c.fillStyle = 'white';
          c.fillRect(x * cellSize * mm, y * cellSize * mm, cellSize * mm, cellSize * mm);
        }
      }
    }
    bugX = bugY = 20*mm;
    bugAngle = 0;
    drawBug(bugX, bugY, bugAngle);
}
  else{
    console.log("maze draw again");
    syncMatrixMaze();
    drawBug(bugX, bugY, bugAngle);
  }
}

screenSize();


//Update the canvas dimensions on window resize
window.addEventListener("resize", function(){screenSize()});
//----------------------------------------//

// Discretize Maze


function syncMatrixMaze(){
  for (var y = 0; y < numCellsY; y++) {
    for (var x = 0; x < numCellsX; x++) {
      if (mazeMatrix[y][x] === 1) {
        // Draw a wall.
        c.fillStyle = 'red';
        c.fillRect(x * cellSize * mm, y * cellSize * mm, cellSize * mm, cellSize * mm);
      } else {
        // Draw an open space.
        c.fillStyle = 'white';
        c.fillRect(x * cellSize * mm, y * cellSize * mm, cellSize * mm, cellSize * mm);
      }
    }
  }
}







//Draw Bug Init
function drawBug(X, Y, angle, colour="red", clear=0) {
  c.save(); // Save the current context state
  c.translate(X+bugWidth/2, Y+bugHeight/2); // Translate origin to the bug centre for centre of rotation
  c.rotate(angle); // Rotate the context
  c.translate(-X-bugWidth/2, -Y-bugHeight/2);
  // c.translate(-X - bugWidth / 2, -Y - bugHeight / 2); // Reset Origin to top left of context
  c.fillStyle = colour;
  c.fillRect(Math.floor(X-clear/2), Math.floor(Y-clear/2), Math.floor(bugWidth+clear), Math.floor(bugHeight+clear)); // Assuming LED strips 20mm
  c.restore(); // Restore the context state
}




function moveBugRelative(dx, dy) {
  // Clear the bug's current position.
  //c.fillRect(bugX-1, bugY-1, bugWidth+2, bugWidth+2); //slightly incremented due to browser anti-aliasing
  drawBug(bugX, bugY, bugAngle, "blue", 2);

  // Update the bug's position.
  bugX += dx * mm;
  bugY += dy * mm;

  // Draw the bug at the new position.
  //socket.emit("bugCoordinates", { x: bugX, y: bugY });
  drawBug(bugX, bugY, bugAngle);
  
}

function moveBugAbsolute(X, Y){
  //clear bug
  drawBug(bugX, bugY, bugAngle, "blue", 2);
  bugX = X * mm;
  bugY = Y*mm;
  drawBug(bugX, bugY, bugAngle);
}

function rotateBugAbsolute(angle){
  //clear bug
  drawBug(bugX, bugY, bugAngle, "blue", 2)
  bugAngle += angle*Math.PI/180;
  drawBug(bugX, bugY, bugAngle);
}

function rotateBugRelative(angle){
    var newAngle = angle+bugAngle*180/Math.PI;
    rotateBugAbsolute(bugAngle+angle);
}




socket.on("clientUpdateCoordsAbs", function(data){
  moveBugAbsolute(data.x, data.y);
});

// function locationUpdate(){
//   socket.emit("location");
// }

