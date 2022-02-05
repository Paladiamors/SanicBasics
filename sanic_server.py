###############################################################################
# Copyright (C) 2022, created on January 31, 2022
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

from sqlalchemy import select
from sanic import Sanic
from sanic_jwt import Initialize, exceptions
from db.base import get_async_session
from db.auth import User
from blueprints.core.views import bp as core
from blueprints.auth.views import bp as auth
from settingsManager import get_settings
from utils.forms import parse_body


settingsManager = get_settings()
blueprints = [
    core,
    auth
]


async def authenticate(request):
    data = parse_body(request)
    if "email" and "password" in data:
        async with get_async_session() as session:
            resp = await User.authenticate(session, data["email"], data["password"])
        if resp["ok"]:
            return {"user_id": resp["uid"]}
        else:
            raise exceptions.AuthenticationFailed("Invalid credentials")


async def extend_payload(payload):

    uid = payload.get("user_id")
    query = select(User.username).where(User.id == uid)
    async with get_async_session() as session:
        async with session.begin():
            cursor = await session.execute(query)
            username = cursor.scalar()
    payload.update({"username": username})
    return payload


def createApp():

    app = Sanic(name="main")
    config = settingsManager.get_setting("sanic/config", {})
    app.config.update(config)

    Initialize(app,
               authenticate=authenticate,
               cookie_split=True,
               cookie_set=True,
               url_prefix="auth",
               extend_payload=extend_payload,
               path_to_authenticate="/login",
               path_to_retrieve_user="/user",
               path_to_verify="/verify",
               path_to_refresh="/refresh")
    [app.blueprint(bp) for bp in blueprints]
    return app


def runServer(**kwargs):

    settings = settingsManager.get_setting("sanic/run")
    settings.update(kwargs)

    app = createApp()
    app.run(**settings)


if __name__ == "__main__":

    runServer(auto_reload=True)
