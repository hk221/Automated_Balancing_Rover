import socket
import time
import asyncio
import websockets
import numpy as np
from collections import deque
import math
import random
from itertools import combinations



global N, counter, image_size, actual_size, focal_length, beacon_boxes, beacon_positions

counter = 0
image_size = (480, 640) 


beacon_boxes = {

}

beacon_positions = {
    'red': (0, 0),
    'blue': (2.4, 0),
    'yellow': (0, 3.6)
}

focal_length = 625

def calculate_rover_position(beacon_boxes, beacon_positions, image_size):
    beacon_angles = {}
    for color in beacon_boxes:
        min_x, _ = beacon_boxes[color][0]
        max_x, _ = beacon_boxes[color][1]
        mid_x = (min_x + max_x) / 2
        angle_to_beacon = math.atan((mid_x - image_size[1] / 2) / focal_length)
        beacon_angles[color] = angle_to_beacon
    # calculate rover position based on the triangulation of the known beacons
    rover_position = triangulate(beacon_positions, beacon_angles)
    return rover_position

def triangulate(positions, angles):
    # choose any two of the beacons to form a pair
    pair = list(combinations(positions.keys(), 2))
    pos1, ang1 = positions[pair[0][0]], angles[pair[0][0]]
    pos2, ang2 = positions[pair[0][1]], angles[pair[0][1]]
    # position of rover using triangulation equations
    x = ((pos1[1] - pos2[1]) - math.tan(ang2) * pos2[0] + math.tan(ang1) * pos1[0]) / (math.tan(ang1) - math.tan(ang2))
    y = pos1[1] + math.tan(ang1) * (x - pos1[0])
    return x, y


async def server(websocket, path):
    global counter

    redcoords = {}
    bluecoords = {}
    yellcoords = {}

    async for message in websocket:
        #print (message)
        if len(message) == 8:
            if message[0] == "3":
                coords = (int(message[1:3], 16), int(message[4:8], 16))
            else:
                coords = (int(message[1:4], 16), int(message[5:8], 16))
        else:
            coords = (0, 0)

        if message[0] == "1":
            #print (coords)
            if len(bluecoords) == 0:
                bluecoords["min"] = coords
            elif len(bluecoords) == 1:
                if bluecoords["min"][0]>coords[0]:
                    bluecoords["max"] = bluecoords["min"]
                    bluecoords["min"] = coords
                else:
                    bluecoords["max"] = coords
                
            else:
                #print ("Blue: "+str(bluecoords))
                beacon_boxes["blue"] = [bluecoords["min"], bluecoords["max"]]
                bluecoords = {}

        elif message[0] == "0" and message != "00000000":

            #print (coords)
            if len(redcoords) == 0:
                redcoords["min"] = coords
            elif len(redcoords) == 1:
                if redcoords["min"][0]>coords[0]:
                    redcoords["max"] = redcoords["min"]
                    redcoords["min"] = coords
                else:
                    redcoords["max"] = coords
                
            else:
                #print ("RED: "+str(redcoords))
                beacon_boxes["red"] = [redcoords["min"], redcoords["max"]]
                redcoords = {}

        elif message[0] == "3": #yellow

            
            if len(yellcoords) == 0:
                yellcoords["min"] = coords
            elif len(yellcoords) == 1:
                if yellcoords["min"][0]>coords[0]:
                    yellcoords["max"] = yellcoords["min"]
                    yellcoords["min"] = coords
                else:
                    yellcoords["max"] = coords
                
            else:
                #print ("Yellow: "+str(yellcoords))
                beacon_boxes["yellow"] = [yellcoords["min"], yellcoords["max"]]
                yellcoords = {}
                
        if len(beacon_boxes) == 3:
            #To-Do calculate position of rover and print it
                position = calculate_rover_position(beacon_boxes, beacon_positions, image_size)
                position = (position[0]*1.5, position[1]*1.5)
                random_decimal = random.random()
                print ("Position: "+str(position))
                
          

        # counter += 1
        
        # if counter % N == 0:  # process every Nth message
        #     if len(coordarray) == 0:
        #         coordarray.append(message)
        #     elif len(coordarray) == 1:
        #         coordarray.append(message)
        #     elif len(coordarray) == 2:
        #         identifier1 = coordarray[0][0]
        #         identifier2 = coordarray[1][0]
        #         if identifier1== identifier2 and coordarray[0]!= '00000000' and coordarray[1] != '00000000':
        #             minmax = [(int(coordarray[0][1:4], 16), int(coordarray[0][5:8], 16)), (int(coordarray[1][1:4], 16), int(coordarray[1][5:8], 16))] #[(xmin, ymin), (xmax,ymax)]
        #             if identifier1 == '0':#red
                        
        #                 print("Red: "+str(minmax))
        #                 redcoords.append(minmax)
        #                 position = calculate_position(image_size, beacon_boxes, beacon_positions, actual_size, focal_length)
                        
        #                 beacon_boxes["red"] = minmax
        #             elif identifier1=='1':#blue
                       
        #                 print("Blue: "+str(minmax))
        #                 bluecoords.append((minmax[1], minmax[0]))
        #                 beacon_boxes["blue"] = minmax
        #                 position = calculate_position(image_size, beacon_boxes, beacon_positions, actual_size, focal_length)
        #             elif identifier1 == '3':#yellow
                       

        #                 print("Yellow: "+str(minmax))
        #                 yellcoords.append(minmax)
        #                 beacon_boxes["yellow"] = minmax
        #                 position = calculate_position(image_size, beacon_boxes, beacon_positions, actual_size, focal_length)
        #             print ("Position: "+str(position))
        #         coordarray = []
        #     counter = 0  # reset the counter


def calculate_angle(center, point):
    x, y = point[0] - center[0], point[1] - center[1]
    return math.atan2(y, x)

def estimate_distance(box_corners, actual_size, focal_length):
    # Estimate distance based on size of box in image (use appropriate formula based on your camera setup)
    # Assuming corners are in order: top left, top right, bottom right, bottom left
    box_width = math.sqrt((box_corners[1][0] - box_corners[0][0])**2 + (box_corners[1][1] - box_corners[0][1])**2)#
    if box_width <= 0:
        box_width = 1
    distance = (actual_size * focal_length) / box_width
    return distance

def calculate_position(image_size, beacon_boxes, beacon_positions, actual_size, focal_length):
    beacon_distances = {}
    beacon_angles = {}

    # Get the center of the image
    center = (image_size[1] // 2, image_size[0] // 2)

    for color, box_corners in beacon_boxes.items():
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
        if x > distance1:  # prevent sqrt of negative number
            y = 0
        else:
            y = np.sqrt(distance1**2 - x**2)

        position_estimates.append((x, y))

    # Choose the position estimate that minimizes the total distance to the beacons
    best_position = min(position_estimates, key=lambda pos: sum(np.sqrt((pos[0] - beacon_positions[color][0])**2 + 
                                                                       (pos[1] - beacon_positions[color][1])**2) 
                                                               for color in beacon_boxes.keys()))

    return best_position



start_server = websockets.serve(server, '192.168.31.210', 3000)









































































































































































asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
