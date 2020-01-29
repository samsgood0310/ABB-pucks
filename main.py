import time
from RAPID import RAPID
from ImageFunctions import *


session = RAPID()
cap = cv2.VideoCapture(1)

totalNumOfPucks = 5  # Total number of pucks in the work area
angles = [0]*totalNumOfPucks
positions = [0]*totalNumOfPucks
safe_height = 90
WRD = 0  # What RAPID Does

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

    if userinput == "1":
        print("Image from above")

        session.set_rapid_variable('WPW', 1)  # Position robot in overview

        session.wait_for_rapid()  # Wait for robot to be in position

        positions, angles = overviewImage()  # Extract position and orientation of all QR codes

    elif userinput == "2":
        print("Move puck to middle")
        pucknr = int(input('\nWhich puck do you want to move?: '))

        session.set_robtarget_variables('puck_position', positions[pucknr - 1])
        session.set_rapid_variable('WPW', 2)  # Position camera above puck

        session.wait_for_rapid()  # Wait for robot to be in position

        offset_mm, angle = closeupImage()  # Get close-up image of the puck and extract QR code's offset from middle
        session.set_offset_variables('offset', offset_mm)  # Tell RAPID where the puck is
        session.set_rapid_variable('angle', angle)  # Give RAPID the orientation of the puck
        session.set_rapid_variable('processed_image', True)  # Tell RAPID that it may proceed

    elif userinput == "3":
        print("Stack pucks")

        for position in positions:
            session.set_robtarget_variables('puck_position', position)
            session.set_rapid_variable('WPW', 2)  # Position camera above puck

            session.wait_for_rapid()  # Wait for robot to be in position

            offset_mm, angle = closeupImage()  # Get close-up image of the puck and extract QR code's offset from middle
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
            session.set_rapid_variable('processed_image', True)  # Tell RAPID that it may proceed

    elif userinput == "5":
        print("Exited program")
        break
    else:
        pass