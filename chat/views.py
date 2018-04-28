import asyncio

from aiohttp import web, WSMsgType

routes = web.RouteTableDef()


@routes.get('/')
async def hello(request: web.Request) -> web.Response:
    return web.json_response({'message': 'Hello mfk'})


@routes.get('/chat/{channel}')
async def websocket_handler(request: web.Request):

    ws = web.WebSocketResponse()
    await ws.prepare(request)
    print('Create we WebSocket connection')
    channel = request.match_info.get('channel', 'main')

    request.app['chats'][channel].append(ws)
    redis = request.app['redis']
    messages = await redis.lrange(channel, 0, -1)
    if messages:
        for m in messages:
            await ws.send_str(m.decode('utf-8') + '/MFK')
    try:
        async for msg in ws:
            if msg.type == WSMsgType.TEXT:
                print(msg)
                if msg.data == 'close':
                    await ws.close()
                else:
                    await redis.rpush(channel, msg.data)
                    for w in request.app['chats'][channel]:
                        await w.send_str(msg.data + '/MFK')
            elif msg.type == WSMsgType.ERROR:
                print('ws connection closed with exception %s' %
                      ws.exception())

    finally:
        print('Connection closed')
        request.app['chats'][channel].remove(ws)

    return ws


async def read_subscription(ws, redis):
    # import ipdb; ipdb.set_trace()
    channel, = await redis.subscribe('wow')
    try:
        async for msg in channel.iter():
            # ipdb.set_trace()
            answer = msg.decode("utf-8")
            await ws.send_str(answer)
    finally:
        await redis.unsubscribe('wow')
