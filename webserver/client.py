import socketio

# standard Python
sio = socketio.Client()
mo = socketio.Client()


@sio.on('message')
def on_message(data):
    print(data)
# asyncio
sio.connect("http://0.0.0.0:8080")
sio.send({"type":"quickjoin","displayname":"mohammed"})

