var socket = io();
var canvas = document.getElementById("ctx");
var c = canvas.getContext("2d");

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

//Draw Bug Init
c.fillStyle="red";
c.fillRect(20*mm, 20*mm, bugWidth, bugWidth);//Assuming LED strips 20mm



// function heyserver(){
//   socket.emit("hi server");
// }

