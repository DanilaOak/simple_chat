from aiohttp import web, WSMsgType

routes = web.RouteTableDef()


@routes.get('/')
async def hello(request: web.Request) -> web.Response:
    return web.json_response({'message': 'Hello mfk'})


@routes.get('/ws')
async def websocket_handler(request):

    ws = web.WebSocketResponse()
    await ws.prepare(request)

    task = request.app.loop.create_task(
        read_subscription(ws,
                          request.app['redis']))
    try:
        async for msg in ws:
            if msg.type == WSMsgType.TEXT:
                print(msg)
                if msg.data == 'close':
                    await ws.close()
                else:
                    await ws.send_str(msg.data + '/answer')
            elif msg.type == WSMsgType.ERROR:
                print('ws connection closed with exception %s' %
                      ws.exception())

    finally:
        task.close()
        print('websocket connection closed')

    return ws


async def read_subscription(ws, redis):
    channel, = await redis.subscribe('channel:1')
    try:
        async for msg in channel.iter():
            answer = process_message(msg)
            ws.send_str(answer)
    finally:
        await redis.unsubscribe('channel:1')


def process_message(msg):
    return msg