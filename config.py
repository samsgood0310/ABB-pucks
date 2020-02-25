import math
import cv2
from pyueye import ueye
from pyueye_example_camera import Camera
from pyueye_example_utils import ImageData, ImageBuffer
import time
import os


"""cam = Camera()
cam.init()
cam.set_colormode(ueye.IS_CM_BGR8_PACKED)
cam.set_aoi(0, 0, 1280, 960)
cam.alloc()
cam.capture_video()"""

#array = img_data.as_1d_image()

#cv2.imshow("hei", array)

"""cap = cv2.VideoCapture(1)
px_width = 1280
px_height = 960
cap.set(3, px_width)
cap.set(4, px_height)
cap.set(cv2.CAP_PROP_AUTOFOCUS, 3)"""
cam = Camera()
cam.init()
cam.set_aoi(0, 0, 10, 20)
cam.alloc()
ueye.is_Focus(cam.handle(), ueye.FOC_CMD_SET_DISABLE_AUTOFOCUS, None, 0)
puckdict = {}
focus_overview = ueye.INT(190)
focus_closeup = ueye.INT(165)

if __name__ == "__main__":
    from matplotlib import pyplot as plt
    import numpy as np

    #ret = ueye.is_Focus(cam.handle(), ueye.FOC_CMD_GET_MANUAL_FOCUS_MIN, value, ueye.sizeof(value))
    #print(value.value)
    focus = ueye.INT(190)
    ret = ueye.is_Focus(cam.handle(), ueye.FOC_CMD_SET_MANUAL_FOCUS, focus, ueye.sizeof(focus))
    img_buffer = ImageBuffer()  # Create image buffer
    cam.freeze_video(True)  # Freeze video captures a single image after initializing the camera
    #ueye.is_Focus(cam.handle(), ueye.FOC_CMD_SET_ENABLE_AUTOFOCUS_ONCE, None, 0)

    time.sleep(2)
    nRet = ueye.is_WaitForNextImage(cam.handle(), 1000, img_buffer.mem_ptr, img_buffer.mem_id)
    img_data = ImageData(cam.handle(), img_buffer)
    array = img_data.as_1d_image()
    cv2.imshow("hei", array)
    cv2.waitKey(0)
    #if cv2.waitKey(10) & 0xFF == ord('q'):
    img_data.unlock()  # Important action"""
    #cam.exit()

    #nRet = cam.capture_video()
    img_buffer = ImageBuffer()
    cam.freeze_video(True)
    # ueye.is_Focus(cam.handle(), ueye.FOC_CMD_SET_ENABLE_AUTOFOCUS_ONCE, None, 0)

    time.sleep(2)
    nRet = ueye.is_WaitForNextImage(cam.handle(), 1000, img_buffer.mem_ptr, img_buffer.mem_id)
    img_data = ImageData(cam.handle(), img_buffer)
    array = img_data.as_1d_image()
    cv2.imshow("hei", array)
    cv2.waitKey(0)
    img_data.unlock()


    """if "hei" not in puckdict:
        puckdict["puck3"] = {"position": [10, 20], "angle": 5}
        puckdict["puck2"] = {"position": [30, 50], "angle": 50}
        puckdict["puck2"] = {"position": [40, 60], "angle": 90}
        puckdict["puck7"] = {"position": [25, 30], "angle": -40}
        puckdict["puck4"] = {"position": [23, 10], "angle": 31}
    while cap.isOpened():
        #cap.set(28, i)
        #cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)
        #cap.set(cv2.CAP_PROP_AUTOFOCUS, 1)
        ret, frame = cap.read()
        #print(cap.get(cv2.CAP_PROP_FOCUS))
        print(cap.get(cv2.CAP_PROP_AUTOFOCUS))
        #cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)
        #cap.set(cv2.CAP_PROP_AUTOFOCUS, 1)
        #cap.set(cv2.CAP_PROP_FOCUS, 112.0)
        #cap.set(cv2.CAP_PROP_FOCUS, 1)
        # create a CLAHE object (Arguments are optional).
        #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        #clahe = cv2.createCLAHE(clipLimit=2, tileGridSize=(8, 8))

        #cl1 = clahe.apply(frame)
        #cl1 = QR_Reader.QR_Scanner_visualized(frame)
        #stack = np.hstack((gray, cl1))
        #print(cv2.Laplacian(frame, cv2.CV_64F).var())
        cv2.imshow("hei,", frame)
        #i+=5
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

print(puckdict)"""

"""ret, frame = cap.read()
if ret:
    grayscale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    grayscale2 = grayscale.copy()
    #normalized = cv2.normalize(grayscale, None)
    #hist = cv2.calcHist([img], [0], None, [256], [0, 256])

    #cv2.normalize(grayscale2, grayscale2, alpha=0, beta=255, norm_type=cv2.NORM_L1)
    #plt.hist(grayscale2.ravel(), 256, [0, 256]);
    #plt.show()
#hstack = np.hstack((grayscale, grayscale2))
#cv2.imshow("hei", hstack)
#cv2.waitKey(0)
x, y, w, h = 364, 633, 791, 273
ROI = grayscale[y:y + h, x:x + w]

# Calculate mean and STD
mean, STD = cv2.meanStdDev(ROI)

# Clip frame to lower and upper STD
offset = 0.2
clipped = np.clip(grayscale, mean - offset * STD, mean + offset * STD).astype(np.uint8)
blur = cv2.bilateralFilter(src=grayscale, d=3, sigmaColor=75, sigmaSpace=75)
# Normalize to range
result = cv2.normalize(blur, blur, 0, 255, norm_type=cv2.NORM_MINMAX, dtype=-1)
result = cv2.cvtColor(result, cv2.COLOR_GRAY2BGR)

cv2.imshow('image', grayscale)
cv2.imshow('result', result)
cv2.waitKey()"""
