from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from webserver.realclient import ChessClient
import threading

class initiate_gui(GridLayout):
    def __init__(self, **kwargs):
        # Super is used to call superclass methods, and to access the superclass constructor
        super(initiate_gui, self).__init__(**kwargs)
        self.cols = 2

        self.currentlyclicked = ''
        self.prevcolor = ''
        self.flipped_board = False
        self.movelist = []
        threading.Thread(target=self.initiate_client).start()
        """self.SANDICT = {
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
        }"""

        self.chess_grid = GridLayout()

        self.chess_grid.cols = 8
        self.chess_grid.rows = 8

        self.add_widget(self.chess_grid)

        self.Buttons = {}

        self.init_board()
        
        self.other_grid = GridLayout()
        self.other_grid.cols = 1
        self.add_widget(self.other_grid)

        self.flip_button = Button(text='Flip Board')
        self.flip_button.bind(on_press = self.flip_board)

        self.other_grid.add_widget(self.flip_button)
    
    def init_board(self):
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
                self.chess_grid.add_widget(self.Buttons[move])

    def initiate_client(self):
        try:
            print('started')
            self.client = ChessClient(addr='http://127.0.0.1:8080', update_board=self.update_root, name=input('Enter your name'))
            input('wait...')
            print(self.client.turn)
            print(self.client.opponent)
            print(self.client.player_id)
        except:
            print('Sorry cannot connect to the server')
    
    def update_root(self, uco: str):
        if self.flipped_board == True:
            uco = uco[::-1]
        rows = uco.split('\n')
        for row in range(1,9):
            currentrow = rows[8-row].split()
            for column in range(1,9):
                move = chr(ord('`')+column) + str(row)
                self.Buttons[move].text = currentrow[column-1]
    
    def flip_board(self, instance):
        for sq in self.Buttons.keys():
            self.chess_grid.remove_widget(self.Buttons[sq])
        for row in range(1, 9):
            for col in range(1, 9):
                if self.flipped_board == False:
                    move = chr(ord('`') + 9-col) + str(row)
                else:
                    move = chr(ord('`') + col) + str(9-row)
                self.chess_grid.add_widget(self.Buttons[move])
        self.flipped_board = not self.flipped_board
        
        

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
    
    def add_move(self, instance, move: str):

        if self.currentlyclicked == move:
            # Unselect piece
            self.Buttons[move].background_color = self.prevcolor
            self.currentlyclicked = ''
        
        elif self.currentlyclicked != '':

            # Move the piece to the desired square (actual move)

            self.Buttons[self.currentlyclicked].background_color = self.prevcolor
            self.client.do_move(self.currentlyclicked + move)

            '''if chess.Move.from_uci(uci) in self.board.legal_moves:
                self.add_movelist(self.SANDICT[self.Buttons[self.currentlyclicked].text], move)
                print(self.movelist)'''

            self.currentlyclicked = ''
        else:
            # Select the piece you want to move
            self.prevcolor = self.Buttons[move].background_color
            self.Buttons[move].background_color = '#BACA2B'
            # Save the position as currentlyclicked
            self.currentlyclicked = move
