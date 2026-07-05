import math

def calculate_distance(p1, p2):
    """
    Calculate Euclidean distance between two points (x, y).
    """
    return math.hypot(p2[0] - p1[0], p2[1] - p1[1])

def get_landmark_coords(landmark, img_width, img_height):
    """
    Convert normalized landmark coordinates to pixel coordinates.
    """
    x = int(landmark.x * img_width)
    y = int(landmark.y * img_height)
    return (x, y)
