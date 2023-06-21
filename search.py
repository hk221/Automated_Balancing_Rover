import serial
import numpy as np
import time
from heapq import heappop, heappush

# Serial communication setup
arduino_port = 'COM3'  # Change to the appropriate port
arduino_baudrate = 115200
ser = serial.Serial(arduino_port, arduino_baudrate, timeout=1)

# Maze dimensions
maze_width = 280
maze_height = 360

# start and goal position
start_position = (0, 0)
goal_position = (maze_height-1, maze_width-1)

# Initialize the walls array
walls = np.zeros((maze_height, maze_width), dtype=bool)

# Motor control functions
# Define your motor control functions here based on the Arduino code

# Dijkstra's algorithm for path finding
def dijkstra(maze, start, goal):
    # Implementation of Dijkstra's algorithm here
    # Calculate the shortest path from start to end
    # Return a list of nodes representing the shortest path
    rows, cols = maze.shape #gives rows and column size of matrix
    distances = np.full((rows, cols), np.inf)
    distances[start] = 0
    previous = np.empty((rows, cols), dtype=object)
    queue = [(0, start)]
    
    while queue:
        current_dist, current_pos = heappop(queue)

        if current_pos == goal:
            return distances, previous

        if current_dist > distances[current_pos]:
            continue

        for neighbor in get_neighbors(current_pos):
            new_dist = current_dist + 1  # Assume unit cost for each step

            if new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                previous[neighbor] = current_pos
                heappush(queue, (new_dist, neighbor))

    return distances, previous


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

def get_next_coordinates(next_pos):
    # Implement your function to get the coordinates for the next position
    # based on the next_pos value
    # Replace this with your actual implementation
    return 0, 0

def update_path(current_pos, next_pos, path):
    # Update the path with the current position and the next position
    path.append(current_pos)
    path.append(next_pos)


# Main program
def main():
    # Initialize the walls array
    walls = np.zeros((maze_height, maze_width), dtype=bool)

    # Run Dijkstra's algorithm
    distances, previous = dijkstra(walls, start_position, goal_position)

    # Determine the shortest path
    path = []
    current_pos = goal_position
    while current_pos != start_position:
        path.append(current_pos)
        current_pos = previous[current_pos]
    path.append(start_position)
    path.reverse()

    # Execute the movements based on the shortest path
    for i in range(len(path)-1):
        current_pos = path[i]
        next_pos = path[i+1]
        
        # Get the current and next coordinates
        current_coordinates = get_current_coordinates()
        next_coordinates = get_next_coordinates(next_pos)

        # Determine the movement direction based on sensor readings from Arduino
        ser.write(b'get_led_walls\n')  # Request sensor readings from Arduino
        response = ser.readline().decode().strip()  # Read response from Arduino
        # Use the sensor readings to update the walls array dynamically

        # Process the sensor readings to update the walls array
        bits = int(response, 2)
        row, col = current_pos
        if bits & 0b0001:
            walls[row-1, col] = True  # Wall detected in front
        if bits & 0b0010:
            walls[row+1, col] = True  # Wall detected at the back
        if bits & 0b0100:
            walls[row, col+1] = True  # Wall detected on the right
        if bits & 0b1000:
            walls[row, col-1] = True  # Wall detected on the left

        # Execute the movement commands based on the determined direction
        if current_pos[0] < next_pos[0]:
            move_forward()
        elif current_pos[0] > next_pos[0]:
            move_back()
        elif current_pos[1] < next_pos[1]:
            turn_right()
        elif current_pos[1] > next_pos[1]:
            turn_left()
        

        update_path(current_pos, next_pos)

        # Add a delay to allow the robot to complete the movement
        time.sleep(1)

    # Close the serial connection
    ser.close()

if __name__ == '__main__':
    main()