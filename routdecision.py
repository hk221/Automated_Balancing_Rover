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
def getSensorReadings():
    # Returns a list of 4 numbers which would be 4 LDR readings, 
    # representing the distance to the nearest object in 
    # each direction (front, left, back, right)
    # The list should be in the same order as the directions
    pass
def getMap():
    # Returns the robot's internal map
    pass
def getRobotPosition():
    # Returns the robot's current position
    pass
def getRobotDirection():
    # Returns the robot's current direction
    pass


