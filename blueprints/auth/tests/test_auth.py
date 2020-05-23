'''
Created on May 17, 2020

@author: justin
'''
import os
import time
import unittest

from requests import Session

from db.base import memorySession
from utils.testing import runSanicProcess

proc, port = runSanicProcess()
time.sleep(0.5)

baseUrl = f"http://localhost:{port}"


class Test(unittest.TestCase):

    def setUp(self):
        self.session = memorySession()

    def tearDown(self):
        pass

    def testCreateUser(self):

        session = Session()
        json = {"username": ["test"]}
        session.post(os.path.join(baseUrl, "api/auth/createUser"), data=json)
        session.close()

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
