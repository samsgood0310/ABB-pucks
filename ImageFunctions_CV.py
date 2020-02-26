import cv2
from QR_Reader import QR_Scanner, QR_Scanner_visualized
import config
from pyueye import ueye
import time

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


def overviewImage_ueye():
    ret = ueye.is_Focus(config.cam.handle(), ueye.FOC_CMD_SET_MANUAL_FOCUS,
                        config.focus_overview, ueye.sizeof(config.focus_overview))
    img_buffer = config.ImageBuffer()  # Create image buffer
    config.cam.freeze_video(True)  # Freeze video captures a single image after initializing the camera
    # ueye.is_Focus(cam.handle(), ueye.FOC_CMD_SET_ENABLE_AUTOFOCUS_ONCE, None, 0)

    time.sleep(0.1)
    nRet = ueye.is_WaitForNextImage(config.cam.handle(), 1000, img_buffer.mem_ptr, img_buffer.mem_id)
    img_data = config.ImageData(config.cam.handle(), img_buffer)
    array = img_data.as_1d_image()
    QR_Scanner(array)
    img_data.unlock()


def closeupImage(gripper_height):
    """Grab several images at low height over the approximate position of a puck.
    If several pucks are seen, keep only the one closest to the center."""

    ret = ueye.is_Focus(config.cam.handle(), ueye.FOC_CMD_SET_MANUAL_FOCUS,
                        config.focus_closeup, ueye.sizeof(config.focus_closeup))
    img_buffer = config.ImageBuffer()  # Create image buffer
    config.cam.freeze_video(True)  # Freeze video captures a single image after initializing the camera
    # ueye.is_Focus(cam.handle(), ueye.FOC_CMD_SET_ENABLE_AUTOFOCUS_ONCE, None, 0)

    time.sleep(0.1)
    nRet = ueye.is_WaitForNextImage(config.cam.handle(), 1000, img_buffer.mem_ptr, img_buffer.mem_id)
    img_data = config.ImageData(config.cam.handle(), img_buffer)
    array = img_data.as_1d_image()
    offset_pixel_tuple, img = QR_Scanner(img=array)
    img_data.unlock()

    if offset_pixel_tuple == 0:
        return False, 0, 0

    # Use resolution to make middle of image (x,y) = (0,0).
    # Now one can use offset in RAPID from current position:
    mm_width = 0.95 * (gripper_height + 70)  # 0.95 = Conversion number between camera height and FOV
    pixel_to_mm = mm_width / 1280  # mm_height / px_height
    offset_mm_x = -offset_pixel_tuple[1] * pixel_to_mm
    offset_mm_y = -offset_pixel_tuple[0] * pixel_to_mm
    adjustment_x = (offset_mm_x * 30) / (gripper_height + 70)
    adjustment_y = (offset_mm_y * 30) / (gripper_height + 70)
    offset_mm_x -= adjustment_x
    offset_mm_y -= adjustment_y
    return True, offset_mm_x, offset_mm_y


def showVideo(self):
    while config.cap.isOpened():
        nRet = config.ueye.is_Focus(config.cam_h, config.ueye.FOC_CMD_SET_ENABLE_AUTOFOCUS_ONCE, None, 0)
        if nRet == config.ueye.IS_SUCCESS:
            print("ueye success")
        else:
            print("ueye fail")
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
