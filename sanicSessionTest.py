import asyncio_redis
from sanic import Sanic
from sanic.response import text
from sanic_session import Session, RedisSessionInterface


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


redis = Redis()

app = Sanic(name="main")
Session(app, interface=RedisSessionInterface(redis.get_redis_pool))


@app.route("/")
async def test(request):
    # interact with the session like a normal dict
    if not request.ctx.session.get('foo'):
        request.ctx.session['foo'] = 0

    request.ctx.session['foo'] += 1

    response = text(request.ctx.session['foo'])

    return response

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4000, debug=True)
