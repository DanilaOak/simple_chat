from aiohttp import web

from .views import routes


def setup_routes(app: web.Application) -> web.Application:
    app.add_routes(routes)
    return app
