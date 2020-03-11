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
norbert.wait_for_rapid()

cam_comp = False

while True:
    norbert.set_rapid_variable("WPW", 5)  # Start camera adjustment procedure in RAPID

    norbert.wait_for_rapid()

    robtarget_pucks = []

    while not robtarget_pucks:
        ImageFunctions_CV.findPucks(config.cam, norbert, robtarget_pucks, 195, cam_comp=cam_comp)

    norbert.set_robtarget_variables("puck_target", robtarget_pucks[0].get_xyz())
    norbert.set_rapid_variable("image_processed", "TRUE")

    robtarget_pucks.clear()

    norbert.wait_for_rapid()

    while not robtarget_pucks:
        ImageFunctions_CV.findPucks(config.cam, norbert, robtarget_pucks, 160, cam_comp=cam_comp)

    norbert.set_rapid_variable("image_processed", "TRUE")

    pos_low = robtarget_pucks[0].get_xyz()
    print(f'Low robtarget: ({pos_low[0]:.1f},{pos_low[1]:.1f}')
    error_x = 150-pos_low[0]
    error_y = 150-pos_low[1]
    print(f"Low error: ({error_x:.1f},{error_y:.1f})")
    #print("low:", pos_low)

    norbert.wait_for_rapid()

    robtarget_pucks.clear()
    while not robtarget_pucks:
        ImageFunctions_CV.findPucks(config.cam, norbert, robtarget_pucks, 195, cam_comp=cam_comp)

    pos_high = robtarget_pucks[0].get_xyz()
    print(f'High robtarget: ({pos_high[0]:.1f},{pos_high[1]:.1f}')
    error_x = 150 - pos_high[0]
    error_y = 150 - pos_high[1]
    print(f"High error: ({error_x:.1f},{error_y:.1f})")

    delta_h = 500 - 60
    delta_x = pos_high[0] - pos_low[0]
    delta_y = pos_high[1] - pos_low[1]

    slope_x = delta_x / delta_h
    slope_y = delta_y / delta_h

    if cam_comp:
        with open('camera_adjustment_XS.txt', 'a') as the_file:
            the_file.write("{0},{1}\n".format(slope_x, slope_y))

    # Previous: 0.028106499821647302,0.004115557794815522    -     0.0242737738280447,0.0035319402989294458
