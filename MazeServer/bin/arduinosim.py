#Script to simulate requests to the server from arduino 

import socketio
import time

# Create a Socket.IO client instance
sio = socketio.Client()

# Connect to the server
sio.connect("http://localhost:3000")

@sio.event
def connect(x, y):
    print("Connected to server")

    # Emit the "hi server" event to simulate Arduino's "hi server" request
    sio.emit("hi server")
    sio.emit("startcorner", "startcorner": )

    # Simulate sending new x and y values
    sio.emit("update", {"x": x, "y": y})

@sio.event
def disconnect():
    print("Disconnected from server")

# Start the Socket.IO event loop
x = 0
y= 0
for i in range (0, 200):

    connect(x, y)
    x+=1
    y+=1
    time.sleep(0.5)

disconnect()