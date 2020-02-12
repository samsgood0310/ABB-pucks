    if userinput == "1":
        config.puckdict.clear()  # Reset puckdict
        session.set_rapid_variable("WPW", 1)  # Robot goes to position for image acquisition

        session.wait_for_rapid()

        trans, rot = session.get_gripper_position()
        gripper_height = session.get_gripper_height()

        cam_pos = OpenCV_to_RAPID.get_camera_position(trans=trans, rot=rot)
        time.sleep(1)
        overviewImage()

        OpenCV_to_RAPID.create_robtargets(gripper_height=gripper_height, rot=rot, cam_pos=cam_pos)

        # session.set_rapid_variable("image_processed", "TRUE")
        # session.wait_for_rapid()

        # Send all robtargets and angles from dictionary to RAPID:
        # TODO: Find out which method works best; send all pucks at once or send them only when needed by RAPID
        pucknr = 1
        for key in sorted(config.puckdict):
            session.set_robtarget_variables("puck_target{}".format(pucknr), config.puckdict[key]["position"])
            session.set_rapid_variable("puck_angle{}".format(pucknr), config.puckdict[key]["angle"])
            pucknr += 1

    elif userinput == "2":
        print("Move puck to middle")
        pucknr = int(input('\nWhich puck do you want to move?: '))

        session.set_rapid_variable('which_puck', 2)

        # session.set_robtarget_variables('puck_position', positions[pucknr - 1])
        session.set_rapid_variable('WPW', 2)  # Position camera above puck

        session.wait_for_rapid()  # Wait for robot to be in position

        gripper_height = session.get_gripper_height()

        # Get close-up image of the puck and extract QR code's offset from middle
        offset_mm_x, offset_mm_y = closeupImage(gripper_height)
        session.set_rapid_variable('offset_x', offset_mm_x)  # Tell RAPID where the puck is
        session.set_rapid_variable('offset_y', offset_mm_y)  # Give RAPID the orientation of the puck
        session.set_rapid_variable('image_processed', "TRUE")  # Tell RAPID that it may proceed

        
        
""" OpenCV_to_RAPID: """
def pixel_to_mm(gripper_height):
    """Converts coordinates in image from pixels to millimeters. This depends on the height the image is taken from"""
    mm_width = 0.95 * (gripper_height+70)  # 0.95 = Conversion number between camera height and FOV
    pixel_to_mm = mm_width / config.px_width  # mm_width / px_width

    # Convert all positions from pixels to millimeters:
    for puck in config.puckdict:
        config.puckdict[puck]["position"] = [x * pixel_to_mm for x in config.puckdict[puck]["position"]]


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
    print("robot orientation", rotation_z_degrees)
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

    transform_positions(rot=rot)

    """config.puckdict["Puck#1"]["position"] = [config.puckdict["Puck#1"]["position"][0] + cam_pos[0],
                                             config.puckdict["Puck#1"]["position"][1] + cam_pos[1], 0]
    config.puckdict["Puck#3"]["position"] = [config.puckdict["Puck#3"]["position"][0] + cam_pos[0],
                                             config.puckdict["Puck#3"]["position"][1] + cam_pos[1], 0]"""
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
