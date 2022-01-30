'''
Created on May 17, 2020

@author: justin
'''

import os
from settingsManager import get_settings
from subprocess import Popen
from utils.networking import get_port
import requests
import time
from urllib.parse import urljoin

settingsManager = get_settings("test")
base_path = settingsManager.base_path


def runSanicProcess():

    pythonExec = os.path.join(base_path, "pybin/bin/python3")
    runCommand = os.path.join(base_path, "runserver.py")
    port = str(get_port())

    proc = Popen([pythonExec, runCommand, "--port", port, "--settings", settings])
    return proc, port


class SanicRequests:

    def __init__(self, session=None, wait=0.5, settings="settings_test.json"):
        """
        launchers a server at local host for testing
        session: is a requests session
        wait: time in seconds to wait after kicking off the sanic process
        settings: the name of the settings file to load
        """

        base_path = settingsManager.base_path

        self.session = session or requests.Session()
        pythonExec = os.path.join(base_path, "pybin/bin/python3")
        runCommand = os.path.join(base_path, "runserver.py")
        self.port = str(get_port())
        self.proc = Popen([pythonExec, runCommand, "--port", self.port, "--settings", settings])
        self.baseUrl = f"http://localhost:{self.port}"
        time.sleep(wait)  # give the server some time to start up

    def localLink(self, url):
        return urljoin(self.baseUrl, url)

    def get(self, url, **kwargs):
        return self.session.get(self.localLink(url), **kwargs)

    def put(self, url, **kwargs):
        return self.session.put(self.localLink(url), **kwargs)

    def post(self, url, **kwargs):
        return self.session.post(self.localLink(url), **kwargs)

    def delete(self, url, **kwargs):
        return self.session.delete(self.localLink(url), **kwargs)

    def kill(self):
        """
        stops the sanic server
        """
        self.proc.kill()

    def newSession(self):
        self.session = requests.Session()


if __name__ == '__main__':

    proc, port = runSanicProcess()
    time.sleep(2)

    result = requests.get("http://localhost:9000/core/users")
    print(result.json())
    proc.kill()
    print("process complete")
