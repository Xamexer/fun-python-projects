from dictionaries.colors import Color, COLORS
class Player:
    def __init__(self, map_width, map_height):
        self.symbol = "o"
        self.name = "Zet"
        self.color = COLORS[Color.GREEN]
        self.coordinate_x = map_width // 2
        self.coordinate_y = map_height // 2

    def move(self, x_change, y_change) -> None:
        self.coordinate_x += x_change
        self.coordinate_y += y_change
