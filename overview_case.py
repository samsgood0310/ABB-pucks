import time
import session
from ImageFunctions import *
import OpenCV_to_RAPID
import config

config.puckdict.clear()  # Reset puckdict
session.set_rapid_variable("WPW", 1)  # Robot goes to position for image acquisition

session.wait_for_rapid()

trans, rot = session.get_gripper_position()
gripper_height = session.get_gripper_height()

cam_pos = OpenCV_to_RAPID.get_camera_position(trans=trans, rot=rot)

overviewImage()
for key in config.puckdict:
    print(config.puckdict[key]["position"])

OpenCV_to_RAPID.create_robtargets(gripper_height=gripper_height, rot=rot, cam_pos=cam_pos)

# session.set_rapid_variable("image_processed", "TRUE")
# session.wait_for_rapid()

# Send all robtargets and angles from dictionary to RAPID:
for key in sorted(config.puckdict):
    pucknr = 1
    session.set_robtarget_variables("puck_target{}".format(pucknr), config.puckdict[key]["position"])
    session.set_rapid_variable("puck_angle{}".format(pucknr), config.puckdict[key]["angle"])
    pucknr += 1
