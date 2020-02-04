import time
from RAPID import *
from ImageFunctions import *
from OpenCV_to_RAPID import *


session = RAPID()
cap = cv2.VideoCapture(1)
# TODO: Check which solution is best here (get width and height from the start?):
ret, frame = cap.read()
frame_width, frame_height, channels = frame.shape

totalNumOfPucks = 5  # Total number of pucks in the work area
angles = [0]*totalNumOfPucks
positions = [0]*totalNumOfPucks
safe_height = 90
WRD = 0  # What RAPID Does

session.request_rmmp()
session.set_rapid_variable("ready_flag", "FALSE")

while True:

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

    if userinput == "6":
        print("Image from above")

        session.set_rapid_variable('WPW', 1)  # Position robot in overview

        session.wait_for_rapid()  # Wait for robot to be in position

        positions, angles = overviewImage()  # Extract position and orientation of all QR codes

    elif userinput == "2":
        print("Move puck to middle")
        pucknr = int(input('\nWhich puck do you want to move?: '))

        #session.set_robtarget_variables('puck_position', positions[pucknr - 1])
        session.set_rapid_variable('WPW', 2)  # Position camera above puck

        session.wait_for_rapid()  # Wait for robot to be in position

        """offset_mm, angle = closeupImage()  # Get close-up image of the puck and extract QR code's offset from middle
        session.set_offset_variables('offset', offset_mm)  # Tell RAPID where the puck is
        session.set_rapid_variable('angle', angle)  # Give RAPID the orientation of the puck
        session.set_rapid_variable('processed_image', True)  # Tell RAPID that it may proceed"""

    elif userinput == "3":
        print("Stack pucks")

        for position in positions:
            session.set_robtarget_variables('puck_position', position)
            session.set_rapid_variable('WPW', 2)  # Position camera above puck

            session.wait_for_rapid()  # Wait for robot to be in position

            # Get close-up image of the puck and extract QR code's offset from middle:
            offset_mm, angle = closeupImage()
            session.set_offset_variables('offset', offset_mm)  # Tell RAPID where the puck is
            session.set_rapid_variable('angle', angle)  # Give RAPID the orientation of the puck
            session.set_rapid_variable('processed_image', True)  # Tell RAPID that it may proceed

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
        #[266.9375, 147.5, 90]
        #[265.625, 211.75, 90]
        break

    # TODO: Make a CASE for close up image as well. Remember to convert form px to mm
    elif userinput == "1":
        session.set_rapid_variable("WPW", 1)
        #print(session.get_rapid_variable("ready_flag").type)

        session.wait_for_rapid()

        # while not done capturing images:
        trans, rot = session.get_current_position()
        print(trans)
        gripper_height = session.get_gripper_height()

        overviewImage()

        pixel_to_mm(frame_height, gripper_height)

        transform_positions(trans, rot)

        session.set_rapid_variable("processed_image", True)
        #session.wait_for_rapid()

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
            session.set_robtarget_variables("puck_target{0}".format(i+1), robtargets[i])
            session.set_rapid_variable("puck_angle{0}".format(i+1), angles[i])
            print(robtargets[i])
            print(angles[i])

    else:
        pass

