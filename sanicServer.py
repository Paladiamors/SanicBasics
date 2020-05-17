##################################################
# Author: Justin Ho
# Created: 2020-04-26
# Copyright (C) Justin Ho - All Rights Reserved
##################################################

import asyncio_redis
from sanic import Sanic
from sanic_session import Session, RedisSessionInterface

from blueprints.core.views import bp as core
from blueprints.auth.views import bp as auth
from blueprints.forms.views import bp as forms
from settingsManager import settingsManager
from utils.redis import redis


class Redis:
    """
    A simple wrapper class that allows you to share a connection
    pool across your application.
    """
    _pool = None

    async def get_redis_pool(self):
        if not self._pool:
            self._pool = await asyncio_redis.Pool.create(
                host='0.0.0.0', port=6379, poolsize=10
            )

        return self._pool


blueprints = [
    core,
    auth,
    forms
]


def createApp():

    app = Sanic(name="main")
    config = settingsManager.getSetting("REDIS_SESSION")

    Session(app, interface=RedisSessionInterface(redis.get_redis_pool_func(), **config))

    [app.blueprint(bp) for bp in blueprints]

    app.config.update(settingsManager.settings)
    return app


def runServer(host=None, port=None, settings=None, auto_reload=None):

    if settings:
        settingsManager.loadSettings(settings)
    # auto_reload = auto_reload if auto_reload is not None else settingsManager.getSetting("TESTING")
    host = host or settingsManager.getSetting("HOST")
    port = port or settingsManager.getSetting("PORT")
    app = createApp()
    app.run(host=host, port=port, auto_reload=auto_reload)


if __name__ == "__main__":

    runServer(auto_reload=True)
    print("at the end")
