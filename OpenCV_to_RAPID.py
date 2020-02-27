import math
import config


def pixel_to_mm(gripper_height):
    """Converts coordinates in image from pixels to millimeters. This depends on the height the image is taken from"""
    mm_width = 0.95 * (gripper_height+70)  # 0.95 = Conversion number between camera height and FOV
    pixel_to_mm = mm_width / 1280  # mm_width / px_width

    # Convert all positions from pixels to millimeters:
    for puck in config.puckdict:
        config.puckdict[puck]["position"] = [x * pixel_to_mm for x in config.puckdict[puck]["position"]]
        #adjustment_x = config.puckdict


def transform_positions(rot):
    """Transform coordinate system given by image in OpenCV to coordinate system of work object in RAPID.
    Swap x & y coordinates and rotate by the same amount that the camera has been rotated."""

    # Perform transformations to match RAPID: x -> y, y -> x, x -> -x, y -> -y
    for key in config.puckdict:
        config.puckdict[key]["position"] = \
        [-config.puckdict[key]["position"][1], -config.puckdict[key]["position"][0]]

    # Convert from quaternion to Euler angle (we only need z-axis):
    rotation_z_radians = quaternion_to_euler(rot)
    rotation_z_degrees = -math.degrees(rotation_z_radians)
    # TODO: Check if rotation is positive or negative for a given orientation

    # TODO: Rotate all points in dict, not list:
    """Rotate all points found by the QR scanner.
    Also, adjust the angle of all pucks by using the orientation of the gripper:"""
    for key in config.puckdict:

        config.puckdict[key]["position"] = \
            [config.puckdict[key]["position"][0] * math.cos(rotation_z_radians) +
             config.puckdict[key]["position"][1] * math.sin(rotation_z_radians),
             -config.puckdict[key]["position"][0] * math.sin(rotation_z_radians) +
             config.puckdict[key]["position"][1] * math.cos(rotation_z_radians)]

        config.puckdict[key]["angle"] -= rotation_z_degrees

        # Only want the gripper to rotate between -180 and +180 degrees
        if config.puckdict[key]["angle"] > 180:
            config.puckdict[key]["angle"] -= 360
        elif config.puckdict[key]["angle"] < -180:
            config.puckdict[key]["angle"] += 360


def get_camera_position(trans, rot):
    """Find the offset between gripper and camera"""

    r = 50  # Distance between gripper and camera
    rotation_z_radians = quaternion_to_euler(rot)
    # TODO: Check if angle should be - or +
    offset_x = r * math.cos(rotation_z_radians)
    offset_y = r * math.sin(rotation_z_radians)

    camera_position = [trans[0] + offset_x, trans[1] + offset_y]  # Gripper position + offset from gripper
    return camera_position


def create_robtargets(gripper_height, rot, cam_pos):
    """Combine all known offsets to make a robtarget on the work object"""
    pixel_to_mm(gripper_height=gripper_height)  # Converts coordinates in image from pixels to millimeters

    camera_compensation(gripper_height=gripper_height)

    transform_positions(rot=rot)

    """config.puckdict["Puck#1"]["position"] = [config.puckdict["Puck#1"]["position"][0] + cam_pos[0],
                                             config.puckdict["Puck#1"]["position"][1] + cam_pos[1], 0]
    config.puckdict["Puck#3"]["position"] = [config.puckdict["Puck#3"]["position"][0] + cam_pos[0],
                                             config.puckdict["Puck#3"]["position"][1] + cam_pos[1], 0]"""

    # TODO: Add compensation *here*

    for key in config.puckdict:
        config.puckdict[key]["position"][0] += cam_pos[0]
        config.puckdict[key]["position"][1] += cam_pos[1]
        config.puckdict[key]["position"].append(0)  # Add z-coordinate for robtarget


def quaternion_to_euler(quaternion):
    """Convert a Quaternion to Euler angle. We only need the rotation around the z-axis"""
    w, x, y, z = quaternion
    t1 = +2.0 * (w * z + x * y)
    t2 = +1.0 - 2.0 * (y * y + z * z)
    rotation_z = math.atan2(t1, t2)

    return rotation_z


def camera_compensation(gripper_height):
    camera_height = gripper_height + 70

    slope_x = -0.03325233759842519
    slope_y = 0.019120094119094485
    comp_x = slope_x * camera_height
    comp_y = slope_y * camera_height
    for key in config.puckdict:
        config.puckdict[key]["position"][0] -= comp_x
        config.puckdict[key]["position"][1] -= comp_y