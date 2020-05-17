'''
Created on May 17, 2020

@author: justin
'''


import asyncio
import ujson
import asyncio_redis


@asyncio.coroutine
def example():
    # Create Redis connection
    connection = yield from asyncio_redis.Connection.create(host='127.0.0.1', port=6379, db=1)

    # Set a key
    yield from connection.set('my_key', 'my_value')

    # When finished, close the connection.
    connection.close()


async def example2():
    # Create Redis connection
#     connection = await asyncio_redis.Connection.create(host='127.0.0.1', port=6379, db=1)
    pool = await asyncio_redis.Pool.create(host='127.0.0.1', port=6379, db=1, poolsize=10)

    # Set a key
    await pool.setex('CSRF:SOME_ID:blahblahblah3', 60, ujson.dumps({"something": True}))

    # When finished, close the connection.
    pool.close()

async def example3():
    # Create Redis connection
#     connection = await asyncio_redis.Connection.create(host='127.0.0.1', port=6379, db=1)
    pool = await asyncio_redis.Pool.create(host='127.0.0.1', port=6379, db=1, poolsize=10)

    # Set a key
    value = await pool.get('CSRF:SOME_ID:blahblahblah4')
    print(value)

    # When finished, close the connection.
    pool.close()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(example2())
