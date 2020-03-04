from ImageFunctions_CV import *
import OpenCV_to_RAPID
import config
import random
import RAPID

norbert = RAPID.RAPID()

norbert.request_rmmp()
norbert.set_rapid_variable("ready_flag", "FALSE")

random_target = [0,0]

input("Press enter to start the program")
print("Program started")
norbert.set_rapid_variable("WPW", 1)  # Robot goes to position for image acquisition
norbert.reset_pp()

while True:
    config.puckdict.clear()  # Reset puckdict
    previous_random_target = random_target
    random_target = [random.randint(-50, 150), random.randint(-150, 150), 0]
    norbert.set_robtarget_variables("randomTarget", random_target)
    print(random_target)

    norbert.wait_for_rapid()

    trans, rot = norbert.get_gripper_position()
    gripper_height = norbert.get_gripper_height()

    cam_pos = OpenCV_to_RAPID.get_camera_position(trans=trans, rot=rot)

    while not config.puckdict:
        overviewImage_ueye()

    for key in config.puckdict:
        adjustment_x = (config.puckdict[key]["position"][0] * 30) / (gripper_height + 70)
        adjustment_y = (config.puckdict[key]["position"][1] * 30) / (gripper_height + 70)
        config.puckdict[key]["position"][0] -= adjustment_x
        config.puckdict[key]["position"][1] -= adjustment_y

    """for key in config.puckdict:
        print("pixel pos:", config.puckdict[key]["position"])"""

    OpenCV_to_RAPID.create_robtargets(gripper_height=gripper_height, rot=rot, cam_pos=cam_pos)

    for key in config.puckdict:
        print("robtarget:", config.puckdict[key]["position"])

    norbert.set_robtarget_variables("puck_target", config.puckdict["Puck#1"]["position"])
    norbert.set_rapid_variable("puck_angle", config.puckdict["Puck#1"]["angle"])

    norbert.set_rapid_variable('WPW', 2)  # Position camera above puck

    norbert.wait_for_rapid()  # Wait for robot to be in position
    gripper_height = norbert.get_gripper_height()
    camera_height = gripper_height + 70

    ret = False
    while not ret:
        ret, offset_mm_x, offset_mm_y = closeupImage(
            gripper_height)  # Get close-up image of the puck and extract QR code's offset from middle

    norbert.set_rapid_variable('offset_x', offset_mm_x)  # Tell RAPID where the puck is
    norbert.set_rapid_variable('offset_y', offset_mm_y)  # Give RAPID the orientation of the puck
    robtarget_x = config.puckdict["Puck#1"]["position"][0] + offset_mm_x
    robtarget_y = config.puckdict["Puck#1"]["position"][1] + offset_mm_y
    # print("correct position:", previous_random_target)
    # print("calculated position:({},{})".format(robtarget_x, robtarget_y))
    norbert.set_rapid_variable('image_processed', "TRUE")  # Tell RAPID that it may proceed
    norbert.set_rapid_variable("WPW", 1)  # Robot goes to position for image acquisition

    error_x = previous_random_target[0] - robtarget_x
    error_y = previous_random_target[1] - robtarget_y
    """with open('robtarget_error.txt', 'a') as the_file:
        the_file.write("{0},{1}\n".format(error_x, error_y))"""

    norbert.wait_for_rapid()