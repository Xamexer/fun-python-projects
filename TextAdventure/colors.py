import curses
from enum import Enum

class Color(Enum):
    RED = 1
    ORANGE = 2
    GREEN = 3

# Global color dictionary
COLORS = {}

def initializeColors() -> None:
    curses.start_color()
    curses.use_default_colors()

    curses.init_pair(Color.RED.value, curses.COLOR_RED, -1)
    curses.init_pair(Color.ORANGE.value, 6, -1)
    curses.init_pair(Color.GREEN.value, curses.COLOR_GREEN, -1)
    
    COLORS[Color.RED] = curses.color_pair(Color.RED.value)
    COLORS[Color.ORANGE] = curses.color_pair(Color.ORANGE.value)
    COLORS[Color.GREEN] = curses.color_pair(Color.GREEN.value)
