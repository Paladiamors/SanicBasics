'''
Created on May 17, 2020

@author: justin
'''
import os
import time
import unittest

from requests import Session

from db import getSession
from settingsManager import settingsManager
from utils.auth import deleteUser, userExists
from utils.testing import runSanicProcess


# testing settings
settingsManager.loadSettings("settings_test.json")

proc, port = runSanicProcess()
time.sleep(0.5)

baseUrl = f"http://localhost:{port}"


class Test(unittest.TestCase):

    def testCreateUser(self):

        session = Session()
        dSession = getSession()
        username = "testUser"
        password = "12345"
        userData = {"username": username, "password": password,
                    "email": "email@test.com", "isStaff": True,
                    "isActive": True, "verified": True}

        print("deleting user")
        deleteUser(username, dSession=dSession)
        print("making post")
        result = session.post(os.path.join(baseUrl, "api/auth/createUser"), data=userData)
        print(result.json())
        self.assertTrue(userExists(username, dSession), "user exist")
        dSession.close()

    @unittest.skip("not testing")
    def testAuth(self):

        session = Session()
        response = session.get(os.path.join(baseUrl, "api/auth/login"))
        print(response)
        session.close()


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main(exit=False)
    print("after unittest")
    proc.kill()
