var socket = io();
var canvas = document.getElementById("ctx");
var c = canvas.getContext("2d");
//-----MAZE CANVAS AND MAINTENANCE----//
// Set dimensions based on the window size
var bugWidth, mm;
function screenSize(){

  if ((2.4/3.6)*window.innerWidth >= window.innerHeight){
    canvas.height = window.innerHeight*0.85;
    canvas.width = canvas.height*(3.6/2.4);
  }
  else{
    canvas.width = window.innerWidth*0.85;
    canvas.height = canvas.width*(2.4/3.6);
  }
  mm = canvas.width/3600;
  bugWidth = 300*mm;
};
screenSize();

//Update the canvas dimensions on window resize
window.addEventListener("resize", function(){reSize()});
//----------------------------------------//

// Discretize Maze
var cellSize = 20; // Size of each cell in the maze, in mm.
var numCellsX = Math.floor(canvas.width / (cellSize * mm)); // Number of cells in the x direction.
var numCellsY = Math.floor(canvas.height / (cellSize * mm)); // Number of cells in the y direction.


// Initialize a 2D array to represent the maze.
var mazeData = [];
for (var i = 0; i < numCellsY; i++) {
  mazeData[i] = [];
  for (var j = 0; j < numCellsX; j++) {
    mazeData[i][j] = 0; // Initialize all cells as open space.
  }
}

mazeData[10][20] = 1;

for (var y = 0; y < numCellsY; y++) {
  for (var x = 0; x < numCellsX; x++) {
    if (mazeData[y][x] === 1) {
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
//Draw Bug Init
c.fillStyle="red";
c.fillRect(20*mm, 20*mm, bugWidth, bugWidth);//Assuming LED strips 20mm




// function heyserver(){
//   socket.emit("hi server");
// }

