import os

import asyncio
from aiohttp import web

from routes import setup_routes
# from settings import config

HOST = os.getenv('HOST', '0.0.0.0')
PORT = int(os.getenv('PORT', "8080"))

# loop = asyncio.get_event_loop()
app = web.Application()
setup_routes(app)
web.run_app(app, host=HOST, port=PORT)