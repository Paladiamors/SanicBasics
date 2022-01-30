'''
Created on May 17, 2020

@author: justin
'''
import unittest

from db import get_session
from utils.auth import deleteUser, userExists
from utils.testing import SanicRequests


sanicRequests = SanicRequests()


class Test(unittest.TestCase):

    @unittest.skip("works")
    def testCreateUser(self):

        sanicRequests.newSession()
        dSession = get_session()
        username = "testUser"
        password = "12345"
        userData = {"username": username, "password": password,
                    "email": "email@test.com", "isStaff": True,
                    "isActive": True, "verified": True}

        deleteUser(username)
        response = sanicRequests.get("auth/createUser")
        userData.update(response.json())
        print(userData)
        sanicRequests.post("auth/createUser", data=userData)
        self.assertTrue(userExists(username, dSession), "user should exist")
        dSession.close()

#     @unittest.skip("not testing")
    def testAuth(self):

        sanicRequests.newSession()
        dSession = get_session()
        username = "testUser"
        password = "12345"
        userData = {"username": username, "password": password,
                    "email": "email@test.com", "isStaff": True,
                    "isActive": True, "verified": True}

        deleteUser(username, dSession=dSession)
        token = sanicRequests.get("forms/token").json()
        userData.update(token)
        sanicRequests.post("auth/createUser", data=userData)

        login = {"ident": "testUser", "password": "12345"}
        login.update(token)
        response = sanicRequests.post("auth/login", data=login)
        print("logged in", response.cookies.get("authenticated"))
        print("response", response.json())


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']

    unittest.main(exit=False)
    sanicRequests.kill()
