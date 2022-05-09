import socketio

# standard Python
sio = socketio.Client()


@sio.on('message')
def on_message(data):
    print(data)

# asyncio
sio.connect("http://localhost:8080")
sio.send({"type":"quickjoin","displayname":"mohammedsss"})

