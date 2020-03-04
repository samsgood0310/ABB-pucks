from requests import Session
from requests.auth import HTTPDigestAuth

session = Session()

rudolf_url = 'http://152.94.0.39'
digest_auth = HTTPDigestAuth('Default User', 'robotics')

payload = {'ctrl-state': 'motoron'}
resp = session.post(rudolf_url + "/rw/panel/ctrlstate?action=setctrlstate", auth=digest_auth, data=payload)