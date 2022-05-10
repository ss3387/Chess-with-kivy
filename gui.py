from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout


class initiate_gui(GridLayout):
    def __init__(self, **kwargs):
        # Super is used to call superclass methods, and to access the superclass constructor
        super(initiate_gui, self).__init__(**kwargs)

        self.cols = 8
        self.rows = 8

        self.Buttons = {}

        for row in range(1, 9):
            for col in range(1, 9):
                move = chr(ord('`') + col) + str(9-row)
                if (col + row) % 2 == 0 :
                    color =  "#ecebd0"
                else:
                    color = "#779556"
                
                self.Buttons[move] = Button(text=move, background_normal='', background_color=color, color=(0, 0, 0, 1))
                self.add_widget(self.Buttons[move])
                print(move)
    
    def update_root(self, uco: str, turn: bool):

        if turn == True:
            rows = uco.split('\n')

            for row in range(1,9):
                currentrow = rows[8-row].split()
                for column in range(1,9):
                    move = chr(ord('`')+column) + str(row)
                    self.Buttons[move].text = currentrow[column-1]
