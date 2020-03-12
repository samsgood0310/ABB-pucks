import cv2 as cv

import configparser
import time

"""from QR_Reader import QR_Scanner
from pyueye_example_camera import Camera
from pyueye import ueye
from pyueye_example_utils import ImageData, ImageBuffer
from numpy import median
import ImageFunctions_CV


# List with rough indicators where the best exposure lies
range_indicator = []

# List with exposure values
exposure_values = []

# Exposure range (in ms)
exposure_low = 1
exposure_high = 66

# Initialize camera
cam = Camera()
cam.init()

# Change the format to 1280x960
formatID = ueye.UINT(8)
nRet = ueye.is_ImageFormat(cam.handle(), ueye.IMGFRMT_CMD_SET_FORMAT, formatID, ueye.sizeof(formatID))

# Allocate image memory
cam.alloc()

# Disable auto focus
ueye.is_Focus(cam.handle(), ueye.FOC_CMD_SET_DISABLE_AUTOFOCUS, None, 0)

# Set manual gain (should automatically disable auto gain)
gain = ueye.INT(10)
ueye.is_SetHardwareGain(cam.handle(), gain, ueye.IS_IGNORE_PARAMETER, ueye.IS_IGNORE_PARAMETER,
                        ueye.IS_IGNORE_PARAMETER)

# Disable auto exposure
dblEnable = ueye.DOUBLE(0)
dblDummy = ueye.DOUBLE(0)
ueye.is_SetAutoParameter(cam.handle(), ueye.IS_SET_ENABLE_AUTO_SENSOR_GAIN_SHUTTER, dblEnable, dblDummy)

# Increment
increment = 2

# Loop from lowest possible exposure to highest possible exposure, incremented by 2 (ms)
for exposure in range(exposure_low, exposure_high, increment):
    # Set new exposure
    newExposure = ueye.DOUBLE(exposure)
    ret = ueye.is_Exposure(cam.handle(), ueye.IS_EXPOSURE_CMD_SET_EXPOSURE, newExposure, ueye.sizeof(newExposure))

    time.sleep(0.1)

    img = ImageFunctions_CV.capture_image(cam, 500, 195)
    puck_list = QR_Scanner(img)
    print(puck_list)

    # Checking exposure
    d = ueye.DOUBLE()
    retVal = ueye.is_Exposure(cam.handle(), ueye.IS_EXPOSURE_CMD_GET_EXPOSURE, d, 8)
    if retVal == ueye.IS_SUCCESS:
        print('Currently set exposure time %8.3f ms' % d)

    # Position returns as None if no QR-code is found
    if puck_list:
        range_indicator.append(exposure)

    # Show image to see result of exposure setpoint change
    #cv.imshow('result', img)
    #cv.waitKey(0)

#_exposure = str(median(exposure_values))"""
_exposure = str(100000)

start = time.time()


config = configparser.ConfigParser()
config.read('exposure.ini')
cfgfile = open('exposure.ini', 'w')

# Updating the value for exposure
config.set('EXPOSURE', 'exposure', _exposure)

config.write(cfgfile)
cfgfile.close()

end = time.time()
print(end - start)

timing = 0.0005436041355133057  # average time divided by 1000
