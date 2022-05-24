from flask import Flask , request
from flask_socketio import SocketIO, send, emit
from flask_socketio import join_room, leave_room
import os
import uuid
import chess


app = Flask(__name__)
app.secret_key = os.urandom(24)
socketio = SocketIO(app, manage_session=False)


class GameData: 
    def __init__(self): 
        self.opengames = []
        self.playinggames = {}

    def init_game(self, displayname, player_id, play_game): 

        game_id = play_game['game_id']
        player1 = play_game['player_id']
        player2 = player_id
        player1displayname = play_game['display_name']
        player2displayname = displayname

        # Send opponents to individual clients
        data = {
            'type': 'Game started', 
            'opponent': player2displayname, 
            'game_id': game_id, 
            'player_id': player1,
            'opponent_id': player2
        }
        send(data, room=player1)

        data = {
            'type': 'Game started', 
            'opponent': player1displayname, 
            'game_id': game_id, 
            'player_id': player2,
            'opponent_id': player1,
            'flip_board': True
        }
        send(data, room=player2)


        gameobject = {
            'status': 'RUNNING', 
            'player1': player1, 
            'player2': player2, 
            'player_ids': [player1, player2], 
            'player1name': player1displayname, 
            'player2name': player2displayname, 
            'display_names': [player1displayname, player2displayname], 
            'game': {
                'board': chess.Board(), 
                'white': player1, 
                'black': player2,

            }

        }
        self.playinggames[game_id] = gameobject

        # Join clients to room so we can broadcast it easily
        join_room(game_id, player1)
        join_room(game_id, player2)

        turn = gameobject['game']['board'].turn
        if turn == chess.WHITE: 
            
            turn = 'white'
        else: 
            turn = 'black'

        data = {
            'type': 'Game Info', 
            'turn': turn, 
            'unicodeboard': gameobject['game']['board'].unicode(), 
            'san': None,
            'white': player1, 
            'black': player2, 
        }

        send(data, room=game_id)


    def init_new_game(self, displayname, player_id): 
        game_id = str(uuid.uuid4().fields[-1])[: 5]

        gameobject = {
            'player_id': player_id, 
            'display_name': displayname, 
            'game_id': game_id
        }
        self.opengames.append(gameobject)
        # change to player l8r



    def add_move(self, game_id, player_id, move): 

        game = self.playinggames[game_id]

        if player_id not in game['player_ids']: 
            send({'type': 'fail', 'message': 'Wrong game'}, room=player_id)
            return

        turn = game['game']['board'].turn
        if turn == chess.WHITE: 
            turn = 'white'
        else: 
            turn = 'black'
        
        if game['game'][turn] != player_id: 
            return

        try: 
            if chess.Move.from_uci(move) in game['game']['board'].legal_moves: 
                move_san = game['game']['board'].san(chess.Move.from_uci(move))
                print(move_san)
                game['game']['board'].push_uci(move)
            else: 
                send({'type': 'fail', 'message': 'Wrong Move'}, room=player_id)
                return
        except: 
            send({'type': 'fail', 'message': 'Wrong Move'}, room=player_id)
            return
    
        turn = game['game']['board'].turn
        if turn == chess.WHITE: 
            turn = 'white'
        else: 
            turn = 'black'
        
        boardupdate = {
            'type': 'Board Update', 
            'unicodeboard': game['game']['board'].unicode(), 
            'turn': turn, 
            'san': move_san
        }
        send(boardupdate, room=game_id)

        if game['game']['board'].is_game_over():
            result_phrases = {
                '1-0': 'White wins!',
                '0-1': 'Black wins!',
                '1/2-1/2': 'It\'s a draw!'
            }
            send({'type': 'game_over', 'result': result_phrases[game['game']['board'].result()]}, room=game_id)

e = GameData()


@socketio.on('message')
def handleMessage(msg):
    if msg['type'] == 'quickjoin':
        if len(e.opengames) == 0:
            e.init_new_game(msg['displayname'], request.sid)
            send({'type':'wait', 'message':'awaiting join'})
            
        else:
            game = e.opengames.pop()
            e.init_game(msg['displayname'], request.sid, game)
            
    elif msg['type'] == 'move':
        e.add_move(msg['game_id'], request.sid, msg['move'])
    elif msg['type'] == 'undo':
        send({'type': 'takeback_request', 'unicodeboard': None, 'san': None, 'turn': None}, room=msg['opponent_id'])
    elif msg['type'] == 'undo_accepted':
        e.playinggames[msg['game_id']]['board'].pop()
        turn = game['game']['board'].turn
        if turn == chess.WHITE: 
            turn = 'white'
        else: 
            turn = 'black'
        boardupdate = {
            'type': 'Board Update', 
            'unicodeboard': e.playinggames[msg['game_id']]['board'].unicode(), 
            'turn': turn, 
            'san': 'undo'
        }
        send(boardupdate, room=msg['game_id'])
    if msg['type'] == 'close':
        send()
        socketio.close_room(msg['game_id'])

@socketio.on('connect')
def handleConnection(): 
  send({
    'type': 'Connected', 
    'message': 'Successfuly connected to server'}, )

socketio.run(app, host='0.0.0.0' , port=8080, debug = True)