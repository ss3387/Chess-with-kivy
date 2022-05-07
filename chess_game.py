import chess
import chess.engine
import queue
import threading

class main_game:
    def __init__(self):
        pass

"""from time import sleep
import chess
import chess.engine
import queue
from tkinter import *
import threading



SANDICT = {
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

class ChessBoard:
    def __init__(self):
        self.signal_stop = False
        threading.Thread(target=self.init_board).start()

    def stop(self):
        print("HERE")
        self.signal_stop = True
        print(self.signal_stop)

    def init_board(self):
        # Initiate tkinter / gui here
        self.root = Tk()
        self.root.geometry('400x400')
        self.root.rowconfigure((1, 2, 3, 4, 5, 6, 7, 8), weight=1)
        self.root.columnconfigure((1, 2, 3, 4, 5, 6, 7, 8), weight=1)
        
        self.Buttons = {}

        self.menu = Menu(self.root)
        self.root['menu'] = self.menu
        self.file = Menu(self.menu)
        self.menu.add_cascade(label='File', menu=self.file)
        self.file.add_command(label='New', command=lambda:self.stop())

        for row in range(1,9):
            ## Get row letter
            for column in range(1,9):

                move = chr(ord('`')+column) + str(row)
                if (column + row) % 2 == 0 :
                    color = "#779556"
                else:
                    color = "#EBECD0"
                ## Create button with row letter and column num
                button = Button(self.root, font=('Arial', 20), command=lambda move = move: self.add_move(move),bg=color)
                button.grid(row=8-row, column=column, sticky=NSEW)
                self.Buttons[move] = button


        self.root.mainloop()
    
    def update_root(self,board):
        ## Update tkinter here

        unicode = board.unicode()
        
        rows = unicode.split("\n")

        for row in range(1,9):
            currentrow = rows[8-row].split()
            for column in range(1,9):
                move = chr(ord('`')+column) + str(row)
                self.Buttons[move]["text"] = currentrow[column-1]
        
    def add_movelist(self, piece, move):
        if self.board.is_checkmate() == True:
            self.movelist.append(f"{piece}{move}#")
        elif self.board.is_check() == True:
            self.movelist.append(f"{piece}{move}+")
        elif self.Buttons[move]['text'] != '⭘':
            self.movelist.append(f"{piece}x{move}")
        elif piece == '':
            self.movelist.append(move)
        else:
            self.movelist.append(f"{piece}{move}")
        
            
    def add_move(self,move):
        if self.currentyclicked == move:
            ## Unselect
            self.Buttons[move]["bg"] = self.prevcolor
            self.currentyclicked = ""
        elif self.currentyclicked != "":
            ## Detect that player wants to play move
            uci = self.currentyclicked + move
            self.movequeue.put(uci)
            self.Buttons[self.currentyclicked]["bg"] = self.prevcolor

            if chess.Move.from_uci(uci) in self.board.legal_moves:
                self.add_movelist(SANDICT[self.Buttons[self.currentyclicked]['text']], move)
                print(self.movelist)

            self.currentyclicked = ""
        else:
            self.prevcolor = self.Buttons[move]["bg"]
            self.Buttons[move]["bg"] = "#BACA2B"
            self.currentyclicked = move

    def initate_new_game(self):

        ## Initiate game here
        self.currentyclicked = ""
        ## Lazy way of not having to recalculate letter to color etc..
        self.prevcolor = ""
        self.movequeue = queue.Queue()
        print(f"{self.movequeue}dflkhwajsnpodivicwnpoad")
        self.movelist = []
        self.board = chess.Board()
        ## Already clicked board coordinat

        while not self.board.is_game_over():
            try:
                if self.signal_stop == True:
                    print("exitting loop")
                    break
                else:
                    print(self.signal_stop)
                self.update_root(self.board)
                move = self.movequeue.get()
                turn = self.board.turn
                if turn == chess.WHITE:
                    turn = "white"
                else:
                    turn = "black"
                ## Convert move to chess move
                if chess.Move.from_uci(move) in self.board.legal_moves:
                    self.board.push_uci(move)
                elif move == 'e1h1' or move == 'e8h8':
                    self.board.push_san(move)
                elif chess.Move.from_uci(move + "q") in self.board.legal_moves:
                    ## Prompt what they want to promote here
                    ""
                else:
                    print("invalid move")
                
                ## Evaluate after each move
                print(self.evaluation(self.board,color=turn))
                
                #self.analyze_board(board)
            except Exception as e:
                print(e)
                pass

        if self.signal_stop:
            print("SIGNAL OUTSIDEEEEE")
            self.signal_stop = False
            self.initate_new_game()
        else:
            sleep(1)
            winner = self.board.result()
            print(winner)

            print("game is done")


    def analysis(self,board, time_limit = 0.5):
        engine = chess.engine.SimpleEngine.popen_uci("stockfish_14.1_win_x64_avx2.exe")
        info = engine.analyse(board, chess.engine.Limit(time=time_limit))
        engine.quit()
        return info

    def evaluation(self, board, color='white', time_limit = 1):
        info = self.analysis(board, time_limit)
        if color == 'white':
            score = info['score'].white().score()
        else:
            score = info['score'].black().score()
        return score


    

test = ChessBoard()
test.initate_new_game()
"""