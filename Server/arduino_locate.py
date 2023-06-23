import numpy as np
import math
from itertools import combinations

def calculate_angle(center, point):
    x, y = point[0] - center[0], point[1] - center[1]
    return math.atan2(y, x)

def estimate_distance(box_corners, actual_size, focal_length):
    # Estimate distance based on size of box in image (use appropriate formula based on your camera setup)
    # Assuming corners are in order: top left, top right, bottom right, bottom left
    box_width = math.sqrt((box_corners[1][0] - box_corners[0][0])**2 + (box_corners[1][1] - box_corners[0][1])**2)
    distance = (actual_size * focal_length) / box_width
    return distance

def calculate_position(image_size, beacon_boxes, beacon_positions, actual_size, focal_length):
    beacon_distances = {}
    beacon_angles = {}

    # Get the center of the image
    center = (image_size[1] // 2, image_size[0] // 2)

    for color, box_corners in beacon_boxes.items():
        # get the position of the beacon in the image (center of the box)
# get the position of the beacon in the image (center of the box)
        beacon_pos = ((box_corners[0][0] + box_corners[1][0]) // 2, 
                    (box_corners[0][1] + box_corners[1][1]) // 2)


        # calculate the distance to the beacon
        beacon_distances[color] = estimate_distance(box_corners, actual_size, focal_length)

        # calculate the angle to the beacon
        beacon_angles[color] = calculate_angle(center, beacon_pos)

    # Calculate position estimates for all pairs of beacons
    position_estimates = []
    for red, blue in combinations(beacon_boxes.keys(), 2):
        # get the angle between the beacons
        angle_between_beacons = abs(beacon_angles[red] - beacon_angles[blue])

        # calculate distances to the beacons
        distance1 = beacon_distances[red]
        distance2 = beacon_distances[blue]
        # Assume red is at (0, 0), blue is at (d, 0)
        d = np.sqrt((beacon_positions[blue][0] - beacon_positions[red][0])**2 + (beacon_positions[blue][1] - beacon_positions[red][1])**2)

        assert d!=0, "d = 0"

        # position of the rover (x, y)
        x = (distance1**2 - distance2**2 + d**2) / (2 * d)
        y = np.sqrt(distance1**2 - x**2)

        position_estimates.append((x, y))

    # Choose the position estimate that minimizes the total distance to the beacons
    best_position = min(position_estimates, key=lambda pos: sum(np.sqrt((pos[0] - beacon_positions[color][0])**2 + 
                                                                       (pos[1] - beacon_positions[color][1])**2) 
                                                               for color in beacon_boxes.keys()))

    return best_position



#TestCode

image_size = (480, 640)  

beacon_boxes = {
    'red': [(10, 10), (20, 10)],
    'blue': [(100, 100)],
    'green': [(200, 200)]
}

beacon_positions = {
    'red': (0, 0),
    'blue': (2.4, 0),
    'green': (0, 3.6)
}

actual_size = 0.2  # example actual size
focal_length = 500  # example focal length

position = calculate_position(image_size, beacon_boxes, beacon_positions, actual_size, focal_length)
print(f"Estimated position: {position}")

