from dictionaries.colors import Color, COLORS

class Tile:
    def __init__(self, type, tile, color):
        self.type = type
        self.tile = tile
        self.color = color

tiles = None

def initialize_tiles():
    global tiles

    tiles = {
        'air': Tile('air', " ", COLORS[Color.WHITE]),
        'grass': Tile('grass', ",", COLORS[Color.WHITE]),
        'tree': Tile('tree', "T", COLORS[Color.GREEN]),
        'wall': Tile('wall', "#", COLORS[Color.GRAY]),
    }

def get_tiles():
    if tiles is None:
        initialize_tiles()
    return tiles
