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

# Maze dimensions
maze_width = 280
maze_height = 360

# start and goal position
start_position = (0, 0)
goal_position = (maze_width-1, maze_height-1)

# Initialize the walls array
walls = np.zeros((maze_height, maze_width), dtype=bool)

# Motor control functions
# Define your motor control functions here based on the Arduino code

# Breadth-First Search for maze exploration
def bfs(maze, start, goal):
    rows, cols = maze.shape
    visited = np.zeros((rows, cols), dtype=bool)
    queue = deque([(start, [])])

    while queue:
        current_pos, path = queue.popleft()

        if current_pos == goal:
            return path

        if visited[current_pos]:
            continue

        visited[current_pos] = True

        for neighbor in get_neighbors(current_pos):
            queue.append((neighbor, path + [neighbor]))

    return None


def get_neighbors(position):

    row, col = position
    neighbors = []

    if row > 0 and not walls[row-1, col]:
        neighbors.append((row-1, col))
    if row < maze_height-1 and not walls[row+1, col]:
        neighbors.append((row+1, col))
    if col > 0 and not walls[row, col-1]:
        neighbors.append((row, col-1))
    if col < maze_width-1 and not walls[row, col+1]:
        neighbors.append((row, col+1))

    return neighbors

def get_current_coordinates():
    # Implement your function to get the current coordinates of the rover
    # Replace this with your actual implementation
    return 0, 0


def update_path(current_pos, next_pos, path):
    # Update the path with the current position and the next position
    path.append(current_pos)
    path.append(next_pos)


# Main program
def main():

    # Run Dijkstra's algorithm
    distances, previous = bfs(walls, start_position, goal_position)

    # Determine the shortest path
    path = []
    current_pos = goal_position
    path.append(start_position)
    while current_pos != goal_position:
        path.append(current_pos)
        current_pos = previous[current_pos]
    path.append(start_position)
    path.reverse()

    # Execute the movements based on the shortest path
    for i in range(len(path)-1):
        current_pos = path[i]
        next_pos = path[i+1]
        
        #define decision
        response=read_from_websocket()
        # Get the current and next coordinates
        current_coordinates = get_current_coordinates()
        
        # Process the sensor readings to update the walls array
        # this part is just to update the walls- not to do with decision!!
        bits = int(response, 2)
        row, col = current_pos
        if bits == 0b0000:
            # No LED walls detected, handle this case
            # For example, you can skip updating the walls array for the current position
            pass
        else:
            if bits & 0b0001:
                # Wall detected in the front
                walls[row+1, col] = True  # Update the row below
            if bits & 0b0010:
                # Wall detected at the back
                walls[row-1, col] = True  # Update the row above
            if bits & 0b0100:
                # Wall detected on the right
                walls[row, col+1] = True  # Update the column to the right
            if bits & 0b1000:
                # Wall detected on the left
                walls[row, col-1] = True  # Update the column to the left
            if bits & 0b0101:
                # Walls detected at the front and right
                walls[row+1, col+1] = True  # Update the row below and the column to the right
            if bits & 0b1010:
                # Walls detected at the back and left
                walls[row-1, col-1] = True  # Update the row above and the column to the left
            if bits & 0b0110:
                # Walls detected at the right and left
                walls[row, col+1] = True  # Update the column to the right
                walls[row, col-1] = True  # Update the column to the left
            if bits & 0b1001:
                # Walls detected at the front and left
                walls[row+1, col-1] = True  # Update the row below and the column to the left
            if bits & 0b0111:
                # Walls detected at the front, right, and left
                walls[row+1, col+1] = True  # Update the row below and the column to the right
                walls[row, col-1] = True  # Update the column to the left
            if bits & 0b1011:
                # Walls detected at the back, right, and left
                walls[row-1, col+1] = True  # Update the row above and the column to the right
                walls[row, col-1] = True  # Update the column to the left
            if bits & 0b1101:
                # Walls detected at the front, back, and left
                walls[row+1, col-1] = True  # Update the row below and the column to the left
                walls[row-1, col-1] = True  # Update the row above and the column to the left
            if bits & 0b1110:
                # Walls detected at the front, back, and right
                walls[row+1, col+1] = True  # Update the row below and the column to the right
                walls[row-1, col+1] = True  # Update the row above and the column to the right
            if bits & 0b1111:
                # Walls detected in all four directions
                walls[row+1, col] = True  # Update the row below
                walls[row-1, col] = True  # Update the row above
                walls[row, col+1] = True

        
        # Determine the movement commands based on the determined direction and sensor readings
        if current_pos[0] < next_pos[0]:
            # Move forward
            if bits == 0b0000:
                # No LED walls detected, handle this case
                decision = "move_forward()"
            elif walls[current_pos[0]+1, current_pos[1]] and walls[current_pos[0], current_pos[1]-1]:
                # Wall on the left and front, turn right
                decision = "turn_right()"
            elif walls[current_pos[0]+1, current_pos[1]]:
                # Wall in front, turn left
                decision = "turn_left()"
            elif walls[current_pos[0], current_pos[1]-1]:
                # Wall on the left, turn right
                decision = "turn_right()"
            else:
                decision = "move_forward()"

        elif current_pos[1] < next_pos[1]:
            # Turn right
            if bits == 0b0000:
                # No LED walls detected, handle this case
                decision = "move_forward()"
            elif walls[current_pos[0]+1, current_pos[1]] and walls[current_pos[0]-1, current_pos[1]]:
                # Wall in front and back, turn back
                decision = "move_back()"
            elif walls[current_pos[0]+1, current_pos[1]]:
                # Wall in front, turn left
                decision = "turn_left()"
            elif walls[current_pos[0]-1, current_pos[1]]:
                # Wall at the back, turn right
                decision = "turn_right()"
            else:
                decision = "turn_right()"

        elif current_pos[1] > next_pos[1]:
            # Turn left
            if bits == 0b0000:
                # No LED walls detected, handle this case
                decision = "move_forward()"
            elif walls[current_pos[0]+1, current_pos[1]] and walls[current_pos[0]-1, current_pos[1]]:
                # Wall in front and back, turn back
                decision = "move_back()"
            elif walls[current_pos[0]+1, current_pos[1]]:
                # Wall in front, turn right
                decision = "turn_right()"
            elif walls[current_pos[0]-1, current_pos[1]]:
                # Wall at the back, turn left
                decision = "turn_left()"
            else:
                decision = "turn_left()"


            # Determine the movement direction based on sensor readings from Arduino
            #sock.sendall(b'get_led_walls\n')            
            # Use the sensor readings to update the walls array dynamically
            
        sock.sendall(decision.encode())
        
        time.sleep(1)  # Add a delay to allow the robot to complete the movement

        update_path(current_pos, next_pos, path)

    # Close the socket connection
    sock.close()

if __name__ == '__main__':
    main()