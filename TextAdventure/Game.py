import time
import random
from colors import COLORS, Color
from CursesUtilities import CursesUtilities
##### (y,x)
##01y
#0
#1
#x
class Game:
    def __init__(self, screen) -> None:
        self.screen = screen
        self.cUtils = CursesUtilities(screen)

        self.cUtils.drawBorder((5, 20), (2, 10), 'x', COLORS[Color.RED])
        #self.screen.addstr(5,10,f'#',COLORS[Color.GREEN])
        self.screen.refresh()
        time.sleep(5)
