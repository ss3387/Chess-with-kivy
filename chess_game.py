from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.clock import mainthread
from matplotlib.pyplot import text
from webserver.realclient import ChessClient
import threading
import time

class initiate_gui(GridLayout):
    def __init__(self, **kwargs):
        # Super is used to call superclass methods, and to access the superclass constructor
        super(initiate_gui, self).__init__(**kwargs)
        self.cols = 2

        self.currentlyclicked = ''
        self.prevcolor = ''
        self.flipped_board = False
        self.move_count = 1

        self.init_board()
        self.init_other_stuff()
    
    def init_board(self):

        self.chess_grid = GridLayout()

        self.chess_grid.cols = 8
        self.chess_grid.rows = 8

        self.add_widget(self.chess_grid)

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
                self.chess_grid.add_widget(self.Buttons[move])
    
    def init_other_stuff(self):
        self.other_grid = GridLayout()
        self.other_grid.cols = 2

        self.add_widget(self.other_grid)

        self.opponent_name_label = Label(text='rg', font_size=20, size_hint_y=None, size_hint_x=1.3, height=80, halign='left')
        self.opponent_name_label.valign = 'top'
        self.other_grid.add_widget(self.opponent_name_label)

        self.flip_button = Button(text='Flip Board', size_hint_y=None, height=80)
        self.flip_button.bind(on_press = self.flip_board)
        self.other_grid.add_widget(self.flip_button)

        self.white_moves = TextInput(text='\t\t\t\t\t\t\t\t\t White\n', multiline=True, readonly=False, size_hint_y=None, height=400)
        self.other_grid.add_widget(self.white_moves)

        self.black_moves = TextInput(text='\t\t\t\t\t\t\t Black\n', multiline=True, readonly=False, size_hint_y=None, height=400)
        self.other_grid.add_widget(self.black_moves)

        self.play_option_grid = GridLayout(cols=2, size_hint_y=None)
        self.other_grid.add_widget(self.play_option_grid)

        self.play_offline = Button(text='Human vs Human', size_hint_y=None)
        self.play_option_grid.add_widget(self.play_offline)

        self.play_online = Button(text='Play Online', size_hint_y=None)
        self.play_online.bind(on_press = self.initiate_client)
        self.play_option_grid.add_widget(self.play_online)

        self.play_computer = Button(text='Play against Computer', size_hint_y=None)
        self.other_grid.add_widget(self.play_computer)

        self.ask_name = Label(text='Enter your name: ')
        self.entry_name = TextInput(multiline=False)


    def initiate_client(self, instance):
        if len(self.entry_name.text) != 0:
            
            self.client_thread = threading.Thread(target= self.run_client, daemon=True)
            self.client_thread.start()
            self.game_type = 'Online'

            time.sleep(1)

            self.other_grid.remove_widget(self.ask_name)
            self.other_grid.remove_widget(self.entry_name)

            self.request_takeback = Button(text='Offer a draw')
            self.request_takeback.bind(on_press=self.client.request_takeback)
            self.other_grid.add_widget(self.request_takeback)

            self.resign_btn = Button(text='resign')
            self.resign_btn.bind(on_press=self.client.resign)
            self.other_grid.add_widget(self.resign_btn)
            
        else:
            self.other_grid.add_widget(self.ask_name)
            self.other_grid.add_widget(self.entry_name)


    def run_client(self):
        self.client = ChessClient(addr='http://127.0.0.1:8080', update_board=self.update_root, name=self.entry_name.text)
    

    @mainthread
    def update_movelist(self, san: str, turn: str):
        if san == 'undo':
            if self.move_count > 1:
                white_rows = self.white_moves.text.split('\n')
                black_rows = self.black_moves.text.split('\n')
                white_rows.pop()
                black_rows.pop()
                self.white_moves.text = '\n'.join(white_rows)
                self.black_moves.text = '\n'.join(black_rows)
            else:
                return
        elif san != None:
            if turn == 'black':
                self.white_moves.text += f"{self.move_count}.\t{san}\n"
            else:
                self.black_moves.text += f"{san}\n"
                self.move_count += 1
            print(self.move_count)


    def update_root(self, uco: str, san: str, turn: str, msg = ''):
        
        if msg == '' or msg == bool:
            self.update_movelist(san, turn)
            if uco != '':
                rows = uco.split('\n')
                for row in range(1,9):
                    currentrow = rows[8-row].split()
                    for column in range(1,9):
                        move = chr(ord('`') + column) + str(row)
                        self.Buttons[move].text = currentrow[column-1]
            if msg == True:
                self.flip_board(None)
        elif msg == 'takeback_request':
            self.other_grid.remove_widget(self.request_takeback)
            self.other_grid.remove_widget(self.resign_btn)

            self.accept_or_decline = GridLayout(cols=2)

            accept = Button(text='Accept Takeback')
            accept.bind(on_press = self.client.accept_takeback)
            self.accept_or_decline.add_widget(accept)

            decline = Button(text='Decline Takeback')
            decline.bind(on_press=self.decline_undo)
            self.accept_or_decline.add_widget(decline)

            self.other_grid.add_widget(self.resign_btn)
        else:
            if self.game_type == 'Online':
                self.other_grid.remove_widget(self.request_takeback)
                self.other_grid.remove_widget(self.resign_btn)
            self.result = Label(text=msg, font_size=20)
            self.other_grid.add_widget(self.result)
        
    def decline_undo(self, instance):
        self.other_grid.remove_widget(self.accept_or_decline)
        self.other_grid.remove_widget(self.resign_btn)
        self.other_grid.add_widget(self.request_takeback)
        self.other_grid.add_widget(self.resign_btn)
    
    @mainthread
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
    
    def add_move(self, instance, move: str):

        if self.currentlyclicked == move:
            # Unselect piece
            self.Buttons[move].background_color = self.prevcolor
            self.currentlyclicked = ''
        
        elif self.currentlyclicked != '':
            # Move the piece to the desired square (actual move)
            self.Buttons[self.currentlyclicked].background_color = self.prevcolor
            self.client.do_move(self.currentlyclicked + move)
            self.currentlyclicked = ''

        else:
            # Select the piece you want to move
            self.prevcolor = self.Buttons[move].background_color
            self.Buttons[move].background_color = '#BACA2B'
            # Save the position as currentlyclicked
            self.currentlyclicked = move
