"""from flask import Flask, session 
from flask_socketio import SocketIO, send
from flask_socketio import join_room, leave_room"""
import os
import uuid

import chess

"""
app = Flask(__name__)
app.secret_key = os.urandom(24)
socketio = SocketIO(app)
"""

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
        ## change to player l8r
        return game_id

    def get_games(self):
        return self.games

    def add_move(self,gameid,move):
        self.games[gameid]["moves"].append(move)


e = GameData()


x = e.init_new_game("maison")
print(e.opengames)

test = e.init_game("francis",x)
print(e.playinggames)


