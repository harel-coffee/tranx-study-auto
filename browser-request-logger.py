import logging
import os
import time

import requests

"""
RequestsLogger is an addon for mitmdump that logs information about request
and response pairs to server. As it does not do any changes to the body of the
request/response, I advise to run it with `--set stream_large_bodies=1`,
which enables streaming of the request/response body.
"""

class RequestsLogger:

    def __init__(self):
        self.s = requests.Session()
        self.user, self.task = self.read_current_user_task()

    def done(self):
        self.s.close()

    def read_current_user_task(self):
        path = '/vagrant/.user_study_current_status'
        if not os.path.exists(path):
            return None, None
        with open(path, "r", encoding='utf-8') as f:
            lines = f.readlines()
            userid = lines[0].strip()
            task = lines[1].strip()
        return userid, task

    """ 
    This hook function is called by `mitmdump` whenever a response is received from a target server.
    the flow object holds information about both request and response (the whole HTTP/s flow).
    """
    def response(self, flow):
        if flow.request.method == "GET" and flow.response.status_code == 200 and flow.response.headers:
            for k, v in flow.response.headers.items():
                if k.lower() == 'content-type' and 'text/html' in v.lower():
                    payload = {'url': flow.request.url,
                               'local_timestamp': int(time.time()),
                               'userid': self.user,
                               'task': self.task,
                                }
                    try:
                        res = self.s.post('http://moto.clab.cs.cmu.edu:8081/browser_log', json=payload, timeout=2.0)
                    except:
                        print('exception')
                    return

plugin = RequestsLogger()

addons = [
    plugin
]
