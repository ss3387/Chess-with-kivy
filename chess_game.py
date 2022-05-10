import chess
import queue
import threading
from gui import initiate_gui

class main_game:
    def __init__(self):
        self.signal_stop = False
        self.currentlyclicked = ''
        self.prevcolor = ''
        self.movelist = []

        self.SANDICT = {
            # Pawns
            '♙': '',
            '♟': '',
            # Bishops
            '♗': 'B',
            '♝': 'B',
            # Knights
            '♘': 'N',
            '♞': 'N',
            # Rooks
            '♖': 'R',
            '♜': 'R',
            # Queens
            '♕': 'Q',
            '♛': 'Q',
            # Kings
            '♔': 'K',
            '♚': 'K'
        }

        self.gui = initiate_gui()

        #self.gui.update_root()
    
    def add_movelist(self, piece, move):
        if self.board.is_checkmate() == True:
            self.movelist.append(f"{piece}{move}#")
        elif self.board.is_check() == True:
            self.movelist.append(f"{piece}{move}+")
        elif self.Buttons[move]['text'] != ' ':
            self.movelist.append(f"{piece}x{move}")
        elif piece == '':
            self.movelist.append(move)
        else:
            self.movelist.append(f"{piece}{move}")
    
    def add_move(self, move):
        if self.currentlyclicked == move:
            # Unselect
            self.Buttons[move].background_color = self.prevcolor
            self.currentlyclicked = ""
        elif self.currentlyclicked != "":
            ## Detect that player wants to play move
            #uci = self.currentlyclicked + move
            #self.movequeue.put(uci)
            self.Buttons[self.currentlyclicked].background_color = self.prevcolor

            """if chess.Move.from_uci(uci) in self.board.legal_moves:
                self.add_movelist(self.SANDICT[self.Buttons[self.currentlyclicked].text], move)
                print(self.movelist)"""

            self.currentlyclicked = ""
        else:
            self.prevcolor = self.Buttons[move].background_color
            self.Buttons[move].background_color = "#BACA2B"
            self.currentlyclicked = move

