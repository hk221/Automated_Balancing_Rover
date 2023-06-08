import cv2
import math
import numpy as np

# Dimensions of the maze
maze_width = 2.8  # Width of the maze
maze_height = 3.6  # Height of the maze

# Robot-camera coordinates
robot_camera = (0, 0)  # (x, y)

# Beacon coordinates (known initially)
beacon_coordinates = {
    'red': (1.0, 2.0),    # Example coordinates, replace with actual values
    'blue': (3.0, 4.0),
    'yellow': (5.0, 6.0)
}

# Create a graph to hold the nodes and edges
graph = {}

# Camera parameters (focal length and optical center)
focal_length = 500.0    # Example focal length, replace with actual value
optical_center = (320, 240)    # Example optical center, replace with actual value

def measure_angle(beacon_color):
    # Example code to measure the angle to a beacon using a camera
    # Replace this code with your actual camera angle measurement implementation
    # This example code assumes you have access to the camera frame 'frame'
    frame = cv2.imread('camera_frame.jpg')    # Replace with actual camera frame capture
    # Perform image processing and detection to find the beacon
    # Calculate the angle from the optical center to the detected beacon
    angle = 0.0    # Example angle, replace with actual measured angle
    return angle


def localize_robot():
    # Measure angles to the beacons
    angles = {}
    for beacon_color in beacon_coordinates:
        angle = measure_angle(beacon_color)
        angles[beacon_color] = angle

    # Calculate robot position using triangulation
    robot_position = None
    visible_beacons = list(angles.keys())

    # Localize based on any two visible beacons
    if len(visible_beacons) >= 2:
        # Iterate through all possible pairs of visible beacons
        for i in range(len(visible_beacons)):
            for j in range(i + 1, len(visible_beacons)):
                
                # Extract the measured angles
                angle1 = angles[visible_beacons[0]]
                angle2 = angles[visible_beacons[1]]

                # Extract the beacon coordinates
                beacon1 = beacon_coordinates[visible_beacons[0]]
                beacon2 = beacon_coordinates[visible_beacons[1]]

                # Calculate the distances to the beacons
                distance1 = math.sqrt(beacon1[0]**2 + beacon1[1]**2)
                distance2 = math.sqrt(beacon2[0]**2 + beacon2[1]**2)

                # Calculate the robot position
                x = (distance1 * math.tan(angle1) + distance2 * math.tan(angle2)) / (math.tan(angle1) + math.tan(angle2))
                y = (distance1 * math.tan(angle1) + distance2 * math.tan(angle2)) / (math.tan(angle1) + math.tan(angle2))

        robot_position = (x, y)
        return robot_position

# Function to update the graph with the robot's position
def update_graph(robot_position):
    # Find the closest vertex in the graph to the robot's position
    closest_vertex = min(graph.keys(), key=lambda vertex: math.dist(vertex, robot_position))

    # Add an edge between the closest vertex and the robot's position
    graph[closest_vertex].append(robot_position)
    graph[robot_position] = [closest_vertex]


# Main function
def main():
    robot_position = localize_robot()
    if robot_position is not None:
        print("Robot position:", robot_position)
        # Iterate over each cell in the maze
        for i in range(maze_width):
            for j in range(maze_height):
                cell = (i, j)
                # Perform triangulation to estimate the robot's position for the current cell
                robot_position = localize_robot()

                # Update the graph with the estimated robot's position for the current cell
                update_graph(robot_position)
    else:
        print("Localization failed.")

if __name__ == '__main__':
    main()
    
    # Print the graph
    print(graph)