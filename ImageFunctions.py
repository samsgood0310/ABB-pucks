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
            if is_blurry(img=frame, threshold=80):
                return "failed"
            else:
                pos, img = QR_Scanner(img=frame)
                if not config.puckdict:
                    continue
                print("success")
                return "success"
            #break

def closeupImage(gripper_height):
    """Grab several images at low height over the approximate position of a puck.
    If several pucks are seen, keep only the one closest to the center."""

    # TODO: Bryte while-loop når puck er funnet
    offset_pixel_tuple = 0

    while config.cap.isOpened():
        ret, frame = config.cap.read()  # Read image to np.array
        # Take x amount of images, depending on thresh_inc and the if statement:
        if is_blurry(img=frame, threshold=100):
            return "failed", 0, 0
        else:
            # Get position and orientation of QR code:
            offset_pixel_tuple, img = QR_Scanner(img=frame)
            if offset_pixel_tuple == 0:
                continue
            print("offset_pixel ", offset_pixel_tuple)
            # TODO: Check if several pucks are detected and only include the puck closest to the center of the frame
            break

    # Use resolution to make middle of image (x,y) = (0,0).
    # Now one can use offset in RAPID from current position:
    # TODO: Find height and width of image in mm
    mm_width = 0.95 * (gripper_height + 70)  # 0.95 = Conversion number between camera height and FOV
    pixel_to_mm = mm_width / 1280  # mm_height / px_height
    offset_mm_x = -offset_pixel_tuple[1] * pixel_to_mm
    offset_mm_y = -offset_pixel_tuple[0] * pixel_to_mm
    adjustment_x = (offset_mm_x * 30) / (gripper_height + 70)
    adjustment_y = (offset_mm_y * 30) / (gripper_height + 70)
    offset_mm_x -= adjustment_x
    offset_mm_y -= adjustment_y
    return "success", offset_mm_x, offset_mm_y


def showVideo(self):
    while config.cap.isOpened():
        ret, frame = config.cap.read()
        if ret:
            frame = QR_Scanner_visualized(frame)
            cv2.imshow("hei,", frame)
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break


def is_blurry(img, threshold):

    laplacian_variance = cv2.Laplacian(img, cv2.CV_64F).var()
    print("Blur", laplacian_variance)
    if laplacian_variance > threshold:
        return False
    else:
        return True
