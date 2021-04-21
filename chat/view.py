# aiohttpdemo_polls/views.py
from aiohttp import web, WSMsgType
# to store user specific data
import aiohttp_session
async def index(request):
    print('SECRET CHAT READY')
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    # In the client side, print "Welcome to our group, if you want to continue type
    # your id, otherwise type exit."

    msg = await ws.receive() # recv user id or exit
    if msg.type in (WSMsgType.CLOSE,WSMsgType.ERROR): # if xlients wants to quit
        await ws.close()
        return ws
    user_id = msg.data

    #  user user_id has joined the chat, announce this to other members
    # announcement = ('%s has joined the chat. Welcome!' % user_id)
    announcement = {"user": "0", "msg": '%s has joined the chat. Welcome!' % user_id}
    # announcement = ('%s has joined the chat. Welcome!' % user_id)
    for client_socket in request.app['websockets']:
        # await client_socket.send_str(announcement)
        await client_socket.send_json(announcement)

    request.app['websockets'].append(ws) # add to the grouo (only 1 group currently is what we have
    request.app['user_id'].append(user_id) # FIXME - what if there are users with similar user_id??

    await ws.send_str('Welcome to the SECRET CHAT %s!' % user_id)

    while True:
        msg = await ws.receive()
        if msg.type == WSMsgType.TEXT:
            # print(msg.data)
            if msg.data == 'exit':
                #await ws.close()
                break
            else:
                for client_socket in request.app['websockets']:
                    if client_socket != ws:
                        await client_socket.send_json({"user": user_id, "msg": "%s" % (msg.data)})
                        # await client_socket.send_str('%s: %s' % (user_id, msg.data))    # FIXME send json instead of str

        if msg.type in (WSMsgType.CLOSE,
                          WSMsgType.ERROR):
            break # FIXME if it is error handle it elegantly
    # await ws.close()
    request.app['websockets'].remove(ws)
    announcement = {"user": "0", "msg": ('%s left the chat' % user_id)}
    for client_socket in request.app['websockets']:
        await client_socket.send_json(announcement)
    return ws