import cv2 as cv

from QR_Reader import QR_Scanner
from pyueye_example_camera import Camera
from pyueye import ueye
from pyueye_example_utils import ImageData, ImageBuffer
from numpy import median
import time

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

# Declare focus value for camera in overview position
focus_overview = ueye.INT(190)

# Set manual focus
ueye.is_Focus(cam.handle(), ueye.FOC_CMD_SET_MANUAL_FOCUS, focus_overview, ueye.sizeof(focus_overview))

# Set manual gain (should automatically disable auto gain)
gain = ueye.INT(10)
ueye.is_SetHardwareGain(cam.handle(), gain, ueye.IS_IGNORE_PARAMETER, ueye.IS_IGNORE_PARAMETER,
                        ueye.IS_IGNORE_PARAMETER)

# Disable auto exposure
dblEnable = ueye.DOUBLE(0)
dblDummy = ueye.DOUBLE(0)
ueye.is_SetAutoParameter(cam.handle(), ueye.IS_SET_ENABLE_AUTO_SENSOR_GAIN_SHUTTER, dblEnable, dblDummy)

# Set exposure manually
newExposure = ueye.DOUBLE(66)
ueye.is_Exposure(cam.handle(), ueye.IS_EXPOSURE_CMD_SET_EXPOSURE, newExposure, ueye.sizeof(newExposure))

# Check exposure
d = ueye.DOUBLE()
retVal = ueye.is_Exposure(cam.handle(), ueye.IS_EXPOSURE_CMD_GET_EXPOSURE, d, 8)
if retVal == ueye.IS_SUCCESS:
    print('Currently set exposure time %8.3f ms' % d)

# Create image buffer
img_buffer = ImageBuffer()

# Increment and round number
round_nr = 0
increment = 10
while True:
    for exposure in range(exposure_low, exposure_high, 10):
        # Set new exposure
        newExposure = ueye.DOUBLE(exposure)
        ret = ueye.is_Exposure(cam.handle(), ueye.IS_EXPOSURE_CMD_SET_EXPOSURE, newExposure, ueye.sizeof(newExposure))

        time.sleep(0.1)

        # Freeze video captures a single image after initializing the camera
        cam.freeze_video(True)

        # Checking exposure
        retVal = ueye.is_Exposure(cam.handle(), ueye.IS_EXPOSURE_CMD_GET_EXPOSURE, d, 8)
        if retVal == ueye.IS_SUCCESS:
            print('Currently set exposure time %8.3f ms' % d)

        ueye.is_WaitForNextImage(cam.handle(), 1000, img_buffer.mem_ptr, img_buffer.mem_id)
        img_data = ImageData(cam.handle(), img_buffer)
        image = img_data.as_1d_image()

        # Position returns as None if no QR-code is found
        position, img = QR_Scanner(image)

        if round_nr == 0:
            if position is not None:
                range_indicator.append(exposure)
        elif round_nr == 1:
            if position is not None:
                exposure_values.append(exposure)

        # Show image to see result of exposure setpoint change
        cv.imshow('result', image)
        cv.waitKey(0)

        img_data.unlock()

        exposure += increment

    # Round number
    round_nr += 1
    if round_nr == 2:
        break
    # Update increment and brightness values
    increment = 2
    exposure_low = range_indicator[0] - 10
    exposure_high = range_indicator[-1] + 10

median(exposure_values)
