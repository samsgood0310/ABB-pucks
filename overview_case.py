import time
from RAPID import *
from ImageFunctions import *
from OpenCV_to_RAPID import *
from threading import Thread

x = Thread(target=showVideo, args=(1,), daemon=True)
x.start()

session = RAPID()
# TODO: Check which solution is best here (get width and height from the start?):
ret, frame = config.cap.read()
frame_width, frame_height, channels = frame.shape
print(frame_width, frame_height)

WRD = 0  # What RAPID Does

session.request_rmmp()
session.set_rapid_variable("ready_flag", "FALSE")

while False:

    while WRD != 0:
        WRD = int(session.get_rapid_variable('WRD'))
        time.sleep(0.5)

    print("""
    1. Image from above
    2. Move puck to middle
    3. Stack pucks
    4. Rotate puck
    5. Exit""")

    """Every time a puck is to be picked up, a close-up image will be taken. 
    The gripper will move backwards, go down, and slide in towards the puck and grip it.
    Moving the robot, picking up and placing pucks are handled by RAPID in the manner that Python wants it done."""

    userinput = input('\nWhat should RAPID do?: ')

    if userinput == "1":
        config.puckdict.clear()  # Reset puckdict
        session.set_rapid_variable("WPW", 1)  # Robot goes to position for image acquisition

        session.wait_for_rapid()

        trans, rot = session.get_gripper_position()
        gripper_height = session.get_gripper_height()

        cam_pos = OpenCV_to_RAPID.get_camera_position(trans=trans, rot=rot)

        overviewImage()
        for key in config.puckdict:
            print(config.puckdict[key]["position"])

        OpenCV_to_RAPID.create_robtargets(gripper_height=gripper_height, rot=rot, cam_pos=cam_pos)

        # session.set_rapid_variable("image_processed", "TRUE")
        # session.wait_for_rapid()

        # Send all robtargets and angles from dictionary to RAPID:
        for key in sorted(config.puckdict):
            pucknr = 1
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
        print(gripper_height)

        # Get close-up image of the puck and extract QR code's offset from middle
        offset_mm_x, offset_mm_y = closeupImage(gripper_height)
        session.set_rapid_variable('offset_x', offset_mm_x)  # Tell RAPID where the puck is
        session.set_rapid_variable('offset_y', offset_mm_y)  # Give RAPID the orientation of the puck
        session.set_rapid_variable('image_processed', "TRUE")  # Tell RAPID that it may proceed

    elif userinput == "3":
        print("Stack pucks")

        session.set_rapid_variable('WPW', 3)

        # Run program until all pucks are stacked
        while session.get_rapid_variable('WRD') is 3:
            session.wait_for_rapid()

            gripper_height = session.get_gripper_height()

            # Get close-up image of the puck and extract QR code's offset from middle
            offset_mm_x, offset_mm_y = closeupImage(gripper_height)
            session.set_rapid_variable('offset_x', offset_mm_x)  # Tell RAPID where the puck is
            session.set_rapid_variable('offset_y', offset_mm_y)  # Give RAPID the orientation of the puck
            session.set_rapid_variable('image_processed', "TRUE")  # Tell RAPID that it may proceed

    elif userinput == "4":
        print("Reorient pucks")

        for position in positions:
            session.set_robtarget_variables('puck_position', position)
            session.set_rapid_variable('WPW', 4)  # Position camera above puck

            session.wait_for_rapid()  # Wait for robot to be in position

            offset_mm, angle = closeupImage()  # Get close-up image of the puck and extract QR code's offset from middle
            session.set_offset_variables('offset', offset_mm)  # Tell RAPID where the puck is
            session.set_rapid_variable('angle', angle)  # Give RAPID the orientation of the puck
            session.set_rapid_variable('processed_image', "TRUE")  # Tell RAPID that it may proceed

    elif userinput == "5":
        print("Exited program")
        break

    else:
        pass

import random

input()
while True:
    config.puckdict.clear()
    session.set_rapid_variable("WPW", 1)
    trans = [random.randint(-50, 150), random.randint(-150, 150), 0]
    session.set_robtarget_variables("randomTarget", trans)
    # print(session.get_rapid_variable("ready_flag").type)

    print("before wait1")
    session.wait_for_rapid()
    print("after wait1")
    trans, rot = session.get_current_position()
    gripper_height = session.get_gripper_height()
    print("gripper height ", gripper_height)

    overviewImage()
    for key in config.puckdict:
        print("image position ", config.puckdict[key]["position"])

    transform_positions(trans, rot)

    pixel_to_mm(gripper_height)

    # session.set_rapid_variable("image_processed", "TRUE")
    # session.wait_for_rapid()

    # end while
    # TODO: Check if safe_height is to be used:
    # Convert the values of the dictionary into a list of robtargets and angles to be sent to RAPID
    robtargets = []
    angles = []
    for key in sorted(config.puckdict):
        robtarget = list(config.puckdict[key]["position"] + (0,))  # Add z-coordinate to the targets
        robtargets.append(robtarget)
        angle = config.puckdict[key]["angle"]
        angles.append(angle)

    # Send robtargets and angles one by one to RAPID:
    for i in range(len(robtargets)):
        session.set_robtarget_variables("puck_target{0}".format(i + 1), robtargets[i])
        session.set_rapid_variable("puck_angle{0}".format(i + 1), -angles[i])  # TODO: CHECK MINUS
        print("robtarget to RAPID ", robtargets[i])
        print("angle ", angles[i])

    session.set_rapid_variable('WPW', 2)  # Position camera above puck

    print("before wait2")
    session.wait_for_rapid()  # Wait for robot to be in position
    print("after wait2")
    gripper_height = session.get_gripper_height()
    offset_mm_x, offset_mm_y = closeupImage(
        gripper_height)  # Get close-up image of the puck and extract QR code's offset from middle
    session.set_rapid_variable('offset_x', offset_mm_x)  # Tell RAPID where the puck is
    session.set_rapid_variable('offset_y', offset_mm_y)  # Give RAPID the orientation of the puck
    session.set_rapid_variable('image_processed', "TRUE")  # Tell RAPID that it may proceed
    print("before wait3")
    session.wait_for_rapid()
    print("after wait3")
while False:
    session.set_robtarget_variables("rob1", [0, 0, 100])
    session.set_rapid_variable('image_processed', "TRUE")
    session.wait_for_rapid()
    session.set_robtarget_variables("rob1", [0, 0, 200])
    session.set_rapid_variable('image_processed', "TRUE")
    session.wait_for_rapid()
