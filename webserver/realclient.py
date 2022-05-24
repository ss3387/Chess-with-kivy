import socketio


class ChessClient():
    def __init__(self, addr: str, update_board, name: str):
        self.socketclient = socketio.Client()
        self.socketclient.connect(addr)
        self.socketclient.send({'type': 'quickjoin','displayname': self.name})
        

        @self.socketclient.on('message')
        def on_message(msg: dict):
            if msg['type'] == 'Game started':
                self.game_id = msg['game_id']
                self.player_id = msg['player_id']
                self.opponent = msg['opponent']
                self.opponent_id = msg['opponent_id']
            elif msg['type'] == 'Game Info':
                self.turn = msg['turn']
                update_board(msg['unicodeboard'], msg['san'], msg['turn'])
                self.white = msg['white']
                self.black = msg['black']
            elif msg['type'] == 'Board Update':
                update_board(msg['unicodeboard'], msg['san'], msg['turn'])
            else:
                print(msg)
                try:
                    update_board(msg['unicodeboard'], msg['san'], msg['turn'])
                except:
                    pass


    def do_move(self, move):
        self.socketclient.send({'type': 'move','game_id': self.game_id,'move': move})
    
    def request_takeback(self):
        self.socketclient.send({'type': 'undo', 'game_id': self.game_id, 'opponent': self.opponent_id})
