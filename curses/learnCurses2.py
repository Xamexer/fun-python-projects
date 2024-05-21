import curses
from curses import wrapper
import time

def main(s):
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    COLOR_RED = curses.color_pair(1)
    COLOR_GREEN = curses.color_pair(2)

    pad = curses.newpad(100,100)
    s.refresh()

    for i in range(100):
        for j in range(26):
            char = chr(67 + j)
            pad.addstr(char, COLOR_GREEN)

    #curses.LINES - 1, curses.COLS - 1
    for i in range(100):
        s.clear()
        s.refresh()        
        pad.refresh(i,0,0,0,20,20)
        time.sleep(0.2)
    s.getch() # user input
    

wrapper(main)