import asyncio
import os

import aiohttp

HOST = os.getenv('HOST', 'localhost')
PORT = int(os.getenv('PORT', 5004))

URL = f'http://{HOST}:{PORT}/chat/wow1'


async def main():
    session = aiohttp.ClientSession(cookies={
        'AppCookie': '70095f6c33c83812643b4d9392066dd263fe884bd86714e27cf1c798638a078d'})
    async with session.ws_connect(URL) as ws:
        print('Start to consume')
        async for msg in ws:
            print('Message received from server:', msg)

            if msg.type in (aiohttp.WSMsgType.CLOSED,
                            aiohttp.WSMsgType.ERROR):
                break


if __name__ == '__main__':
    print('Type "exit" to quit')
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
