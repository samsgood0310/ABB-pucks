import RAPID
import config
import pyueye as ueye
from pyueye_example_camera import *
from pyueye_example_utils import *
import cv2

cam = config.cam

nRet = ueye.is_CaptureVideo(cam.handle(), ueye.IS_DONT_WAIT)
img_buffer = ImageBuffer()

while True:

    #cam.freeze_video(True)  # Freeze video captures a single image
    #nRet = ueye.is_WaitForNextImage(cam.handle(), 1000, img_buffer.mem_ptr, img_buffer.mem_id)
    img_data = ImageData(cam.handle(), img_buffer)
    array = img_data.as_1d_image()
    #scanned_img = QR_Scanner_visualized(array)
    cv2.imshow("hei", array)
    img_data.unlock()
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break