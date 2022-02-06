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
from db.base import session_manager
from sanic_server import createApp
from db.tests.utils import create_user


class Test(unittest.TestCase):

    def setUp(self) -> None:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(session_manager.create_tables_async(env))
        loop.run_until_complete(create_user())

    def test_add_record(self):
        server_kwargs = {"motd": False}
        username = "testUser"
        password = "12345"
        userData = {"username": username,
                    "password": password,
                    "email": "email@test.com",
                    "verified": True}
        app = createApp()
        _, response = app.test_client.post("auth/login", json=userData, server_kwargs=server_kwargs)
        cookies = response.cookies

        _, response = app.test_client.post(
            "expenses/add_record", json={"cost": 100, "description": "test"}, cookies=cookies, server_kwargs=server_kwargs)
        self.assertTrue(response.json["ok"])

        _, response = app.test_client.post(
            "expenses/add_record", json={"cost": 101, "description": "test"}, cookies=cookies, server_kwargs=server_kwargs)
        self.assertTrue(response.json["ok"])

        _, response = app.test_client.get("expenses/get_records", cookies=cookies, server_kwargs=server_kwargs)
        expected_response = [{'id': 1,
                              'date': datetime.date.today().isoformat(),
                              'type': None,
                              'description': 'test',
                              'cost': 100.0,
                              'comment': None},
                             {'id': 2,
                              'date': datetime.date.today().isoformat(),
                              'type': None,
                              'description': 'test',
                              'cost': 101.0,
                              'comment': None}]
        self.assertEqual(response.json, expected_response)


if __name__ == "__main__":
    unittest.main()
