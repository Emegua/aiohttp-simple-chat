import os

import asyncio
from aiohttp import web

import aioredis
import aiohttp_session
from aiohttp_session import redis_storage

from routes import setup_routes

HOST = os.getenv('HOST', '0.0.0.0')
PORT = int(os.getenv('PORT', "8080"))

async def shutdown_ (app):
    for ws in app['websockets']:
        await ws.close(message="The server is shutting down")

async def init ():
    # loop = asyncio.get_event_loop()
    app = web.Application()

    #redis = await aioredis.create_pool (('localhost', 6379)) # default redis configration sets port 6379
    #storage = redis_storage.RedisStorage(redis)
    #aiohttp_session.setup(app, storage)
    setup_routes(app)

    app.on_cleanup.append(shutdown_)
    app['websockets'] = []
    app['user_id'] = []
    return app

web.run_app(init(), host=HOST, port=PORT)