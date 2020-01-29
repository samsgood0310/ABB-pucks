import cv2
from QR_Reader import QR_Scanner

# TODO: Extend the program with threading, this will allow the camera to always stay active
#  and could give a live feed of what the camera sees while still maintaining control over robot.

def overviewImage():
    """Get the location and orientation of all pucks in the scene
    by grabbing several images with different threshold values."""

    cap = cv2.VideoCapture(0)  # Start camera

    numberOfPucks = 5  # Specify total number of pucks in the work area
    thresh_incr = 0  # Initalize counter for incrementing threshold
    positions = [0] * numberOfPucks  # Initialize position list
    angles = [0] * numberOfPucks  # Initalize orientation list

    while cap.isOpened():
        ret, frame = cap.read()  # Read image to np.array
        # Take x amount of images, depending on thresh_inc and the if statement:
        if ret and thresh_incr < 200 and 0 in positions:
            # Extracts position, orientation, which pucks were detected, and image with marked QR codes:
            pos, ang, pucksDetected, img = QR_Scanner(frame, thresh_incr)

            # Updates the lists with position and orientation of the detected pucks:
            for pucknr in pucksDetected:
                positions[pucknr - 1] = pos[pucknr - 1]
                angles[pucknr - 1] = ang[pucknr - 1]

            thresh_incr += 1  # Increment threshold value

        else:
            cap.release()
            break

    return positions, angles


def closeupImage():
    """Grab several images at low height over the approximate position of a puck.
    If several pucks are seen, keep only the one closest to the center."""
    # TODO: Bryte while-loop når puck er funnet
    thresh_incr = 0
    cap = cv2.VideoCapture(0)  # Start camera

    while cap.isOpened():
        ret, frame = cap.read()  # Read image to np.array
        # Take x amount of images, depending on thresh_inc and the if statement:
        if ret and thresh_incr < 50:
            pos, ang = QR_Scanner(frame, thresh_incr)  # Get position and orientation of QR code
            # TODO: Check if several pucks are detected and only include the puck closest to the center of the frame
            # Set position equal to pos if QR code is detected:
            if pos:
                position = pos
                angle = ang
            thresh_incr += 5

    height, width, channels = frame.shape  # Find image resolution
    print(height, width)
    # Use resolution to make middle of image (x,y) = (0,0).
    # Now one can use offset in RAPID from current position:
    offset_pixel = [position[0]-width/2, position[1]-height/2]
    # TODO: Find height and width of image in mm
    pixel_to_mm = "idk"  # TODO
    offset_mm = offset_pixel * pixel_to_mm
    return offset_mm, angle
