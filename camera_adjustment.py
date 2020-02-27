import cv2
from pyueye import ueye
import numpy as np
import RAPID
import time
import config
import OpenCV_to_RAPID
import ImageFunctions_CV
import QR_Reader

norbert = RAPID.RAPID()  # Initialize robot communication
norbert.request_rmmp()  # Request mastership
norbert.reset_pp()  # Program pointer to main
norbert.motors_on()

norbert.set_rapid_variable("WPW", 5)  # Start camera adjustment procedure in RAPID

norbert.wait_for_rapid()

trans, rot = norbert.get_gripper_position()
gripper_height = norbert.get_gripper_height()

cam_pos = OpenCV_to_RAPID.get_camera_position(trans=trans, rot=rot)

while not config.puckdict:
    ImageFunctions_CV.overviewImage_ueye()

for key in config.puckdict:
    adjustment_x = (config.puckdict[key]["position"][0] * 30) / (gripper_height + 70)
    adjustment_y = (config.puckdict[key]["position"][1] * 30) / (gripper_height + 70)
    config.puckdict[key]["position"][0] -= adjustment_x
    config.puckdict[key]["position"][1] -= adjustment_y

OpenCV_to_RAPID.create_robtargets(gripper_height=gripper_height, rot=rot, cam_pos=cam_pos)

for key in config.puckdict:
    print("robtarget:", config.puckdict[key]["position"])

norbert.set_robtarget_variables("puck_target", config.puckdict["Puck#1"]["position"])
norbert.set_rapid_variable("puck_angle", config.puckdict["Puck#1"]["angle"])
config.puckdict.clear()

norbert.set_rapid_variable('image_processed', 'TRUE')

norbert.wait_for_rapid()  # Wait for robot to be in position

ret = ueye.is_Focus(config.cam.handle(), ueye.FOC_CMD_SET_MANUAL_FOCUS,
                        config.focus_closeup, ueye.sizeof(config.focus_closeup))
img_buffer = config.ImageBuffer()  # Create image buffer
config.cam.freeze_video(True)  # Freeze video captures a single image after initializing the camera

time.sleep(0.1)
nRet = ueye.is_WaitForNextImage(config.cam.handle(), 1000, img_buffer.mem_ptr, img_buffer.mem_id)
img_data = config.ImageData(config.cam.handle(), img_buffer)
array = img_data.as_1d_image()
img_data.unlock()

gripper_height_low = norbert.get_gripper_height()

pos, img = QR_Reader.QR_Scanner(array)
norbert.set_rapid_variable('image_processed', 'TRUE')

mm_width = 0.95 * (gripper_height + 70)  # 0.95 = Conversion number between camera height and FOV
pixel_to_mm = mm_width / 1280  # mm_width / px_width

pos_low = [x*pixel_to_mm for x in pos]

ret = ueye.is_Focus(config.cam.handle(), ueye.FOC_CMD_SET_MANUAL_FOCUS,
                        config.focus_overview, ueye.sizeof(config.focus_overview))
img_buffer = config.ImageBuffer()  # Create image buffer

norbert.wait_for_rapid()

config.cam.freeze_video(True)  # Freeze video captures a single image after initializing the camera

time.sleep(0.2)
nRet = ueye.is_WaitForNextImage(config.cam.handle(), 1000, img_buffer.mem_ptr, img_buffer.mem_id)
img_data = config.ImageData(config.cam.handle(), img_buffer)
array = img_data.as_1d_image()
img_data.unlock()

gripper_height_high = norbert.get_gripper_height()

pos, img = QR_Reader.QR_Scanner(array)
norbert.set_rapid_variable('image_processed', 'TRUE')

mm_width = 0.95 * (gripper_height + 70)  # 0.95 = Conversion number between camera height and FOV
pixel_to_mm = mm_width / 1280  # mm_width / px_width

pos_high = [x*pixel_to_mm for x in pos]

delta_h = gripper_height_high - gripper_height_low
delta_x = pos_high[0] - pos_low[0]
delta_y = pos_high[1] - pos_low[1]

slope_x = delta_x / delta_h
slope_y = delta_y / delta_h

with open('camera_adjustment_XS.txt', 'a') as the_file:
            the_file.write("{0},{1}\n".format(slope_x, slope_y))

norbert.motors_off()
norbert.cancel_rmmp()
