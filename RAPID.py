from requests.auth import HTTPDigestAuth
from requests import Session
import xml.etree.ElementTree as ET
import ast
import time
import json

# set of symbols that are used to organize ET objects
namespace = '{http://www.w3.org/1999/xhtml}'


class RAPID:
    """Struct for communicating with RobotWare through Robot Web Services (Rest API)"""

    def __init__(self, base_url='http://152.94.0.38', username='Default User', password='robotics'):
        self.base_url = base_url
        self.username = username
        self.password = password
        self.digest_auth = HTTPDigestAuth(self.username, self.password)
        # create persistent HTTP communication
        self.session = Session()

    def set_rapid_variable(self, var, value):
        payload = {'value': value}
        self.session.post(self.base_url + '/rw/rapid/symbol/data/RAPID/T_ROB1/' + var + '?action=set',
                          auth=self.digest_auth, data=payload)

    def get_rapid_variable(self, var):
        resp = self.session.get(self.base_url + '/rw/rapid/symbol/data/RAPID/T_ROB1/' + var + ';value?json=1',
                                    auth=self.digest_auth)
        json_string = resp.text
        _dict = json.loads(json_string)
        value = _dict["_embedded"]["_state"][0]["value"]
        return value

    def get_robtarget_variables(self, var):
        resp = self.session.get(self.base_url + '/rw/rapid/symbol/data/RAPID/T_ROB1/' + var + ';value?json=1',
                                    auth=self.digest_auth)

        json_string = resp.text
        _dict = json.loads(json_string)
        data = _dict["_embedded"]["_state"][0]["value"]
        data_list = ast.literal_eval(data)  # Convert the pure string from data to list
        trans = data_list[0]  # Get x,y,z from robtarget relative to work object (table)
        rot = data_list[1]  # Get orientation of robtarget

        return trans, rot

    def get_gripper_position(self):
        resp = self.session.get(self.base_url +
                    '/rw/motionsystem/mechunits/ROB_1/robtarget/?tool=tGripper&wobj=wobjTableN&coordinate=Wobj',
                    auth=self.digest_auth)
        # using ET to find and locate rapid variable, print() must be called to view the variable in the run tab
        root = ET.fromstring(resp.text)

        if root.findall(".//{0}li[@class='ms-robtargets']".format(namespace)):
            data = root.findall(".//{0}li[@class='ms-robtargets']/{0}span".format(namespace))
            x = int(float(data[0].text))
            y = int(float(data[1].text))
            z = int(float(data[2].text))
            trans = [x, y, z]

            a = float(data[3].text)
            b = float(data[4].text)
            c = float(data[5].text)
            d = float(data[6].text)
            rot = [a, b, c, d]

            return trans, rot

    def get_gripper_height(self):
        trans, rot = self.get_gripper_position()
        height = trans[2]

        return height

    def set_robtarget_variables(self, var, trans):
        self.set_rapid_variable(var, "[[" + ','.join(
            [str(s) for s in trans]) + "],[0, 1, 0, 0],[-1,0,0,0],[9E+9,9E+9,9E+9,9E+9,9E+9,9E+9]]")

    def wait_for_rapid(self):
        # Wait for camera to be in position
        while self.get_rapid_variable('ready_flag') == "FALSE" and self.is_running():
            time.sleep(0.1)
        #time.sleep(1)
        self.set_rapid_variable('ready_flag', "FALSE")

    def set_offset_variables(self, var, value):
        self.set_rapid_variable(var, "[" + ','.join([str(s) for s in value]) + "]")

    def reset_pp(self):
        # Resets program pointer in RAPID
        self.session.post(self.base_url + '/rw/rapid/execution?action=resetpp', auth=self.digest_auth)

    def request_rmmp(self, timeout=5):
        t1 = time.time()
        resp = self.session.post(self.base_url + '/users/rmmp', auth=self.digest_auth, data={'privilege': 'modify'})

    def cancel_rmmp(self):
        resp = self.session.post(self.base_url + '/users/rmmp?action=cancel', auth=self.digest_auth)

    def motors_on(self):
        # Turn motors on
        payload = {'ctrl-state': 'motoron'}
        resp = self.session.post(self.base_url + "/rw/panel/ctrlstate?action=setctrlstate",
                                    auth=self.digest_auth, data=payload)

        if resp.status_code == 204:
            print("Robot motors turned on")
        else:
            print("Could not turn on motors. The controller might be in manual mode")

    def motors_off(self):
        # Turn motors off
        payload = {'ctrl-state': 'motoroff'}
        resp = self.session.post(self.base_url + "/rw/panel/ctrlstate?action=setctrlstate",
                                 auth=self.digest_auth, data=payload)

        if resp.status_code == 204:
            print("Robot motors turned off")
        else:
            print("Could not turn off motors")

    def start_RAPID(self):
        self.reset_pp()
        payload = {'regain': 'continue', 'execmode': 'continue', 'cycle': 'once', 'condition': 'none',
                   'stopatbp': 'disabled', 'alltaskbytsp': 'false'}
        resp = self.session.post(self.base_url + "/rw/rapid/execution?action=start",
                                 auth=self.digest_auth, data=payload)
        """if resp.status_code == 204:
            print("RAPID execution started")
        else:
            print("Could not start RAPID, maybe motors are turned off")"""

    def stop_RAPID(self):
        resp = self.session.post(self.base_url + "/rw/rapid/execution?action=stop", auth=self.digest_auth)

    def get_execution_state(self):
        resp = self.session.get(self.base_url + "/rw/rapid/execution?json=1", auth=self.digest_auth)
        json_string = resp.text
        _dict = json.loads(json_string)
        data = _dict["_embedded"]["_state"][0]["ctrlexecstate"]
        return data

    def is_running(self):
        execution_state = self.get_execution_state()
        if execution_state == "running":
            return True
        else:
            return False