import socket
import time
import asyncio
import websockets
import numpy as np
from collections import deque

# Socket communication setup
server_address = 'localhost'  # Change to the appropriate server address
server_port = 1234  # Change to the appropriate server port
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((server_address, server_port))

async def read_from_websocket():
    async with websockets.connect('ws://localhost:8765') as websocket: # Replace with your WebSocket server URL
        while True:
            response = await websocket.recv()
            process_websocket_data(response)


# Maze dimensions 280 x 360cm
# Cell size 2x2
# Calculate the number of cells in each dimension
width = 140
height = 180

start_x = 0
start_y = 0
start_orientation = 0
current_position = [start_x, start_y]  #Initialise with the starting position
current_orientation = start_orientation  #Initialise with the starting orientation


# works if receiving e.g. "turn right 45" 
def process_websocket_data(response):
    global x, y, theta, wheel_revolutions

    if response.startswith("turn"):
        # Extract the turn angle from the response string
        angle = int(response.split()[-1])
        wheel_revolutions = 25 

        # Update the orientation angle accordingly
        if "right" in response:
            theta += angle
        elif "left" in response:
            theta -= angle
    else:
        #its just moving forward
        wheel_revolutions = 200
        pass

    # Process other types of data received from Arduino
    # .
    
def update_position_and_orientation(distance):
    global x, y, theta

    # Convert the distance traveled to coordinates update
    dx = distance * np.cos(np.radians(theta))
    dy = distance * np.sin(np.radians(theta))
    # Update the position
    x += dx
    y += dy

def main():
    # Start reading data from the WebSocket
    asyncio.get_event_loop().run_until_complete(read_from_websocket())

    #implement loop?

    # Example usage: Update the position based on wheel revolutions
    wheel_radius = 5  # Radius of the wheels in centimeters
    distance = 2 * np.pi * wheel_radius * wheel_revolutions

    # Update the position and orientation based on the distance traveled
    update_position_and_orientation(distance)

    # Print the updated position and orientation
    print(f"Current position: ({x}, {y})")
    print(f"Current orientation: {theta} degrees")

if __name__ == '__main__':
    main()