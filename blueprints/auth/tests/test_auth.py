###############################################################################
# Copyright (C) 2022, created on February 05, 2022
# Written by Justin Ho
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 3 as published by
# the Free Software Foundation.
#
# This source code is distributed in the hope that it will be useful and
# without warranty or implied warranty of merchantability or fitness for a
# particular purpose.
###############################################################################

import asyncio
import datetime
import unittest

from _env_test import env
from db.base import get_async_session, session_manager
from db.auth import User
from sqlalchemy import select
from sanic_server import createApp
from utils.encrypt import EncryptJson


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
                    "verified": False}
        server_kwargs = {"motd": False, "auto_reload": False}

        app = createApp()
        _, response = app.test_client.post("api/auth/add_user", json=userData, server_kwargs=server_kwargs, debug=True)
        self.assertTrue(response.json["ok"])

        # test authentication fail
        _, response = app.test_client.post(
            "api/auth/login", json={"email": "email@test.com", "password": "wrongPassword"}, server_kwargs=server_kwargs, debug=True)
        self.assertTrue("access_token" not in response.json)

        _, response = app.test_client.post("api/auth/login", json=userData, server_kwargs=server_kwargs, debug=True)
        self.assertTrue("access_token" in response.json)

        _, response = app.test_client.get("api/auth/login_check", cookies=response.cookies,
                                          server_kwargs=server_kwargs, debug=True)
        self.assertTrue(response.status_code == 200)

        _, response = app.test_client.get("api/auth/login_check", server_kwargs=server_kwargs, debug=True)
        self.assertTrue(response.status_code == 401)

        _, response = app.test_client.get("api/auth/logout", cookies=response.cookies,
                                          server_kwargs=server_kwargs, debug=True)
        self.assertTrue("access_token" not in response.cookies)
        self.assertTrue("access_token_signature" not in response.cookies)
        self.assertTrue(response.status_code == 200)

        # perform validation of email address
        e = EncryptJson()
        token = e.encrypt({"email": "email@test.com",
                           "expiry": (datetime.datetime.utcnow() + datetime.timedelta(1)).timestamp()})
        _, response = app.test_client.get(
            "api/auth/verify_user", params={"token": token}, server_kwargs=server_kwargs, debug=True)
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
