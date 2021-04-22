import os

import asyncio
import aiohttp
import logging
import json
from aioconsole import ainput

HOST = os.getenv('HOST', '0.0.0.0')
PORT = int(os.getenv('PORT', "8080"))
URL = f'http://{HOST}:{PORT}/'

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('client')

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

async def main():
    session = aiohttp.ClientSession()
    # To connect to a websocket server
    async with aiohttp.ClientSession() as session:
        async with session.ws_connect(URL) as ws:
            error, user_id = await init_chat (ws)
            if error:
                return

            get_msg_task = asyncio.create_task(recv_msg(ws, user_id))

            send_msg_task = asyncio.create_task(send_msg(ws))

            done, pending = await asyncio.wait([get_msg_task, send_msg_task], return_when=asyncio.FIRST_COMPLETED,)

            if not ws.closed:
                await ws.close()
            for task in pending:
                task.cancel()


async def init_chat(ws):
    print(f"{bcolors.OKBLUE}Welcome to our secret chat ".center(50, " "))
    print(f"{bcolors.OKBLUE}Feel free to talk about what you feel.".center(50, " "))
    print(f"{bcolors.OKBLUE}The data is not saved and you".center(50, " "))
    print(f"{bcolors.OKBLUE}can set yourname whatever you want. ".center(50, " "))
    print(f"{bcolors.OKBLUE}Hence, your privacy is kept!!\n".center(50, " "))
    print(f"{bcolors.OKCYAN}If you want to continue type your id, otherwise type exit.\n{bcolors.ENDC}".center(50, "#"))
    user_id = input("")
    if user_id == 'exit':
        print('Exiting')
        raise SystemExit(0)

    await ws.send_str(user_id)
    msg = await ws.receive()
    # print(msg.data.center(50, " "))     # FIXME what if the server wants to close the connection
    print(f"{bcolors.OKCYAN}%s{bcolors.ENDC}".center(40, ' ') % msg.data)

    error = 0
    if msg.type in (aiohttp.WSMsgType.CLOSE, aiohttp.WSMsgType.ERROR):
        error = 1
    return error, user_id


async def send_msg(ws):
    while True:
        msg = await ainput('')
        if msg == 'exit':
            print('Exiting')
            return
        await ws.send_str(msg)


async def recv_msg(ws, user_id):
    async for msg in ws:
        if msg.type == aiohttp.WSMsgType.TEXT:
            js = json.loads(msg.data)
            # print(js["user"])
            if js["user"] == "0":
                # server
                #print(js["msg"].center(50, " "))
                print(f"{bcolors.OKCYAN}%s{bcolors.ENDC}".center(40, ' ') % js["msg"])
            else: # from another client
                #print(js["msg"].rjust(50, " "))
                print(f"{bcolors.OKGREEN}%s: {bcolors.OKBLUE}%s {bcolors.ENDC}".rjust(30, ' ') % (js["user"], js["msg"]))

        if (msg.type) in (aiohttp.WSMsgType.CLOSE,
                          aiohttp.WSMsgType.ERROR):
            return

if __name__ == '__main__':
    print('Type "exit" to quit')
    asyncio.run(main())

