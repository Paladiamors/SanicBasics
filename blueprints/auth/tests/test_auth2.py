'''
Created on May 17, 2020

@author: justin

This test is interesting but returns too many
noisy warnings. The method of starting a server
seems easier (however, this might be easier for debugging)
'''
import unittest

from db import get_session
from settingsManager import settingsManager
from utils.auth import deleteUser, userExists
from sanicServer import createApp
import time


# testing settings
settingsManager.loadSettings("settings_test.json")

class Test(unittest.TestCase):

    #     @unittest.skip("works")
    def testCreateUser(self):

        app = createApp()
        username = "testUser"
        password = "12345"
        userData = {"username": username, "password": password,
                    "email": "email@test.com", "isStaff": True,
                    "isActive": True, "verified": True}

        deleteUser(username)
        request, response = app.test_client.post("/auth/createUser", data=userData)
        dSession = get_session()
        self.assertTrue(userExists(username, dSession), "user exist")
        dSession.close()

#     @unittest.skip("not testing")
#     def testAuth(self):
# 
#         session = Session()
#         dSession = get_session()
#         username = "testUser"
#         password = "12345"
#         userData = {"username": username, "password": password,
#                     "email": "email@test.com", "isStaff": True,
#                     "isActive": True, "verified": True}
# 
#         deleteUser(username, dSession=dSession)
#         response = session.get(os.path.join(baseUrl, "auth/createUser"))
#         userData.update(response.json())
#         session.post(os.path.join(baseUrl, "auth/createUser"), data=userData)
# 
#         response = session.get(os.path.join(baseUrl, "auth/login"))
#         print(response)
#         session.close()


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
