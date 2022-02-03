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


def createApp():

    app = Sanic(name="main")
    Initialize(app,
               authenticate=authenticate,
               cookie_split=True,
               cookie_set=True,
               url_prefix="auth",
               path_to_authenticate="/login",
               path_to_retrieve_user="/user",
               path_to_verify="/verify",
               path_to_refresh="/refresh",
               )
    [app.blueprint(bp) for bp in blueprints]
    app.config.update(settingsManager.settings)
    return app


def runServer(host=None, port=None, auto_reload=None, motd=False):

    # auto_reload = auto_reload if auto_reload is not None else settingsManager.get_setting("TESTING")
    host = host or settingsManager.get_setting("HOST")
    port = port or settingsManager.get_setting("PORT")
    app = createApp()
    app.run(host=host, port=port, auto_reload=auto_reload, motd=motd)


if __name__ == "__main__":

    runServer(auto_reload=True)
