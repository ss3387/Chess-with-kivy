# Importing kivy objects, client, threading and os
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.slider import Slider
from kivy.uix.gridlayout import GridLayout
from kivy.clock import mainthread
from webserver.realclient import ChessClient
from game import Game
import os
import threading

# This is the main class where everything in the app is stored
class initiate_gui(GridLayout):
    def __init__(self, **kwargs):
        # Super is used to call superclass methods, and to access the superclass constructor
        super(initiate_gui, self).__init__(**kwargs)
        self.cols = 2 # Number of columns in the main grid layout

        # Assigning variables that will be used in other processes
        self.currentlyclicked = ''
        self.prevcolor = ''
        self.flipped_board = False
        self.move_count = 1
        self.game_type = None
        self.level = None
        self.font_path = f"{os.getcwd()}\\FreeSerif.otf"

        # Initialize the widgets here
        self.init_board()
        self.init_other_stuff()
    
    # Create the chess board
    def init_board(self):

        # Use another gridlayout for chess grid because it needs 8 columns
        self.chess_grid = GridLayout(cols=8, rows=8)
        self.add_widget(self.chess_grid)

        # Create a dictionary of all the squares on the board
        self.Buttons = {}



        # More effcient way of creating 64 buttons
        for row in range(1, 9):
            for col in range(1, 9):
                # This gives the notation of the specific square for example 'e4' is 5th column and 4th row
                move = chr(ord('`') + col) + str(9-row)

                # Change the color when it moves to the next square
                if (col + row) % 2 == 0 :
                    color =  '#ecebd0'
                else:
                    color = '#779556'
                
                # Create a Button
                btn = Button(background_normal='', background_color=color, color=(0, 0, 0, 1), font_name=self.font_path, font_size=50)
                # Bind the button with add_move function
                btn.bind(on_press=lambda instance, move= move: self.add_move(instance, move))
                # Assign the square notation to this button
                self.Buttons[move] = btn
                # Add widget on the chess grid
                self.chess_grid.add_widget(self.Buttons[move])
    
    # Here it creates the widgets that are need for the player to do something: example joining a game
    def init_other_stuff(self):

        self.other_grid = GridLayout(cols=2)
        self.add_widget(self.other_grid)

        # Create a label where it shows the opponent name
        self.opponent_name_label = Label(text='', font_size=20, size_hint_y=None, size_hint_x=1.3, height=80)
        self.other_grid.add_widget(self.opponent_name_label)

        # A button for flipping the board
        self.flip_button = Button(text='Flip Board', size_hint_y=None, height=80)
        self.flip_button.bind(on_press = self.flip_board) # Calls "self.flip_board()" when pressed
        self.other_grid.add_widget(self.flip_button)

        self.white_moves = TextInput(text='\t\t\t\t\t\t\t\t\t White\n', multiline=True, readonly=True, size_hint_y=None, height=400)
        self.other_grid.add_widget(self.white_moves)

        self.black_moves = TextInput(text='\t\t\t\t\t\t\t Black\n', multiline=True, readonly=True, size_hint_y=None, height=400)
        self.other_grid.add_widget(self.black_moves)

        self.play_option_grid = GridLayout(cols=2, size_hint_y=None)
        self.other_grid.add_widget(self.play_option_grid)

        self.play_offline = Button(text='Human vs Human', size_hint_y=None)
        self.play_offline.bind(on_press=self.run_offline_game)
        self.play_option_grid.add_widget(self.play_offline)

        self.play_online = Button(text='Play Online', size_hint_y=None)
        self.play_online.bind(on_press = self.initiate_client)
        self.play_option_grid.add_widget(self.play_online)

        self.play_computer = Button(text='Play against Computer', size_hint_y=None)
        self.play_computer.bind(on_press=lambda instance: self.run_offline_game(instance, against_computer=True))
        self.other_grid.add_widget(self.play_computer)

        self.ask_name = Label(text='Enter your name: ')
        self.entry_name = TextInput(multiline=False)

        self.level_choosing = GridLayout(cols=1, rows=2)
        self.ask_level = Label(text='Choose a level (1-20):  1')
        self.level_slider = Slider(min=1, max=20, step=1, orientation='horizontal')
        self.level_slider.bind(value=self.level_choice)

        self.level_choosing.add_widget(self.ask_level)
        self.level_choosing.add_widget(self.level_slider)

        self.request_takeback = Button(text='Request a takeback')
        self.resign_btn = Button(text='resign')

        self.result = Label(font_size=20)
    
    @mainthread
    def update_widgets(self, game_type: str):
        if game_type == 'Offline':
            self.undo = Button(text='undo')
            self.undo.bind(on_press=self.game.undo)
            if self.result.text != '':
                self.other_grid.remove_widget(self.result)
                self.other_grid.add_widget(self.undo)
            elif self.game_type != 'Offline':
                self.other_grid.add_widget(self.undo)
            self.game_type = game_type
            self.white_moves.text = '\t\t\t\t\t\t\t\t\t White\n'
            self.black_moves.text = '\t\t\t\t\t\t\t Black\n'
        else:
            self.game_type = game_type
            self.other_grid.remove_widget(self.ask_name)
            self.other_grid.remove_widget(self.entry_name)
            self.request_takeback.bind(on_press=self.client.request_takeback)
            self.other_grid.add_widget(self.request_takeback)
            self.resign_btn.bind(on_press=self.client.resign)
            self.other_grid.add_widget(self.resign_btn)

    @mainthread
    def update_movelist(self, san: str, turn: str):
        if san == 'undo':
            if self.move_count > 1:
                white_rows = self.white_moves.text.split('\n')
                black_rows = self.black_moves.text.split('\n')
                for i in range(2):
                    white_rows.pop()
                    black_rows.pop()
                self.white_moves.text = '\n'.join(white_rows) + '\n'
                self.black_moves.text = '\n'.join(black_rows) + '\n'
                self.move_count -= 1
            else:
                return
        elif san != None:
            if turn == 'black':
                self.white_moves.text += f"{self.move_count}.\t{san}\n"
            else:
                self.black_moves.text += f"{san}\n"
                self.move_count += 1
    
    @mainthread
    def update_root(self, uco: str, san: str, turn: str, msg = '', name = None):
        if type(name) == str:
            self.opponent_name_label.text = f"Opponent: {name}"
        elif msg == '' or type(msg) == bool:
            self.update_movelist(san, turn)
            uco = uco.replace('⭘', '\u2800')
            if uco != '':
                rows = uco.split('\n')
                for row in range(1,9):
                    currentrow = rows[8-row].split()
                    for column in range(1,9):
                        move = chr(ord('`') + column) + str(row)
                        self.Buttons[move].text = currentrow[column-1].replace('\u2800', '')
            if msg:
                self.flip_board(None)
        elif msg == 'takeback_request':
            self.other_grid.remove_widget(self.request_takeback)
            self.other_grid.remove_widget(self.resign_btn)

            self.accept_or_decline = GridLayout(cols=2)
            self.other_grid.add_widget(self.accept_or_decline)

            accept = Button(text='Accept Takeback')
            accept.bind(on_press = self.accept_takeback)
            self.accept_or_decline.add_widget(accept)

            decline = Button(text='Decline Takeback')
            decline.bind(on_press=self.decline_undo)
            self.accept_or_decline.add_widget(decline)

            self.other_grid.add_widget(self.resign_btn)
        else:
            if self.game_type == 'Online':
                self.other_grid.remove_widget(self.request_takeback)
                self.other_grid.remove_widget(self.resign_btn)
            else:
                self.other_grid.remove_widget(self.undo)
            self.other_grid.add_widget(self.result)
            self.result.text = msg
            self.move_count = 1
            self.game_type = None
            
    @mainthread
    def flip_board(self, instance):
        for sq in self.Buttons.keys():
            self.chess_grid.remove_widget(self.Buttons[sq])
        for row in range(1, 9):
            for col in range(1, 9):
                if not self.flipped_board:
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
            if self.game_type != None:
                if self.game_type == 'Online':
                    self.client.do_move(self.currentlyclicked + move)
                else:
                    self.game.add_move(self.currentlyclicked + move)
            self.currentlyclicked = ''

        else:
            # Select the piece you want to move
            self.prevcolor = self.Buttons[move].background_color
            self.Buttons[move].background_color = '#BACA2B'
            # Save the position as currentlyclicked
            self.currentlyclicked = move
    
    def level_choice(self, *args):
        self.ask_level.text = f"Choose a level:  {args[1]}"
        self.level = args[1]

    def run_offline_game(self, instance, against_computer = False):
        if against_computer and self.level == None:
            self.other_grid.add_widget(self.level_choosing)
            self.level = 1
        else:
            threading.Thread(target=self.init_offline_game, args=(against_computer, self.level), daemon=True).start()
            self.other_grid.remove_widget(self.level_choosing)
            self.level = None
    
    def init_offline_game(self, against_computer: bool, level: int):
        self.game = Game(self.update_root, against_computer, level)
        self.update_widgets(game_type='Offline')
        
    def initiate_client(self, instance):
        if len(self.entry_name.text) != 0:
            threading.Thread(target= self.run_client, daemon=True).start()
        else:
            self.other_grid.add_widget(self.ask_name)
            self.other_grid.add_widget(self.entry_name)

    def run_client(self):
        self.client = ChessClient(addr='http://127.0.0.1:8080', update_board=self.update_root, name=self.entry_name.text)
        self.update_widgets(game_type='Online')
    
    def accept_takeback(self, instance):
        self.client.accept_takeback()
        self.other_grid.remove_widget(self.accept_or_decline)
        self.other_grid.remove_widget(self.resign_btn)
        self.other_grid.add_widget(self.request_takeback)
        self.other_grid.add_widget(self.resign_btn)

    def decline_undo(self, instance):
        self.other_grid.remove_widget(self.accept_or_decline)
        self.other_grid.remove_widget(self.resign_btn)
        self.other_grid.add_widget(self.request_takeback)
        self.other_grid.add_widget(self.resign_btn)
        
