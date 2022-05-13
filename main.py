from kivy.app import App
from kivy.config import Config
from kivy.core.window import Window
from chess_game import initiate_gui

Config.set('kivy', 'exit_on_escape', '0')

class ChessApp(App):
    def build(self):
        
        self.game = initiate_gui()

        Window.bind(on_request_close= self.on_close)

        return self.game
    
    def on_close(self, *args):
        # Do something to stop socket
        self.stop()


app = ChessApp()
app.run()
