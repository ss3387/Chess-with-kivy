import socketio
import time


class ChessClient:
    def __init__(self,addr) -> None:
        self.socketclient = socketio.Client()
        self.socketclient.connect(addr)
        self.socketclient.send({"type":"quickjoin","displayname":"mohammed"})

        @self.socketclient.on('message')
        def on_message(msg):
            if msg["type"] == "Game started":
                self.game_id = msg["game_id"]
                self.player_id = msg["player_id"]
                self.opponent = msg["opponent"]
            elif msg["type"] == "Game Info":
                self.turn = msg["turn"]
                self.unicodeboard = msg["unicodeboard"]
                self.white = msg["white"]
                self.black = msg["black"]
            else:
                print(msg)


    def do_move(self,move):
        self.socketclient.send({"type":"move","game_id":self.game_id,"move":move})


x = ChessClient(addr="http://localhost:8080")
input("wait...")
print(x.turn)
print(x.opponent)
print(x.unicodeboard)
print(x.player_id)
while True:

   move = input("enter move")
   x.do_move(move)