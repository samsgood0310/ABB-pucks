import cv2 as cv
from pyueye_example_camera import Camera
from pyueye import ueye
from pyueye_example_utils import ImageData, ImageBuffer
import time

"""// Disable auto exposure
double dblEnable = 0;
double dblDummy = 0;
ret = is_SetAutoParameter(m_hCam, IS_SET_ENABLE_AUTO_SENSOR_GAIN_SHUTTER, &dblEnable, &dblDummy);

dblEnable = ueye.DOUBLE(0)
dblDummy = ueye.DOUBLE(0)
ret = is_SetAutoParameter(cam.handle(), IS_SET_ENABLE_AUTO_SENSOR_GAIN_SHUTTER, dblEnable, dblDummy);

// Set exposure manually
double newExposure = 50.0;
ret = is_Exposure(m_hCam, IS_EXPOSURE_CMD_SET_EXPOSURE, &newExposure, 8);"""

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

# Check exposure
d = ueye.DOUBLE()
retVal = ueye.is_Exposure(cam.handle(), ueye.IS_EXPOSURE_CMD_GET_EXPOSURE, d, 8)
if retVal == ueye.IS_SUCCESS:
    print('Currently set exposure time %8.3f ms' % d)

# Set exposure manually
newExposure = ueye.DOUBLE(66)
ret = ueye.is_Exposure(cam.handle(), ueye.IS_EXPOSURE_CMD_SET_EXPOSURE, newExposure, ueye.sizeof(newExposure))

# Create image buffer
img_buffer = ImageBuffer()

for exposure in range(exposure_low, exposure_high, 10):
    # Freeze video captures a single image after initializing the camera
    cam.freeze_video(True)

    # Set new exposure
    newExposure = ueye.DOUBLE(exposure)
    ret = ueye.is_Exposure(cam.handle(), ueye.IS_EXPOSURE_CMD_SET_EXPOSURE, newExposure, ueye.sizeof(newExposure))

    time.sleep(0.1)

    # Checking exposure
    retVal = ueye.is_Exposure(cam.handle(), ueye.IS_EXPOSURE_CMD_GET_EXPOSURE, d, 8)
    if retVal == ueye.IS_SUCCESS:
        print('Currently set exposure time %8.3f ms' % d)

    ueye.is_WaitForNextImage(cam.handle(), 1000, img_buffer.mem_ptr, img_buffer.mem_id)
    img_data = ImageData(cam.handle(), img_buffer)
    image = img_data.as_1d_image()

    # Show image to see result of brightness setpoint change
    cv.imshow('result', image)
    cv.waitKey(0)

    img_data.unlock()

    exposure += 10
