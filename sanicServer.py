##################################################
# Author: Justin Ho
# Created: 2020-04-26
# Copyright (C) Justin Ho - All Rights Reserved
##################################################


from sanic import Sanic
from sanic_session import Session, RedisSessionInterface

from blueprints.core.views import bp as core
from blueprints.auth.views import bp as auth
from settingsManager import settingsManager
from utils.redis import redis


blueprints = [
    core,
    auth
]


config = settingsManager.settings
reload = settingsManager.getSetting("TESTING")


def createApp():
    app = Sanic(name="main")

    # setup sanic session
    Session(app, interface=RedisSessionInterface(redis.get_redis_pool_func(), **config["REDIS_SESSION"]))

    [app.blueprint(bp) for bp in blueprints]

    app.config.update(config)
    return app


def runServer(host=None, port=None, settings=None):

    if settings:
        settingsManager.loadSettings(settings)
    host = host or settingsManager.getSetting("HOST")
    port = port or settingsManager.getSetting("PORT")
    app = createApp()
    app.run(host=host, port=port, auto_reload=reload)


if __name__ == "__main__":

    runServer()
