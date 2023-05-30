for i in range(10):
    # Explore 10 times before stopping (will defo need to be more than 10)
    for j in range(10):
        # Attempt to move one meter forward
        while not successfullyMovedForward():
            # If unable to move forward, turn to try a new direction
            turn()
        
        if j % 5 == 0:
            # Once every 5 moves, spin around to gather more accurate readings
            spinAround()
    
    # End of exploration loop
    # Perform additional actions or terminate the program
#########make corresponding functions for each action############
def successfullyMovedForward():
    # Returns true if the robot successfully moved forward
    # Returns false if the robot was unable to move forward
    # (e.g., if there was a wall in the way)
    # This function should also update the robot's internal map
    # based on the sensor readings
    pass
def turn():
    # Turns the robot 90 degrees to the right
    pass
def spinAround():
    # Spins the robot around 180 or 360 degrees?
    pass
# Function to read LDR values from analog pins
def getSensorReadings():
    # Returns a list of 4 numbers which would be 4 LDR readings, 
    # representing the distance to the nearest object in 
    # each direction (front, left, back, right)
    # The list should be in the same order as the directions
    left_ldr_value = analogRead(left_ldr_pin)
    right_ldr_value = analogRead(right_ldr_pin)
    return [left_ldr_value, right_ldr_value]
    pass
#from sensor readings store ldr values in variables like below
#left_ldr_pin = 0  # Pin number for the left LDR input
#right_ldr_pin = 1  # Pin number for the right LDR input
# Function to check if there is an obstacle based on LDR readings
def obstacle_detected():
    ldr_values = getSensorReadings()
    obstacle_threshold = 500  # Threshold value to determine obstacle presence
    
    if ldr_values[0] > obstacle_threshold or ldr_values[1] > obstacle_threshold:
        return True
    else:
        return False
def getMap():
    # Returns the robot's internal map
    pass
def getRobotPosition():
    # Returns the robot's current position
    pass
def getRobotDirection():
    # Returns the robot's current direction
    pass
def moveForward():
    # Moves the robot forward by one square
    pass
# Main loop
#while True:
#    if obstacle_detected():
#        # If obstacle detected, turn or take appropriate action
#        turn()  
#    else:
#        # turn to face the direction of the next waypoint
#        moveForward() 