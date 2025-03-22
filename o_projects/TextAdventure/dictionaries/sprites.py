from dictionaries.colors import Color, COLORS

class Sprite:
    def __init__(self, name, type, symbol, color,coordinate_x,coordinate_y):
        self.name = name
        self.type = type
        self.symbol = symbol
        self.color = color
        self.coordinate_x = coordinate_x
        self.coordinate_y = coordinate_y

    def set_pos (self, coordinate_x, coordinate_y):
        self.coordinate_x = coordinate_x
        self.coordinate_y = coordinate_y

    def move (self, move_x, move_y):
        self.coordinate_x += move_x
        self.coordinate_y += move_y
