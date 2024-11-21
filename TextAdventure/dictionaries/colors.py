import curses
from enum import Enum

class Color(Enum):
    RED = 1
    ORANGE = 2
    GREEN = 3
    WHITE = 4
    DARK_GREEN = 5
    GRAY =  6
    DARK_GRAY = 7

# Global color dictionary
COLORS = {}

def initialize_colors() -> None:
    curses.start_color()
    curses.use_default_colors()

    curses.init_pair(Color.RED.value, curses.COLOR_RED, -1)
    curses.init_pair(Color.ORANGE.value, 6, -1)
    curses.init_pair(Color.GREEN.value, curses.COLOR_GREEN, -1)
    curses.init_pair(Color.WHITE.value, curses.COLOR_WHITE, -1)
    curses.init_pair(Color.DARK_GREEN.value, 2, -1)
    curses.init_pair(Color.GRAY.value, 8, -1)
    curses.init_pair(Color.DARK_GRAY.value, 7, -1)

    COLORS[Color.RED] = curses.color_pair(Color.RED.value)
    COLORS[Color.ORANGE] = curses.color_pair(Color.ORANGE.value)
    COLORS[Color.GREEN] = curses.color_pair(Color.GREEN.value)
    COLORS[Color.WHITE] = curses.color_pair(Color.WHITE.value)
    COLORS[Color.DARK_GREEN] = curses.color_pair(Color.DARK_GREEN.value)
    COLORS[Color.GRAY] = curses.color_pair(Color.GRAY.value)
    COLORS[Color.DARK_GRAY] = curses.color_pair(Color.DARK_GRAY.value)