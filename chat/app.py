#! /usr/bin/env python
import asyncio
import aioredis

from aiohttp import web

from .utils import get_config
from .routes import setup_routes


async def close_redis(app):
    app['redis'].close()


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
    app.on_startup.append(init_redis)
    app.on_shutdown.append(close_redis)

    return app
