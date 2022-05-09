from flask import Flask ,request
from flask_socketio import SocketIO, send, emit
from flask_socketio import join_room, leave_room
from flask_session import Session

import os
import uuid

import chess


app = Flask(__name__)
app.secret_key = os.urandom(24)
Session(app)
socketio = SocketIO(app, manage_session=False)


class GameData:
    def __init__(self):
        self.opengames = []
        self.playinggames = {}

    def init_game(self,displayname,game_id,play_game):

        player_id = str(uuid.uuid4().fields[-1])[:5]
        game_id = play_game["game_id"]
        print(play_game)


        gameobject = {
            "status":"RUNNING",
            "player_ids": [play_game["player_id"],player_id],
            "display_names": [play_game["display_name"],displayname],
            ## Only for displaying move to spectator
            "movelist": [],
            "board": chess.Board(),

        }
        self.playinggames[game_id] = gameobject

        
        return gameobject

    def init_new_game(self,displayname,player_id):
        game_id = str(uuid.uuid4().fields[-1])[:5]

        gameobject = {
            "player_id": player_id,
            "display_name":displayname,
            "game_id":game_id
        }
        self.opengames.append(gameobject)
        ## change to player l8r

    def get_playing_games(self):
        f = self.playinggames
        e = self.playinggames
        print(f)
        d = {}
        for x in f:
            print(x)
            del f[x]["board"]
            d[x] = f[x]
        self.playinggames = e
        return d

    def get_open_games(self):
        return self.opengames

    def add_move(self,game_id,move):
        game = self.playinggames[game_id]


        if chess.Move.from_uci(move) in self.board.legal_moves:
            game.movelist.append(move)
            game.board.push_uci(move)
            self.broadcast_update(game_id)

        elif move == 'e1h1' or move == 'e8h8':
            game.movelist.append(move)
            game.board.push_san(move)
            self.broadcast_update(game_id)
        

    def broadcast_update(self,game_id):
        game = self.playinggames[game_id]

        if game.board.is_checkmate() == True:
            socketio.emit('Game Over', "Check Mate", room=game_id)
            
        elif game.board.is_check() == True:
            socketio.emit('Game Over', "Check Mate", room=game_id)
            
        elif game.board.is_game_over() == True:
            socketio.emit('Game Over', "Unknown Reason", room=game_id)
        else:
            socketio.emit('Move', game.movelist[-1], room=game_id)
            socketio.emit('Legal Moves', game.board.legal_moves, room=game_id)




e = GameData()


@app.route("/playinggames")
def games():
    return e.get_playing_games()

@app.route("/opengames")
def adwdw():
    return e.get_open_games()

@socketio.on('message')
def handleMessage(msg):
    if msg["type"] == "quickjoin":
        displayname = msg["displayname"]
        if len(e.opengames) == 0:
            e.init_new_game(displayname,request.sid)
            send({
    "type":"wait", "message":"awaiting join"})
        else:
            game = e.opengames.pop()
            gamedata = e.init_game(displayname,request.sid,game)
            send({"type":"joined", "game_data":gamedata})
    """elif msg["type"] == "move":
        if len(e.opengames) == 0:"""
            



"""
@socketio.on('join')
def handleJoin(data):
  print("joined " + str(data))
"""

@socketio.on('connect')
def handleConnection():
  send({
    "type":"chat", 
    "name":"Server", 
    "message":"New Player Connected"}, )

socketio.run(app, host='0.0.0.0', port=8080, debug = True)

