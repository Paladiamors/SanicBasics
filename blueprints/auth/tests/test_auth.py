'''
Created on May 17, 2020

@author: justin
'''
import asyncio
import datetime
import unittest

from _env_test import env
from db.base import session_manager
from sanic_server import createApp
from utils.encrypt import EncryptJson


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
        server_kwargs = {"motd": False}

        app = get_app()
        _, response = app.test_client.post("auth/add_user", json=userData, server_kwargs=server_kwargs)
        self.assertTrue(response.json["ok"])

        # test authentication fail
        _, response = app.test_client.post(
            "auth/login", json={"email": "email@test.com", "password": "wrongPassword"}, server_kwargs=server_kwargs)
        self.assertTrue("access_token" not in response.json)

        _, response = app.test_client.post("auth/login", json=userData, server_kwargs=server_kwargs)
        self.assertTrue("access_token" in response.json)

        _, response = app.test_client.get("auth/login_check", cookies=response.cookies,
                                          server_kwargs=server_kwargs)
        self.assertTrue(response.status_code == 200)

        _, response = app.test_client.get("auth/login_check", server_kwargs=server_kwargs)
        self.assertTrue(response.status_code == 401)

        _, response = app.test_client.get("auth/logout", cookies=response.cookies,
                                          server_kwargs=server_kwargs)
        self.assertTrue("access_token" not in response.cookies)
        self.assertTrue("access_token_signature" not in response.cookies)
        self.assertTrue(response.status_code == 200)

        # perform validation of email address
        e = EncryptJson()
        token = e.encrypt({"email": "email@test.com",
                           "expiry": (datetime.datetime.utcnow() + datetime.timedelta(1)).timestamp()})
        _, response = app.test_client.get(
            "auth/verify_user", params={"token": token}, server_kwargs=server_kwargs)
        self.assertTrue(response.json["ok"])

        # async def get_user():
        #     async with get_async_session() as session:
        #         query = select(User).filter(User.username == username)
        #         resp = await session.execute(query)
        #         user = resp.scalar()
        #     self.assertTrue(user.verified)
        # asyncio.run(get_user())


if __name__ == "__main__":
    unittest.main()
