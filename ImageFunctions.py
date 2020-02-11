import cv2
from QR_Reader import QR_Scanner, QR_Scanner_visualized
import config

# TODO: Extend the program with threading, this will allow the camera to always stay active
#  and could give a live feed of what the camera sees while still maintaining control over robot.

def overviewImage():
    """Get the location and orientation of all pucks in the scene
    by grabbing several images with different threshold values."""

    while config.cap.isOpened():
        ret, frame = config.cap.read()  # Read image to np.array
        if ret:
            # Extracts position, orientation, which pucks were detected, and image with marked QR codes:
            img = QR_Scanner(img=frame)
            break

def closeupImage(gripper_height):
    """Grab several images at low height over the approximate position of a puck.
    If several pucks are seen, keep only the one closest to the center."""

    # TODO: Bryte while-loop når puck er funnet
    offset_pixel_tuple = 0

    while config.cap.isOpened():
        ret, frame = config.cap.read()  # Read image to np.array
        # Take x amount of images, depending on thresh_inc and the if statement:
        #if ret and thresh_incr < 200:

        # Get position and orientation of QR code:
        offset_pixel_tuple, img = QR_Scanner(img=frame, closeup=True)
        print("offset_pixel ", offset_pixel_tuple)
        # TODO: Check if several pucks are detected and only include the puck closest to the center of the frame
        #thresh_incr += 5
        # TODO: Increment in a better way?
        break

    # Use resolution to make middle of image (x,y) = (0,0).
    # Now one can use offset in RAPID from current position:
    # TODO: Find height and width of image in mm
    mm_width = 0.95 * (gripper_height + 70)  # 0.95 = Conversion number between camera height and FOV
    pixel_to_mm = mm_width / 1280  # mm_height / px_height
    offset_mm_x = -offset_pixel_tuple[1] * pixel_to_mm
    offset_mm_y = -offset_pixel_tuple[0] * pixel_to_mm
    print("offset i mm ", offset_mm_x, offset_mm_y)
    return offset_mm_x, offset_mm_y


def showVideo(self):
    while config.cap.isOpened():
        ret, frame = config.cap.read()
        if ret:
            frame = QR_Scanner_visualized(frame)
            cv2.imshow("hei,", frame)
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break


