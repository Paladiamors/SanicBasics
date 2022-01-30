###############################################################################
# Copyright (C) 2020, created on May 23, 2020
# Written by Justin Ho
#
# This source code is provided free of charge and without warranty.
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
###############################################################################

import unittest
from utils.auth import createUser, deleteUser, userExists
from db import get_session

env = "local"


class Test(unittest.TestCase):

    def testManageUser(self):

        dSession = get_session(env)
        username = "testUser"
        password = "12345"
        userData = {"username": username, "password": password,
                    "email": "email@test.com", "isStaff": True,
                    "isActive": True, "verified": True}

        deleteUser(username, dSession)
        createUser(userData, dSession)
        self.assertTrue(userExists(username, dSession), "this user should exist")
        deleteUser(username, dSession)
        self.assertFalse(userExists(username, dSession), "this user should not exist")


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
