# aiohttpdemo_polls/views.py
from aiohttp import web, WSMsgType

async def index(request):
    print('Websocket connection starting')
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    print('web socket connection ready.')

    while True:
        msg = await ws.receive()
        print(msg.data)
        if msg.type == WSMsgType.TEXT:
            print(msg.data)
            if msg.data == 'exit':
                print('gonna exit')
                await ws.close()
                break
            else:
                await ws.send_str(msg.data + '/answer')
        if (msg.type) in (WSMsgType.CLOSE,
                          WSMsgType.ERROR):
            break;
    await ws.close()
    print('Websocket connection closed')
    return ws