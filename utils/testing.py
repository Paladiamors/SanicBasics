'''
Created on May 17, 2020

@author: justin
'''

import os
from sanic_config import base_path
from subprocess import Popen
from utils.networking import get_port
import requests
import time


def runSanicProcess():
    
    pythonExec = os.path.join(base_path, "pybin/bin/python3")
    runCommand = os.path.join(base_path, "runserver.py")
    port = str(get_port())

    proc = Popen([pythonExec, runCommand, "--port", port])
    return proc, port


if __name__ == '__main__':
    

    proc, port = runSanicProcess()
    time.sleep(2)
    
    result = requests.get("http://localhost:9000/api/core/users")
    print(result.json())
    proc.kill()
    print("process complete")
    