import asyncio
import os

import aiohttp

HOST = os.getenv('HOST', 'localhost')
PORT = int(os.getenv('PORT', 5004))

URL = f'http://{HOST}:{PORT}/chat/wow1'


async def main():
    session = aiohttp.ClientSession(cookies={
        'AppCookie': '728dc6a3a288fe2c32b7d241364c287cdab983b3f33c8c330fc959010011ac68'})
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
