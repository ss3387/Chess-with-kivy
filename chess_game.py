from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from webserver.realclient import ChessClient
import threading

class initiate_gui(GridLayout):
    def __init__(self, **kwargs):
        # Super is used to call superclass methods, and to access the superclass constructor
        super(initiate_gui, self).__init__(**kwargs)
        self.currentlyclicked = ''
        self.prevcolor = ''
        self.movelist = []
        #self.gui = initiate_gui()
        #self.board = chess.Board()
        #self.gui.update_root(self.board.unicode())

        threading.Thread(target=self.initiate_client).start()
        
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

        self.cols = 8
        self.rows = 8

        self.Buttons = {}

        for row in range(1, 9):
            for col in range(1, 9):
                move = chr(ord('`') + col) + str(9-row)
                if (col + row) % 2 == 0 :
                    color =  '#ecebd0'
                else:
                    color = '#779556'
                
                btn = Button(background_normal='', background_color=color, color=(0, 0, 0, 1), font_name='FreeSerif.otf', font_size=32)
                btn.bind(on_press=lambda instance, move= move: self.add_move(instance, move))
                self.Buttons[move] = btn
                self.add_widget(self.Buttons[move])
    
    def initiate_client(self):
        print('started')
        self.client = ChessClient(addr='http://127.0.0.1:8080', update_board=self.update_root)
        input('wait...')
        print(self.client.turn)
        print(self.client.opponent)
        print(self.client.player_id)
        while True:
            move = input('enter move')
            self.client.do_move(move)
    
    def update_root(self, uco: str):

        
        rows = uco.split('\n')
        print(rows)
        for row in range(1,9):
            currentrow = rows[8-row].split()
            print(currentrow)
            for column in range(1,9):
                move = chr(ord('`')+column) + str(row)
                self.Buttons[move].text = currentrow[column-1]
    
    def add_movelist(self, piece, move):
        if self.board.is_checkmate() == True:
            self.movelist.append(f'{piece}{move}#')
        elif self.board.is_check() == True:
            self.movelist.append(f'{piece}{move}+')
        elif self.Buttons[move]['text'] != ' ':
            self.movelist.append(f'{piece}x{move}')
        elif piece == '':
            self.movelist.append(move)
        else:
            self.movelist.append(f'{piece}{move}')
    
    def add_move(self, instance, move):
        if self.currentlyclicked == move:
            # Unselect
            self.Buttons[move].background_color = self.prevcolor
            self.currentlyclicked = ''
        elif self.currentlyclicked != '':
            ## Detect that player wants to play move
            #uci = self.currentlyclicked + move
            #self.movequeue.put(uci)
            self.Buttons[self.currentlyclicked].background_color = self.prevcolor
            self.client.do_move(move)

            '''if chess.Move.from_uci(uci) in self.board.legal_moves:
                self.add_movelist(self.SANDICT[self.Buttons[self.currentlyclicked].text], move)
                print(self.movelist)'''

            self.currentlyclicked = ''
        else:
            self.prevcolor = self.Buttons[move].background_color
            self.Buttons[move].background_color = '#BACA2B'
            self.currentlyclicked = move
