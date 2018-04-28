import asyncio
import os

import aiohttp

HOST = os.getenv('HOST', 'localhost')
PORT = int(os.getenv('PORT', 5000))

URL = f'http://{HOST}:{PORT}/chat/wow'


async def main():
    session = aiohttp.ClientSession()
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
