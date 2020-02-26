import cv2
from pyueye import ueye
from pyueye_example_camera import Camera
from pyueye_example_utils import ImageData, ImageBuffer
import time

# Initialize camera
cam = Camera()
cam.init()

# Change the format to 1280x960
formatID = ueye.UINT(8)
nRet = ueye.is_ImageFormat(cam.handle(), ueye.IMGFRMT_CMD_SET_FORMAT, formatID, ueye.sizeof(formatID))

cam.alloc()  # Allocate image memory
ueye.is_Focus(cam.handle(), ueye.FOC_CMD_SET_DISABLE_AUTOFOCUS, None, 0)  # Disable autofocus
focus_overview = ueye.INT(195)  # Focus value for overview image (taken from 570mm above table)
focus_closeup = ueye.INT(165)  # Focus value for closeup image (taken from 190mm above table)

puckdict = {}  # Initialize global puck dictionary

if __name__ == "__main__":
    from matplotlib import pyplot as plt
    import numpy as np
    contents = np.genfromtxt(r'robtarget_error.txt', delimiter=',')

    sum_error_x = 0
    sum_error_y = 0
    for content in contents:
        sum_error_x += abs(content[0])
        sum_error_y += abs(content[1])

    average_error_x = sum_error_x / len(contents)
    average_error_y = sum_error_y / len(contents)
    print("average_x", average_error_x)
    print("average_y", average_error_y)

    max_error_x = max([abs(sublist[0]) for sublist in contents])
    max_error_y = max([abs(sublist[1]) for sublist in contents])
    print(max_error_x)
    print(max_error_y)