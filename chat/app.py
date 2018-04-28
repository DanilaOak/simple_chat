#! /usr/bin/env python
import asyncio
import aioredis
from collections import defaultdict

from aiohttp import web, WSCloseCode

from .utils import get_config
from .routes import setup_routes


async def on_shutdown(app):
    for ws in app['websockets']:
        await ws.close(code=WSCloseCode.GOING_AWAY,
                       message='Server shutdown')


async def close_redis(app):
    app['redis'].close()
    print('Redis closed')


async def init_redis(app):
    print('init redis')
    app['redis'] = await aioredis.create_redis(('localhost', 6379), loop=app.loop)



def create_app(config=None) -> web.Application:

    if not config:
        config = get_config()

    loop = asyncio.get_event_loop()
    app = web.Application(loop=loop)
    setup_routes(app)
    app['config'] = config
    app['chats'] = defaultdict(list)
    app.on_startup.append(init_redis)
    app.on_shutdown.append(close_redis)

    return app
