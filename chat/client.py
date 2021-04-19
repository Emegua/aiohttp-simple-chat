import os

import asyncio
import aiohttp

HOST = os.getenv('HOST', '0.0.0.0')
PORT = int(os.getenv('PORT', "8080"))
URL = f'http://{HOST}:{PORT}/ws'

async def main():
    session = aiohttp.ClientSession()
    # To connect to a websocket server
    async with session.ws_connect(URL) as ws:
        await p_send (ws)

        while True:
            msg = await ws.receive()
            print('Message received from server:', msg.data)
            await p_send(ws)
            if (msg.type) in (aiohttp.WSMsgType.CLOSE,
                              aiohttp.WSMsgType.ERROR):
                break


async def p_send(ws):
    msg = input('Type a message to send to the server: ')
    if msg == 'exit':
        print('Exiting')
        raise SystemExit(0)
    await ws.send_str(msg)

if __name__ == '__main__':
    print('Type "exit" to quit')
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

