import os
from aiohttp import web

from routes import setup_routes

HOST = os.getenv('HOST', '0.0.0.0')
PORT = int(os.getenv('PORT', "8080"))

async def shutdown_ (app):
    for ws in app['websockets']:
        await ws.close(message="The server is shutting down")

async def init ():
    app = web.Application()

    setup_routes(app)

    app.on_cleanup.append(shutdown_)
    app['websockets'] = []
    app['user_id'] = []
    return app

web.run_app(init(), host=HOST, port=PORT)