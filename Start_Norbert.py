from requests import Session
from requests.auth import HTTPDigestAuth

session = Session()

norbert_url = 'http://152.94.0.38'
digest_auth = HTTPDigestAuth('Default User', 'robotics')

payload = {'ctrl-state': 'motoroff'}
resp = session.post(norbert_url + "/rw/panel/ctrlstate?action=setctrlstate", auth=digest_auth, data=payload)
