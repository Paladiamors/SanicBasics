'''
Created on May 17, 2020

@author: justin

something to manage the redisStore
between the request and session

request has the session data
response has the cookie data
'''
from settingsManager import settingsManager
from utils.redis import redis
import uuid
import ujson

configs = settingsManager.settings


class RedisStore:

    cookie_name = configs["REDIS_SESSION"]["cookie_name"]
    session_name = configs["REDIS_SESSION"]["session_name"]

    def __init__(self, request):
        """
        response is optional, maybe split this out
        maybe all use the same connetions?
        problems with async when doing that? Not sure
        """
        self.request = request
        self.connections = {}

    async def redis_write(self, key, value, expiry=-1, db=0):
        """
        writes a value into the redis cache
        """

        connection = await redis.get_redis_pool(db)
        value = ujson.dumps(value)
        await connection.setex(key, expiry, value)

    async def redis_read(self, key, db=0):
        """
        reads a value from the redis cache
        """

        connection = await redis.get_redis_pool(db)
        return ujson.loads(await connection.get(key))

    async def redis_delete(self, key, db=0):
        """
        deletes a value from the redis cache
        """
        connection = await redis.get_redis_pool(db)
        return ujson.loads(await connection.delete(key))

    async def csrf_add(self):
        """
        writes a csrf token into the database
        returns the token
        """

        token = uuid.uuid4().hex
        key = f"CSRF:{self.session_id}:{token}"
        await self.redis_write(key, True, 1800)
        return token

    async def csrf_ok(self, token):
        """
        validates the token
        """
        key = f"CSRF:{self.session_id}:{token}"
        result = await self.redis_write(key, True, 1800)
        return True if result else False

    @property
    def session_id(self):
        return self.request[self.session_name][self.cookie_name]

    @property
    def session(self):
        "returns the redis session"
        return self.request[self.session_name]
    
    @property
    def cookie(self):
        return self.request.cookie

    def set_cookie(self, key, value, maxage=None, expires=None, httponly=None,
                   samesite=None, domain=None, secure=None,
                   comment=None):
        """
        information based on https://sanic.readthedocs.io/en/latest/sanic/cookies.html

        key (string): they key to save the cookie at
        value (string): the value of the cookie
        expires (datetime): The time for the cookie to expire on the client’s browser.
        path (string): The subset of URLs to which this cookie applies. Defaults to /.
        comment (string): A comment (metadata).
        domain (string): Specifies the domain for which the cookie is valid. An explicitly specified domain must always start with a dot.
        max-age (number): Number of seconds the cookie should live for.
        secure (boolean): Specifies whether the cookie will only be sent via HTTPS.
        httponly (boolean): Specifies whether the cookie cannot be read by Javascript.
        """
        self.response.cookie[key] = value

        if maxage is not None:
            self.response.cookie[key]["max-age"] = maxage
        if httponly is not None:
            self.response.cookie[key]["httponly"] = httponly
        if domain is not None:
            self.response.cookie[key]["domain"] = domain
        if secure is not None:
            self.response.cookie[key]["secure"] = secure
        if comment is not None:
            self.response.cookie[key]["comment"] = comment
        if expires is not None:
            self.response.cookie[key]["expires"] = expires
        if samesite is not None:
            self.response.cookie[key]["samesite"] = samesite
