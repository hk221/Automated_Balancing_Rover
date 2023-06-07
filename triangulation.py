import math

def triangulate(reference_points, distances):
    # Ensure three reference points and distances are provided
    if len(reference_points) != 3 or len(distances) != 3:
        raise ValueError("Triangulation requires three reference points and distances.")

    # Extract the coordinates of the reference points
    x1, y1 = reference_points[0]
    x2, y2 = reference_points[1]
    x3, y3 = reference_points[2]

    # Extract the distances
    d1, d2, d3 = distances

    # Calculate the coefficients for the system of equations
    A = 2 * (x2 - x1)
    B = 2 * (y2 - y1)
    C = d1**2 - d2**2 - x1**2 + x2**2 - y1**2 + y2**2
    D = 2 * (x3 - x2)
    E = 2 * (y3 - y2)
    F = d2**2 - d3**2 - x2**2 + x3**2 - y2**2 + y3**2

    # Calculate the intersection point coordinates
    x = (C*E - F*B) / (E*A - B*D)
    y = (C*D - A*F) / (B*D - A*E)

    return x, y


#/////////////////////////////////////////////////////////////////
import gtsam
import numpy as np
from gtsam import Pose3, Rot3, Point3

# Define parameters for 2 cameras, with shared intrinsics.
pose1 = Pose3()
pose2 = Pose3(Rot3(), Point3(5., 0., -5.))
intrinsics = gtsam.Cal3_S2()
camera1 = gtsam.PinholeCameraCal3_S2(pose1, intrinsics)
camera2 = gtsam.PinholeCameraCal3_S2(pose2, intrinsics)
cameras = gtsam.CameraSetCal3_S2([camera1, camera2])

# Define a 3D point, generate measurements by projecting it to the 
# cameras and adding some noise.
landmark = Point3(0.1, 0.1, 1.5)
m1_noisy = cameras[0].project(landmark) + gtsam.Point2(0.00817, 0.00977)
m2_noisy = cameras[1].project(landmark) + gtsam.Point2(-0.00610, 0.01969)
measurements = gtsam.Point2Vector([m1_noisy, m2_noisy])

# Triangulate!
dlt_estimate = gtsam.triangulatePoint3(cameras, measurements, rank_tol=1e-9, optimize=False)
print("DLT estimation error: {:.04f}".format(np.linalg.norm(dlt_estimate - landmark)))

# Optimization needs the measurement noise model.
noisemodel = gtsam.noiseModel.Isotropic.Sigma(2, 1e-3)

optimal_estimate = gtsam.triangulatePoint3(cameras, measurements, rank_tol=1e-9, optimize=True, model=noisemodel)
print("Optimal estimation error: {:.04f}".format(np.linalg.norm(optimal_estimate - landmark)))
