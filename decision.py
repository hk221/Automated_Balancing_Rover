import socket
import time
import asyncio
import websockets
import numpy as np
from collections import deque


global wheel_radius, webserver_ip
global x, y, theta, wheel_revolutions, current_position, current_orientation
theta = 0
distance = 5
wheel_radius = 3.2825 # Radius of the wheels in centimeters

webserver_ip = '172.20.10.2:3002'

async def server(websocket, path):
    async for message in websocket:
        process_websocket_data(message)

# Maze dimensions 280 x 360cm
# Cell size 10x10
width = 36
height = 28
#1008 entries in matrix:
mapping = [[0] * width for _ in range(height)]

# works if receiving e.g. "1011turnright15" 
def process_websocket_data(response):
    global x, y, theta, wheel_revolutions, current_position, current_orientation
    
    
    theta=int(response)
    

def update_position_and_orientation(distance):
    global x, y, theta, current_position, current_orientation

    # Convert the distance traveled to coordinates update
    dx = distance * np.cos(np.radians(theta))
    dy = distance * np.sin(np.radians(theta))
    # Update the position
    x += dx
    y += dy
    current_position = [x, y]
    current_orientation = theta
    send_message('serverUpdateCoordsAbs: ')
    #send coordinates to server - NOOR

# def map_path(mapping, response, x, y):
#     if theta < 0:
#         theta = theta + 360
#     while response:
#         #update_position_and_orientation(distance) 
#         mapping[x][y] = 1
#         #mapping[x][y] = 1
async def prepare_message(message):
    async with websockets.connect('ws://'+webserver_ip) as websocket:
        await websocket.send(message)

def send_message(message):
    asyncio.get_event_loop().run_until_complete(send_message(message))

def main():

    start_x = 0
    start_y = 0
    start_orientation = 0
    #current_position = [start_x, start_y] #Initialise with the starting position
    #current_orientation = start_orientation #Initialise with the starting orientation
    # Start the websocket server
    
    start_server = websockets.serve(server, '172.20.10.2', 3000)
    
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()

    #implement loop?

#     # Example usage: Update the position based on wheel revolutions
#     
#     distance = 2 * np.pi * wheel_radius * wheel_revolutions

#     # Update the position and orientation based on the distance traveled
#     update_position_and_orientation(distance)
    
        #[0, 0, 0, 0, 0]
        #[0, 0, 0, 0, 0]
        #[0, 0, 0, 0, 0]
        #[0, 0, 0, 0, 0]
        #[0, 0, 0, 0, 0]
    
    # matrix = [[0] * 5 for _ in range(5)]
    # angle = 45
    # x_val = 2
    # y_val = 3
    # result = map_path(matrix, angle, x_val, y_val)
    # Print the updated position and orientation

    print(f"Current position: ({x}, {y})")
    print(f"Current orientation: {theta} degrees")

if __name__ == 'main':
    main()