from pyueye import ueye
from pyueye_example_utils import ImageData, ImageBuffer
from pyueye_example_camera import Camera
import cv2
import numpy as np


def copy_image(self, image_data):  # copy image_data to self (.np_img, .image and .pixmap)
    # just copy image_data (from camera) into self
    tempBilde = image_data.as_1d_image()
    if np.min(tempBilde) != np.max(tempBilde):
        A = self.np_img = np.copy(tempBilde[:, :, [2, 1, 0]])
        print('  A = self.np_img is an ndarray of %s, shape %s.' % (A.dtype.name, str(A.shape)))
    # end if
    image_data.unlock()  # important action
    return


def cameraOn(self):
    if not self.camOn:
        self.cam = Camera()
        self.cam.init()  # gives error when camera not connected
        self.cam.set_colormode(ueye.IS_CM_BGR8_PACKED)
        # This function is currently not supported by the camera models USB 3 uEye XC and XS.
        self.cam.set_aoi(0, 0, 720, 1280)  # but this is the size used
        self.cam.alloc(3)  # argument is number of buffers
        # just set a camera option (parameter) even if it is not used here
        d = ueye.double()
        retVal = ueye.is_SetFrameRate(self.cam.handle(), 2.0, d)
        if retVal == ueye.IS_SUCCESS:
            print('  frame rate set to                      %8.3f fps' % d)
        retVal = ueye.is_Exposure(self.cam.handle(), ueye.IS_EXPOSURE_CMD_GET_EXPOSURE_DEFAULT, d, 8)
        if retVal == ueye.IS_SUCCESS:
            print('  default setting for the exposure time  %8.3f ms' % d)
        retVal = ueye.is_Exposure(self.cam.handle(), ueye.IS_EXPOSURE_CMD_GET_EXPOSURE_RANGE_MIN, d, 8)
        if retVal == ueye.IS_SUCCESS:
            print('  minimum exposure time                  %8.3f ms' % d)
        retVal = ueye.is_Exposure(self.cam.handle(), ueye.IS_EXPOSURE_CMD_GET_EXPOSURE_RANGE_MAX, d, 8)
        if retVal == ueye.IS_SUCCESS:
            print('  maximum exposure time                  %8.3f ms' % d)
        retVal = ueye.is_Exposure(self.cam.handle(), ueye.IS_EXPOSURE_CMD_GET_EXPOSURE, d, 8)
        if retVal == ueye.IS_SUCCESS:
            print('  currently set exposure time            %8.3f ms' % d)
        d = ueye.double(25.0)
        retVal = ueye.is_Exposure(self.cam.handle(), ueye.IS_EXPOSURE_CMD_SET_EXPOSURE, d, 8)
        if retVal == ueye.IS_SUCCESS:
            print('  tried to changed exposure time to      %8.3f ms' % d)
        retVal = ueye.is_Exposure(self.cam.handle(), ueye.IS_EXPOSURE_CMD_GET_EXPOSURE, d, 8)
        if retVal == ueye.IS_SUCCESS:
            print('  currently set exposure time            %8.3f ms' % d)
        #
        self.camOn = True
        self.qaCameraOn.setEnabled(False)
        self.qaGetOneImage.setEnabled(True)
        self.qaGetOneImage.setToolTip("Capture one single image")
        self.qaCameraOff.setEnabled(True)
        self.qaCameraOff.setToolTip("Turn camera off again.")
        print('%s: cameraOn() Camera started ok' % self.appFileName)
    #
    return


def getOneImage(self):
    if self.camOn:
        print('%s: getOneImage() try to capture one image' % self.appFileName)
        imBuf = ImageBuffer()  # used to get return pointers
        self.cam.freeze_video(True)
        retVal = ueye.is_WaitForNextImage(self.cam.handle(), 1000, imBuf.mem_ptr, imBuf.mem_id)
        if retVal == ueye.IS_SUCCESS:
            print('  ueye.IS_SUCCESS: image buffer id = %i' % imBuf.mem_id)
            self.copy_image(ImageData(self.cam.handle(), imBuf))  # copy image_data to self
            # and display it
    # end if
    #
    return