# aiohttpdemo_polls/views.py
from aiohttp import web, WSMsgType
# to store user specific data
import aiohttp_session
async def index(request):
    print('Websocket connection starting')
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    print('web socket connection ready.')
    # In the client side, print "Welcome to our group, if you want to continue type
    # your id, otherwise type exit."

    msg = await ws.receive()
    if msg.type in (WSMsgType.CLOSE,WSMsgType.ERROR):
        print("exiiii")
        await ws.close()
        return ws
    user_id = msg.data
    print(user_id)
    print("connection begin")
    #  user user_id has joined the chat, announce this to other members
    # announcement = ('%s has joined the chat. Welcome!' % user_id)
    announcement = ('%s has joined the chat. Welcome!' % user_id)
    for client_socket in request.app['websockets']:
        await client_socket.send_str(announcement)
        # await client_socket.send_json(announcement)

    request.app['websockets'].append(ws)
    request.app['user_id'].append(user_id) # FIXME - what is there are users with similar user_id??

    await ws.send_str('Welcome to the chat %s' % user_id)

    while True:
        msg = await ws.receive()
        print(msg.data)
        if msg.type == WSMsgType.TEXT:
            # print(msg.data)
            if msg.data == 'exit':
                print('gonna exit')
                #await ws.close()
                break
            else:
                for client_socket in request.app['websockets']:
                    if client_socket != ws:
                        # await client_socket.send_json('{"user": "%s", "msg": "%s"}' % (user_id, msg.data))
                        await client_socket.send_str('%s: %s' % (user_id, msg.data))    # FIXME send json instead of str

        if msg.type in (WSMsgType.CLOSE,
                          WSMsgType.ERROR):
            break; # FIXME if it is error handle it elegantly
    print("gonn")
    # await ws.close()
    request.app['websockets'].remove(ws)
    announcement = ('%s left the chat' % user_id)
    for client_socket in request.app['websockets']:
        await client_socket.send_str(announcement)


    # print('Websocket connection closed')
    return ws