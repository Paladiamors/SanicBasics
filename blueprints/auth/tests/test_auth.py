'''
Created on May 17, 2020

@author: justin
'''
import asyncio
import datetime
import unittest

from _env_test import env
from db.base import get_async_session, session_manager
from db.auth import User
from sanic_server import createApp
from utils.encrypt import EncryptJson
from sqlalchemy import select


def get_app():
    app = createApp()
    return app


class TestSanicAuth(unittest.TestCase):

    def setUp(self) -> None:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(session_manager.create_tables_async(env))

    def test_add_user(self):
        username = "testUser"
        password = "12345"
        userData = {"username": username,
                    "password": password,
                    "email": "email@test.com",
                    "verified": True}

        app = get_app()
        _, response = app.test_client.post("auth/add_user", json=userData)
        self.assertTrue(response.json["ok"])

        # test authentication fail
        _, response = app.test_client.post("auth/login", json={"email": "email@test.com", "password": "wrongPassword"})
        self.assertTrue("access_token" not in response.json)

        _, response = app.test_client.post("auth/login", json=userData)
        self.assertTrue("access_token" in response.json)

        _, response = app.test_client.get("auth/login_check", cookies=response.cookies)
        self.assertTrue(response.status_code == 200)

        _, response = app.test_client.get("auth/login_check")
        self.assertTrue(response.status_code == 401)

        # perform validation of email address
        e = EncryptJson()
        token = e.encrypt({"email": "email@test.com",
                           "expiry": (datetime.datetime.utcnow() + datetime.timedelta(1)).timestamp()})
        _, response = app.test_client.get("auth/verify_user", params={"token": token})
        self.assertTrue(response.json["ok"])

        async def get_user():
            async with get_async_session() as session:
                query = select(User).filter(User.username == username)
                resp = await session.execute(query)
                user = resp.scalar()
            self.assertTrue(user.verified)
        asyncio.run(get_user())


if __name__ == "__main__":
    unittest.main()
