'''
Created on May 17, 2020

@author: justin
'''
from _env_test import env
import asyncio
import unittest
# from unittest import IsolatedAsyncioTestCase
from db.base import get_async_session, session_manager
from sanic_testing import TestManager
from sanic_server import createApp


def get_app():
    app = createApp()
    return app


class TestSanicAuth(unittest.TestCase):

    def setUp(self) -> None:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(session_manager.create_tables_async(env))

    def test_create_user(self):
        username = "testUser"
        password = "12345"
        userData = {"username": username,
                    "password": password,
                    "email": "email@test.com",
                    "verified": True}

        app = get_app()
        _, response = app.test_client.post("auth/create_user", json=userData)
        self.assertTrue(response.json["ok"])

        _, response = app.test_client.post("auth/login", json=userData)
        self.assertTrue("access_token" in response.json)

        _, response = app.test_client.get("auth/login_check", cookies=response.cookies)
        self.assertTrue(response.status_code == 200)

        _, response = app.test_client.get("auth/login_check")
        self.assertTrue(response.status_code == 401)

    def testAuth(self):

        pass


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']

    unittest.main()
