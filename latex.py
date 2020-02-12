    if userinput == "1":
        config.puckdict.clear()  # Reset puckdict
        session.set_rapid_variable("WPW", 1)  # Robot goes to position for image acquisition

        session.wait_for_rapid()

        trans, rot = session.get_gripper_position()
        gripper_height = session.get_gripper_height()

        cam_pos = OpenCV_to_RAPID.get_camera_position(trans=trans, rot=rot)
        time.sleep(1)
        overviewImage()

        OpenCV_to_RAPID.create_robtargets(gripper_height=gripper_height, rot=rot, cam_pos=cam_pos)

        # session.set_rapid_variable("image_processed", "TRUE")
        # session.wait_for_rapid()

        # Send all robtargets and angles from dictionary to RAPID:
        # TODO: Find out which method works best; send all pucks at once or send them only when needed by RAPID
        pucknr = 1
        for key in sorted(config.puckdict):
            session.set_robtarget_variables("puck_target{}".format(pucknr), config.puckdict[key]["position"])
            session.set_rapid_variable("puck_angle{}".format(pucknr), config.puckdict[key]["angle"])
            pucknr += 1

    elif userinput == "2":
        print("Move puck to middle")
        pucknr = int(input('\nWhich puck do you want to move?: '))

        session.set_rapid_variable('which_puck', 2)

        # session.set_robtarget_variables('puck_position', positions[pucknr - 1])
        session.set_rapid_variable('WPW', 2)  # Position camera above puck

        session.wait_for_rapid()  # Wait for robot to be in position

        gripper_height = session.get_gripper_height()

        # Get close-up image of the puck and extract QR code's offset from middle
        offset_mm_x, offset_mm_y = closeupImage(gripper_height)
        session.set_rapid_variable('offset_x', offset_mm_x)  # Tell RAPID where the puck is
        session.set_rapid_variable('offset_y', offset_mm_y)  # Give RAPID the orientation of the puck
        session.set_rapid_variable('image_processed', "TRUE")  # Tell RAPID that it may proceed
