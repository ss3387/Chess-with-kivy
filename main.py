from kivy.config import Config
Config.set('graphics', 'window_state', 'maximized')
#Config.set('graphics', 'resizable', False)

from kivy.app import App
from chess_game import initiate_gui



class ChessApp(App):
    def build(self):
        
        self.game = initiate_gui()

        return self.game
 
app = ChessApp()
app.run()
