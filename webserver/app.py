from flask import Flask, session 
from flask_socketio import SocketIO, send
from flask_socketio import join_room, leave_room
import os
import uuid

import chess


app = Flask(__name__)
app.secret_key = os.urandom(24)
socketio = SocketIO(app)


class GameData:
    def __init__(self):
        self.opengames = {}
        self.playinggames = {}
        self.currentlyplaying = []

    def init_game(self,displayname,game_id):

        play_game = self.opengames[game_id]
        del self.opengames[game_id]
        player_id = str(uuid.uuid4().fields[-1])[:5]


        gameobject = {
            "status":"RUNNING",
            "player_ids": [play_game["player_id"],player_id],
            "display_names": [play_game["display_name"],displayname],
            ## Only for displaying move to spectator
            "movelist": [],
            "board": chess.Board(),

        }
        self.playinggames[game_id] = gameobject
        self.currentlyplaying.append(play_game["player_id"])
        self.currentlyplaying.append(player_id)
        return gameobject

    def init_new_game(self,displayname):
        game_id = str(uuid.uuid4().fields[-1])[:5]
        player_id = str(uuid.uuid4().fields[-1])[:5]

        gameobject = {
            "player_id": player_id,
            "display_name":displayname
        }
        self.opengames[game_id] = gameobject
        self.currentlyplaying.append(player_id)
        ## change to player l8r
        return game_id

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


x = e.init_new_game("maison")
print(e.opengames)

test = e.init_game("francis",x)
print(e.playinggames)

x = e.init_new_game("maison")
print(e.opengames)

@app.route("/playinggames")
def games():
    return e.get_playing_games()

@app.route("/opengames")
def adwdw():
    return e.get_open_games()

app.run()


