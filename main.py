from kivy.app import App
from kivy.config import Config
from chess_game import initiate_gui

Config.set('graphics', 'window_state', 'maximized')

class ChessApp(App):
    def build(self):
        
        self.game = initiate_gui()

        return self.game
 
app = ChessApp()
app.run()
