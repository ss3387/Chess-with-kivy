import socketio


class ChessClient():
    def __init__(self, addr: str, update_board, name: str):
        self.name = name
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
                self.flip_board = msg['flip_board']
            elif msg['type'] == 'Game Info':
                self.turn = msg['turn']
                update_board(msg['unicodeboard'], msg['san'], msg['turn'], self.flip_board)
                self.white = msg['white']
                self.black = msg['black']
            elif msg['type'] == 'Board Update':
                update_board(msg['unicodeboard'], msg['san'], msg['turn'])
            elif msg['type'] == 'takeback_request':
                update_board(msg['unicodeboard'], msg['san'], msg['turn'], msg['type'])
            elif msg['type'] == 'game_over':
                update_board(None, None, None, None, msg['result'])


    def do_move(self, move):
        self.socketclient.send({'type': 'move','game_id': self.game_id,'move': move})
    
    def request_takeback(self, instance):
        self.socketclient.send({'type': 'undo', 'game_id': self.game_id, 'opponent': self.opponent_id})
    
    def accept_takeback(self, instance):
        self.socketclient.send({'type': 'undo_accepted', 'game_id': self.game_id})
    
    def resign(self, instance):
        self.socketclient.send({'type': 'close', 'game_id': self.game_id, 'player_name': self.name, 'opponent': self.opponent})
