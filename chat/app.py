#! /usr/bin/env python
import asyncio

from aiohttp import web

from .utils import get_config


def create_app(config=None) -> web.Application:

    if not config:
        config = get_config()

    loop = asyncio.get_event_loop()
    app = web.Application(loop=loop)
    app['config'] = config

    return app
