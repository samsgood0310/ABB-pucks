import cv2
from pyueye import ueye
from pyueye_example_camera import Camera
from pyueye_example_utils import ImageData, ImageBuffer
import time
import numpy as np

# Initialize camera
cam = Camera()
cam.init()

nRet = ueye.is_ResetToDefault(cam.handle())

# Change the format to 1280x960
formatID = ueye.UINT(8)
nRet = ueye.is_ImageFormat(cam.handle(), ueye.IMGFRMT_CMD_SET_FORMAT, formatID, ueye.sizeof(formatID))

cam.alloc()  # Allocate image memory

# Disable auto exposure
dblEnable = ueye.DOUBLE(0)
dblDummy = ueye.DOUBLE(0)
ueye.is_SetAutoParameter(cam.handle(), ueye.IS_SET_ENABLE_AUTO_SENSOR_GAIN_SHUTTER, dblEnable, dblDummy)

newExposure = ueye.DOUBLE(30)
ret = ueye.is_Exposure(cam.handle(), ueye.IS_EXPOSURE_CMD_SET_EXPOSURE, newExposure, ueye.sizeof(newExposure))

ueye.is_Focus(cam.handle(), ueye.FOC_CMD_SET_DISABLE_AUTOFOCUS, None, 0)  # Disable autofocus

focus_overview = ueye.INT(205)  # Focus value for overview image (taken from 570mm above table)
focus_closeup = ueye.INT(144)  # Focus value for closeup image (taken from 190mm above table)


"""
exp_min = ueye.DOUBLE()
ret = ueye.is_Exposure(cam.handle(), ueye.IS_EXPOSURE_CMD_GET_EXPOSURE_RANGE_MIN, exp_min, ueye.sizeof(exp_min))
exp_max = ueye.DOUBLE()
ret = ueye.is_Exposure(cam.handle(), ueye.IS_EXPOSURE_CMD_GET_EXPOSURE_RANGE_MAX, exp_max, ueye.sizeof(exp_max))
print(exp_min, exp_max)
exp_def = ueye.DOUBLE()
ret = ueye.is_Exposure(cam.handle(), ueye.IS_EXPOSURE_CMD_GET_EXPOSURE_DEFAULT, exp_def, ueye.sizeof(exp_def))
print(exp_def)

disable = ueye.DOUBLE(0)
dummy = ueye.DOUBLE(0)
ret = ueye.is_SetAutoParameter(cam.handle(), ueye.IS_SET_ENABLE_AUTO_SENSOR_GAIN_SHUTTER, disable, dummy)
exp_val = ueye.DOUBLE(10.0)
ret = ueye.is_Exposure(cam.handle(), ueye.IS_EXPOSURE_CMD_SET_EXPOSURE, exp_val, ueye.sizeof(exp_val))

exp_def = ueye.DOUBLE()
ret = ueye.is_Exposure(cam.handle(), ueye.IS_EXPOSURE_CMD_GET_EXPOSURE, exp_def, ueye.sizeof(exp_def))
print("set exp to", exp_def)"""

if __name__ == "__main__":

    import numpy as np
    #from QR_Reader import QR_Scanner
    #import OpenCV_to_RAPID
    import yaml


    #newExposure = ueye.DOUBLE(9)
    #ret = ueye.is_Exposure(cam.handle(), ueye.IS_EXPOSURE_CMD_SET_EXPOSURE, newExposure, ueye.sizeof(newExposure))



    """contents = np.genfromtxt(r'robtarget_error.txt', delimiter=',')

    sum_error_x = 0
    sum_error_y = 0
    for content in contents:
        sum_error_x += abs(content[0])
        sum_error_y += abs(content[1])

    average_error_x = sum_error_x / len(contents)
    average_error_y = sum_error_y / len(contents)contents = np.genfromtxt(r'robtarget_error.txt', delimiter=',')

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
    print(max_error_y)"""

    """cam = Camera()
    cam.init()

    # Change the format to 1280x960
    formatID = ueye.UINT(8)
    nRet = ueye.is_ImageFormat(cam.handle(), ueye.IMGFRMT_CMD_SET_FORMAT, formatID, ueye.sizeof(formatID))

    cam.alloc()  # Allocate image memory
    ueye.is_Focus(cam.handle(), ueye.FOC_CMD_SET_DISABLE_AUTOFOCUS, None, 0)  # Disable autofocus
    focus_overview = ueye.INT(200)  # Focus value for overview image (taken from 570mm above table)
    focus_closeup = ueye.INT(165)  # Focus value for closeup image (taken from 190mm above table)

    ret = ueye.is_Focus(cam.handle(), ueye.FOC_CMD_SET_MANUAL_FOCUS,
                        focus_overview, ueye.sizeof(focus_overview))
    img_buffer = ImageBuffer()  # Create image buffer
    cam.freeze_video(True)  # Freeze video captures a single image after initializing the camera

    time.sleep(0.1)
    nRet = ueye.is_WaitForNextImage(cam.handle(), 1000, img_buffer.mem_ptr, img_buffer.mem_id)
    img_data = ImageData(cam.handle(), img_buffer)
    array = img_data.as_1d_image()"""

    #with open("calibration_matrix.yaml", "r") as f:
    #    data = yaml.load(f, Loader=yaml.FullLoader)

    #print(data)

    """mtx = data['camera_matrix']
    dist = data['dist_coeff']
    new_mtx = data['new_camera_matrix']

    mtx = np.asarray(mtx, dtype=np.float32)
    dist = np.asarray(dist, dtype=np.float32)
    new_mtx = np.asarray(new_mtx, dtype=np.float32)

    dst = cv2.undistort(array, mtx, dist, None, new_mtx)"""
