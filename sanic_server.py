##################################################
# Author: Justin Ho
# Created: 2020-04-26
# Copyright (C) Justin Ho - All Rights Reserved
##################################################


import os
from sanic import Sanic
from sanic_session import Session, RedisSessionInterface

from blueprints.core.views import bp as core
from blueprints.auth.views import bp as auth
from sanic_config import get_configs
from utils.redis import redis
from utils.networking import get_port
from subprocess import Popen


blueprints = [
    core,
    auth
]

config = get_configs()


def create_app():
    app = Sanic(name="main")

    # setup sanic session
    Session(app, interface=RedisSessionInterface(redis.get_redis_pool_func(), **config["REDIS_SESSION"]))

    [app.blueprint(bp) for bp in blueprints]

    app.config.update(config)
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=8081, auto_reload=True)
