import asyncio
import os

import aiohttp

HOST = os.getenv('HOST', 'localhost')
PORT = int(os.getenv('PORT', 5004))

URL = f'http://{HOST}:{PORT}/chat/wow1'


async def main():
    session = aiohttp.ClientSession(cookies={
        'AppCookie': 'f989736a44a4d91d84822fbf0f67984a766596fd057281a0964aed6214788af5'})
    async with session.ws_connect(URL) as ws:

        await prompt_and_send(ws)
        async for msg in ws:
            print('Message received from server:', msg)
            await prompt_and_send(ws)

            if msg.type in (aiohttp.WSMsgType.CLOSED,
                            aiohttp.WSMsgType.ERROR):
                break


async def prompt_and_send(ws):
    new_msg_to_send = input('Type a message to send to the server: ')
    if new_msg_to_send == 'exit':
        print('Exiting!')
        raise SystemExit(0)
    await ws.send_str(new_msg_to_send)


if __name__ == '__main__':
    print('Type "exit" to quit')
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
