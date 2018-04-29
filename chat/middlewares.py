import json

from aiohttp import web


@web.middleware
async def auth_middleware(request, handler):

    token = request.cookies.get('AppCookie')

    if not token:
        raise web.HTTPForbidden(body=json.dumps({'error': 'Access denied for requested resource'}),
                                content_type='application/json')

    user = request.app['redis'].get(token)

    if not user:
        raise web.HTTPForbidden(body=json.dumps({'error': 'Access denied for requested resource'}),
                                content_type='application/json')

    request.auth_user = json.loads(user)

    return await handler(request)