from dictionaries.colors import Color, COLORS

class Tile:
    def __init__(self, name, tile, color):
        self.name = name
        self.tile = tile
        self.color = color

tiles = None
colliders = None

def initialize_tiles_and_colliders():
    global tiles, colliders


    tiles = {
        'air': Tile('air', " ", COLORS[Color.WHITE]),
        'grass': Tile('grass', ",", COLORS[Color.WHITE]),
        'tree': Tile('tree', "T", COLORS[Color.GREEN]),
        'wall': Tile('wall', "#", COLORS[Color.GRAY]),
        'box' : Tile('box', '+', COLORS[Color.DARK_GRAY])
    }


    colliders = {
        'walkable' : [tiles['air'], tiles['grass']],
        'solid': [tiles['wall'], tiles['tree']],
        'moveable' : [tiles['box']]
    }

def get_tiles_and_colliders():
    if tiles is None or colliders is None:
        initialize_tiles_and_colliders()
    return tiles, colliders
