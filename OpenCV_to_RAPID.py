import math
import config


def pixel_to_mm(px_height, gripper_height):
    # TODO: Find real FOV of camera and how to find the size of the picture as a product of FOV and camera height
    positions_mm = []
    FOV = 60
    mm_height = FOV * gripper_height
    pixel_to_mm = 469 / 1920  # mm_height / px_height

    #  Convert all positions from pixels to millimeters:
    for puck in config.puckdict:
        config.puckdict[puck]["position"] = tuple(pixel_to_mm * x for x in config.puckdict[puck]["position"])


def transform_positions(trans, rot):
    """Transform coordinate system given by image in OpenCV to coordinate system of work object in RAPID.
    Swap x & y coordinates and rotate by the same amount that the camera has been rotated."""

    # Swap x & y coordinates:
    for key in config.puckdict:
        config.puckdict[key]["position"] = \
        (config.puckdict[key]["position"][1], config.puckdict[key]["position"][0])
    """for key, value in config.puckdict.items():
        config.puckdict[value]["position"] = \
            (config.puckdict[value]["position"][1], config.puckdict[value]["position"][0])"""

    # Convert from quaternion to Euler angle (we only need z-axis):
    w, x, y, z = rot
    print(rot)
    t1 = +2.0 * (w * z + x * y)
    t2 = +1.0 - 2.0 * (y * y + z * z)
    rotation_z = math.degrees(math.atan2(t1, t2))
    print(rotation_z , "hei")
    # TODO: Check if rotation is positive or negative for a given orientation

    # TODO: Rotate all points in dict, not list:
    """Rotate all points found by the QR scanner. Add the camera's position on the work object 
    so the resulting position value is the true position of the QR codes on the work object. 
    Finally, adjust the angle of all pucks by using the orientation of the camera:"""
    for key in config.puckdict:
        config.puckdict[key]["position"] = \
            (config.puckdict[key]["position"][0] * math.cos(math.radians(rotation_z)) +
             config.puckdict[key]["position"][1] * math.sin(math.radians(rotation_z)) + trans[0],
             -config.puckdict[key]["position"][0] * math.sin(math.radians(rotation_z)) +
             config.puckdict[key]["position"][1] * math.cos(math.radians(rotation_z)) + trans[1]
             )
        config.puckdict[key]["angle"] += rotation_z
        print(config.puckdict[key]["angle"])