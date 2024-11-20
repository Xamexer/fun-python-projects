from dictionaries.colors import Color, COLORS
import time
class Tile:
     def __init__(self,name,tile,color):
          self.name = name
          self.tile = tile
          self.color = color

print(COLORS)
time.sleep(20)

tiles = {
    'air': Tile('air', " ", COLORS[Color.WHITE]),
    'grass': Tile('grass', ",", COLORS[Color.GREEN]),
    'tree': Tile('tree', "T", COLORS[Color.DARK_GREEN]),
    'wall': Tile('wall', "#", COLORS[Color.GRAY]),
}

colliders = {
    'solid': [tiles['wall'].tile, tiles['tree'].tile],
}