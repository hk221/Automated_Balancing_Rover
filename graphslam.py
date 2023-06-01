import numpy as np
import gtsam
import math
#calculate average distnace 
#open camera and ldr files then average distance (camera_coordinates,ldr_coordinates)
def calculate_distance(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return distance

def average_distance(point1, point2):
    total_distance = 0
    for i in range(len(point1)):
        distance = calculate_distance(point1[i], point2[i])
        total_distance += distance
    average = total_distance / len(point1)
    return average

# Step 1: Define Data Structures

# Define a graph to hold the nodes and edges
graph = gtsam.NonlinearFactorGraph()
# Create a values container to hold the initial estimates of poses and landmarks
initial_estimates = gtsam.Values()
#define landmark_pose_index
# Step 2: Graph Construction
def create_graph(poses, landmarks):
    # Add factors for pose constraints (e.g., odometry or motion model)
    # Assume you have a list of pose measurements `poses` in the form of (x, y, theta)
    for i, pose_measurement in enumerate(poses):
        pose = gtsam.Pose2(pose_measurement[0], pose_measurement[1], pose_measurement[2])
        noise_model = gtsam.noiseModel.Diagonal.Sigmas([0.1, 0.1, 0.1])  # Noise model for the pose measurement
        factor = gtsam.BetweenFactor(gtsam.symbol(ord('x'), i), gtsam.symbol(ord('x'), i+1), pose, noise_model)
        graph.add(factor)

        # Add initial estimate for each pose
        initial_estimates.insert(gtsam.symbol(ord('x'), i), pose)

    # Add factors for landmark constraints (e.g., LED strip measurements)
    # Assume you have a list of landmark measurements `landmarks` in the form of (x, y)
    for i, landmark_measurement in enumerate(landmarks):
        landmark = gtsam.Point2(landmark_measurement[0], landmark_measurement[1])
        noise_model = gtsam.noiseModel.Diagonal.Sigmas([0.1, 0.1])  # Noise model for the landmark measurement
        factor = gtsam.BearingRangeFactor2D(gtsam.symbol(ord('x'), landmark_pose_index), gtsam.symbol(ord('l'), i), landmark, noise_model)
        graph.add(factor)

        # Add initial estimate for each landmark
        initial_estimates.insert(gtsam.symbol(ord('l'), i), landmark)

    # Perform optimization using the graph and initial estimates


# Step 3: Formulate the Optimization Problem ############################

# Define noise models for the sensor measurements

# Define error functions (factors) based on the constraints and sensor measurements
# Add these factors to the graph

# Step 4: Solve the Optimization Problem

# Create an optimizer
# Perform optimization using the graph and initial estimates
optimizer = gtsam.LevenbergMarquardtOptimizer(graph, initial_estimates)
result = optimizer.optimize()

# Step 5: Update Pose and Landmark Estimates

# Retrieve the optimized pose and landmark estimates from the result
# Retrieve optimized poses and landmarks
optimized_poses = [result.atPose2(gtsam.symbol(ord('x'), i)) for i in range(len(poses))]
optimized_landmarks = [result.atPoint2(gtsam.symbol(ord('l'), i)) for i in range(len(landmarks))]

# Optimize the graph
result = optimizer.optimize()

# Step 6: Repeat for New Sensor Data

# As new sensor data becomes available, update the graph and perform optimization iteratively

# Step 7: Test and Validate

# Evaluate the accuracy of the estimated poses and landmarks

# Step 8: Optimize and Refine

# Optimize and refine the code for efficiency and accuracy


# Main Function
def main():
    # Call the necessary functions and methods to perform GraphSLAM

if __name__ == '__main__':
    main()
