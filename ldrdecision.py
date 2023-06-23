import socket
import time
import asyncio
import websockets
import numpy as np
from collections import deque

async def read_from_websocket():
    async with websockets.connect('ws://localhost:8765') as websocket: # Replace with your WebSocket server URL
        while True:
            response = await websocket.recv()
            # Process the received message
            #print(response)  # Example: Print the received message
            
# Socket communication setup
server_address = 'localhost'  # Change to the appropriate server address
server_port = 1234  # Change to the appropriate server port
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((server_address, server_port))

# Maze dimensions 280 x 360cm

# Cell size 2x2

# Calculate the number of cells in each dimension
width = 140
height = 180

# Initialize the walls matrix
walls_matrix = np.zeros((width, height), dtype=np.uint8)

# start and goal position
start_position = walls_matrix(0, 0)
goal_position = walls_matrix(width-1, height-1)
response = read_from_websocket()


current_pos = start_position

#path = []
#while current_pos != goal_position:
#    path
    

bits = int(response, 2)
row, col = current_pos

if bits == 0b0000:
            # No LED walls detected, handle this case
            # For example, you can skip updating the walls array for the current position
            pass
        else:
            if bits & 0b0001:
                # Wall detected in the front right
        
                walls[row+1, col] = True  # Update the row below
                
            if bits & 0b0010:
                # Wall detected at the front left
                
            if bits & 0b0100:
                # Wall detected on the right
                walls_matrix()
            if bits & 0b1000:
                # Wall detected on the left
                
            if bits & 0b0101:
                # Walls detected at the front right and right
                
            if bits & 0b1010:
                # Walls detected at the front left and left
                
            if bits & 0b0110:
                # Walls detected at the right and left
                
            if bits & 0b1001:
               
            if bits & 0b0111:
                # Walls detected at the front right, right, and left
                
            if bits & 0b1011:
                # Walls detected at the front left, right, and left
                
            if bits & 0b1101:
                # Walls detected at the front right, front left, and left
                
            if bits & 0b1110:
                # Walls detected at the front left, right, and front left
                
            if bits & 0b1111:
                # Walls detected in all four directions
                