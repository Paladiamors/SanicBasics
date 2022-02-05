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

from db.auth import User
from db.base import get_async_session


async def create_user():

    username = "testUser"
    password = "12345"
    user_data = {"username": username,
                 "password": password,
                 "email": "email@test.com",
                 "verified": True}

    async with get_async_session() as session:
        await User.add_user(session, user_data)
