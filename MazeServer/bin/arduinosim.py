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
def sendRotate(angle):
    sio.emit("serverUpdateRotate", {"angle": angle})

def testRotateBug():
    
    for i in range(0, 12):

        sendRotate(30)
        time.sleep(0.4)

        if msvcrt.kbhit() and ord(msvcrt.getch()) == 13:
            print("Script stopped by user.")
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


@sio.event
def sendMoveRel(direction, distance):
    sio.emit("moveRelDirection", {"direction": direction, "distance": distance})

def testMoveRelBug():
    for i in range(1, 50):
        sendMoveRel("forward", 30)
        time.sleep(0.1)
    for i in range(1, 50):
        sendMoveRel("right", 30)
        time.sleep(0.1)
    for i in range(1, 50):
        sendMoveRel("back", 30)
        time.sleep(0.1)
    for i in range(1, 50):
        sendMoveRel("left", 30)
        time.sleep(0.1)


    if msvcrt.kbhit() and ord(msvcrt.getch()) == 13:
        print("Script stopped by user.")
        sio.disconnect()
        sys.exit()


            
# testMoveBug()
testRotateBug()
testMoveRelBug()

disconnect()
sio.disconnect()
sys.exit()
