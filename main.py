from kivy.config import Config
Config.set('graphics', 'window_state', 'maximized')
Config.set('kivy', 'exit_on_escape', '0')

from kivy.app import App
from chess_game import initiate_gui
from kivy.core.window import Window

class ChessApp(App):
    def build(self):
        
        self.game = initiate_gui()

        Window.bind(on_request_close=self.on_close)

        return self.game
    
    def on_close(self, *args):
        if self.game.game_type == 'Online':
            self.game.client.resign(True)
        self.stop()
 
app = ChessApp()
app.run()
