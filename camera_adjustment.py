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
norbert.start_RAPID()  # NB! Starts RAPID execution from main
while True:
    norbert.set_rapid_variable("WPW", 5)  # Start camera adjustment procedure in RAPID

    norbert.wait_for_rapid()

    robtarget_pucks = []

    ImageFunctions_CV.findPucks(config.cam, norbert, robtarget_pucks, 195, cam_comp=False)

    norbert.set_robtarget_variables("puck_target", robtarget_pucks[0].get_xyz())
    norbert.set_rapid_variable("image_processed", "TRUE")

    robtarget_pucks.clear()

    norbert.wait_for_rapid()

    ImageFunctions_CV.findPucks(config.cam, norbert, robtarget_pucks, 160, cam_comp=False)

    norbert.set_rapid_variable("image_processed", "TRUE")

    pos_low = robtarget_pucks[0].get_xyz()
    print("low:", pos_low)

    norbert.wait_for_rapid()

    robtarget_pucks.clear()

    ImageFunctions_CV.findPucks(config.cam, norbert, robtarget_pucks, 195, cam_comp=False)

    pos_high = robtarget_pucks[0].get_xyz()
    print("high:", pos_high)

    delta_h = 500 - 120
    delta_x = pos_high[0] - pos_low[0]
    delta_y = pos_high[1] - pos_low[1]

    slope_x = delta_x / delta_h
    slope_y = delta_y / delta_h

    """with open('camera_adjustment_XS.txt', 'a') as the_file:
                the_file.write("{0},{1}\n".format(slope_x, slope_y))"""
