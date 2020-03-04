import config
import OpenCV_to_RAPID
import ImageFunctions_CV
import RAPID
import random

random_target = [random.randint(-50, 150), random.randint(-150, 150), 0]

robtarget_pucks = []
actual_robtarget_pucks = []

norbert = RAPID.RAPID()
norbert.request_rmmp()
norbert.set_rapid_variable("WPW", 6)
norbert.wait_for_rapid()

norbert.set_robtarget_variables("randomTarget", random_target)

ImageFunctions_CV.findPucks(config.cam, norbert, robtarget_pucks, 195)

for puck in robtarget_pucks:
    puck_xyz = puck.pos + [puck.height]
    actual_robtarget_pucks.append(puck_xyz)
    print(puck_xyz)

norbert.set_robtarget_variables("puck_target", actual_robtarget_pucks[0])
norbert.set_rapid_variable("image_processed", "TRUE")
actual_robtarget_pucks.clear()
robtarget_pucks.clear()

norbert.wait_for_rapid()
ImageFunctions_CV.findPucks(config.cam, norbert, robtarget_pucks, 160)
for puck in robtarget_pucks:
    puck_xyz = puck.pos + [puck.height]
    actual_robtarget_pucks.append(puck_xyz)
    print(puck_xyz)
norbert.set_robtarget_variables("puck_target", actual_robtarget_pucks[0])
norbert.set_rapid_variable("image_processed", "TRUE")

