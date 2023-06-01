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


