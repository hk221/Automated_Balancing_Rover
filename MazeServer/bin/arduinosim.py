#Script to simulate requests to the server from arduino 

import socketio
import time, msvcrt, sys

# Create a Socket.IO client instance
sio = socketio.Client()

# Connect to the server
sio.connect("http://localhost:3000")
print ("Connected")

@sio.event
def UpdateCoords(x, y):
    print("Sending: "+str(x) + " "+ str(y))

    # Simulate sending new x and y values
    sio.emit("serverUpdateCoordsAbs", {"x": x, "y": y})

@sio.event
def testRotateBug():
    
    for i in range(0, 360):
        print ("Rotating by "+str(i))
        sio.emit("serverUpdateRotate", {"angle": i})
        time.sleep(0.2)

        if msvcrt.kbhit() and ord(msvcrt.getch()) == 13:
            print("Script stopped by user.")
            sio.disconnect()
            sys.exit()
        sio.disconnect()
        sys.exit()

@sio.event
def disconnect():
    print("Disconnected from server")

def testMoveBug():
    x = 30
    y = 30
    for i in range (0, 200):

        UpdateCoords(x, y)
        x+=10
        y+=12
        time.sleep(0.35)
        # Check if Enter key was pressed to stop the script
        
        if msvcrt.kbhit() and ord(msvcrt.getch()) == 13:
            print("Script stopped by user.")
            sio.disconnect()
            sys.exit()
    sio.disconnect()
    sys.exit()
            
testMoveBug()
# testRotateBug()

disconnect()
sys.exit()