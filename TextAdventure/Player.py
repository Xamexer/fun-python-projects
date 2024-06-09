
class Player:
    def __init__(self):
        self.symbol = "o"
        self.name = "z"
        self.coordinate_x = 2
        self.coordinate_y = 20
    
    def move_player_x(self,x_change) -> None:
        self.coordinate_x += x_change

    def move_player_y(self,y_change) -> None:
        self.coordinate_y += y_change
