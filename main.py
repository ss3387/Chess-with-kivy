from kivy.app import App
from chess_game import main_game


class ChessApp(App):
    def build(self):
        
        self.game = main_game()

        return self.game.gui

app = ChessApp()
app.run()
