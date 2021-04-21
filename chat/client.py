import os

import asyncio
import aiohttp
import logging
from aioconsole import ainput
import time

HOST = os.getenv('HOST', '0.0.0.0')
PORT = int(os.getenv('PORT', "8080"))
URL = f'http://{HOST}:{PORT}/ws'

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('client')

async def main():
    session = aiohttp.ClientSession()
    # To connect to a websocket server
    async with aiohttp.ClientSession() as session:
        async with session.ws_connect(URL) as ws:
            error, user_id = await init_chat (ws)
            if error:
                return
            #while True:

            get_msg_task = asyncio.create_task(recv_msg(ws, user_id))

            send_msg_task = asyncio.create_task(send_msg(ws))

            done, pending = await asyncio.wait([get_msg_task, send_msg_task], return_when=asyncio.FIRST_COMPLETED,)

            if not ws.closed:
                await ws.close()
            for task in pending:
                task.cancel()

async def init_chat(ws):
    user_id = input("Welcome to our group, if you want to continue type "
          "your id, otherwise type exit.\n")
    if user_id == 'exit':
        print('Exiting')
        raise SystemExit(0)

    await ws.send_str(user_id)
    msg = await ws.receive()
    print(msg.data)     # FIXME what if the server wants to close the connection
    error = 0
    if (msg.type) in (aiohttp.WSMsgType.CLOSE,
                      aiohttp.WSMsgType.ERROR):
        error = 1
    return (error, user_id)


async def send_msg(ws):
    while True:
        msg = await ainput('')
        if msg == 'exit':
            print('Exiting')
            #raise SystemExit(0)
            return
        await ws.send_str(msg)

async def recv_msg (ws, user_id):
    async for msg in ws:
        if msg.type == aiohttp.WSMsgType.TEXT:
            print(msg.data)
            #logger.info('> Message from server received: %s', msg.data())
            pass;
        else:
            break
        if (msg.type) in (aiohttp.WSMsgType.CLOSE,
                          aiohttp.WSMsgType.ERROR):
            #raise SystemExit(0)
            return
            #break

    """while True:
        #print('waiting')
        msg = await ws.receive()
        print(msg.data)
        """"""if msg.data.user == user_id:
            pass
        elif msg.data.user == "server":
            #print(msg.data)
            print('%s:  %s' % (msg.data.user, msg.data.msg)) # FIXME server msg should be alligned at the center
        else:
            #print(msg.data)
            print('%s:  %s' % (msg.data.user, msg.data.msg)) # logging should be improved
        """"""
        if (msg.type) in (aiohttp.WSMsgType.CLOSE,
                          aiohttp.WSMsgType.ERROR):
            raise SystemExit(0)
            break
        await asyncio.sleep(0.01)"""

if __name__ == '__main__':
    print('Type "exit" to quit')
    asyncio.run(main())

