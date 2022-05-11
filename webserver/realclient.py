import socketio
import time


class ChessClient:
    def __init__(self, addr, update_board):
        self.socketclient = socketio.Client()
        self.socketclient.connect(addr)
        self.socketclient.send({'type':'quickjoin','displayname':'mohammed'})

        @self.socketclient.on('message')
        def on_message(msg):
            if msg['type'] == 'Game started':
                self.game_id = msg['game_id']
                self.player_id = msg['player_id']
                self.opponent = msg['opponent']
            elif msg['type'] == 'Game Info':
                self.turn = msg['turn']
                update_board(msg['unicodeboard'])
                self.white = msg['white']
                self.black = msg['black']
            elif msg['type'] == 'Board Update':
                update_board(msg['unicodeboard'])
            else:
                print(msg)

    def do_move(self,move):
        self.socketclient.send({'type':'move','game_id':self.game_id,'move':move})

