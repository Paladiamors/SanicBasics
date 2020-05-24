'''
Created on May 17, 2020

@author: justin
'''

import os
from settingsManager import settingsManager
from subprocess import Popen
from utils.networking import get_port
import requests
import time

settings = "settings_test.json"
settingsManager.loadSettings(settings)
basePath = settingsManager.basePath


def runSanicProcess():

    pythonExec = os.path.join(basePath, "pybin/bin/python3")
    runCommand = os.path.join(basePath, "runserver.py")
    port = str(get_port())

    proc = Popen([pythonExec, runCommand, "--port", port, "--settings", settings])
    return proc, port


if __name__ == '__main__':

    proc, port = runSanicProcess()
    time.sleep(2)

    result = requests.get("http://localhost:9000/api/core/users")
    print(result.json())
    proc.kill()
    print("process complete")
