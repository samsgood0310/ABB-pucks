import config
import OpenCV_to_RAPID
import ImageFunctions_CV
import RAPID
import random

random_target = [random.randint(-50, 150), random.randint(-150, 150), 0]

robtarget_pucks = []
puck_to_RAPID = 0

# Initialize robot communication, start motors, and execute RAPID program
norbert = RAPID.RAPID()
norbert.request_rmmp()
norbert.start_RAPID()  # NB! Starts RAPID execution from main

while norbert.is_running():
    print("""
        1. Image from above
        2. Move puck to middle
        3. Stack pucks
        4. Rotate puck
        5. Exit""")

    userinput = input('\nWhat should RAPID do?: ')

    if userinput == '3':
        print("Stack pucks")
        norbert.set_rapid_variable("WPW", 3)
        norbert.wait_for_rapid()

        while not robtarget_pucks:
            ImageFunctions_CV.findPucks(config.cam, norbert, robtarget_pucks, 195)
        print(robtarget_pucks)

        while True:

            pucknr = min(int(x.nr) for x in robtarget_pucks)

            for x in robtarget_pucks:
                if x.nr == pucknr:
                    puck_to_RAPID = x
                    break

            norbert.set_robtarget_variables("puck_target", puck_to_RAPID.get_xyz())
            norbert.set_rapid_variable("puck_angle", puck_to_RAPID.get_puckang())
            norbert.set_rapid_variable("image_processed", "TRUE")

            robtarget_pucks.remove(puck_to_RAPID)

            norbert.wait_for_rapid()

            ImageFunctions_CV.findPucks(config.cam, norbert, robtarget_pucks, 160)

            pucknr = min(int(x.nr) for x in robtarget_pucks)

            for x in robtarget_pucks:
                if x.nr == pucknr:
                    puck_to_RAPID = x
                    break

            norbert.set_robtarget_variables("puck_target", puck_to_RAPID.get_xyz())
            norbert.set_rapid_variable("image_processed", "TRUE")

            robtarget_pucks.remove(puck_to_RAPID)

            norbert.wait_for_rapid()



    if userinput == '6':

        while norbert.is_running():
            norbert.set_rapid_variable("WPW", 6)
            norbert.wait_for_rapid()

            random_target = [random.randint(-50, 150), random.randint(-150, 150), 0]
            norbert.set_robtarget_variables("randomTarget", random_target)
            while not robtarget_pucks:
                ImageFunctions_CV.findPucks(config.cam, norbert, robtarget_pucks, 195)

            puck_to_RAPID = robtarget_pucks[0]
            whichPuck = 3
            """while not puck_to_RAPID:
                whichPuck = input("Which puck do you wish to move?")
                for x in robtarget_pucks:
                    if x.nr == whichPuck:
                        puck_to_RAPID = x
                        break
                else:
                    print("The selected puck has not been detected! Please enter another number.\n")
                    continue
                break"""

            norbert.set_robtarget_variables("puck_target", puck_to_RAPID.get_xyz())
            norbert.set_rapid_variable("image_processed", "TRUE")

            robtarget_pucks.remove(puck_to_RAPID)

            norbert.wait_for_rapid()
            ImageFunctions_CV.findPucks(config.cam, norbert, robtarget_pucks, 160)

            for x in robtarget_pucks:
                if x.nr == whichPuck:
                    puck_to_RAPID = x
                    break

            """puck_to_RAPID = None
            while True:
                whichPuck = input("Which puck do you wish to move?")
                puck_to_RAPID = next((puck for puck in robtarget_pucks if puck.nr == whichPuck), None)
                if puck_to_RAPID:
                    break
                else:
                    print("The selected puck has not been detected! Please enter another number.\n")"""

            # TODO: Perhaps it is not needed to enter close up puck into the same list

            norbert.set_robtarget_variables("puck_target", puck_to_RAPID.get_xyz())
            robtarget_pucks.clear()
            norbert.set_rapid_variable("image_processed", "TRUE")