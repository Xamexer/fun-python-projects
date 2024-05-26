import curses
from curses import wrapper
import time

def main(screen):
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    COLOR_RED = curses.color_pair(1)
    COLOR_GREEN = curses.color_pair(2)

    counter_win = curses.newwin(1,20,10,10)
    screen.addstr("hello world")
    screen.refresh()
    
    for i in range(100):
        counter_win.clear()
        color = COLOR_RED
        if i % 2 == 0:
            color = COLOR_GREEN
        counter_win.addstr(f"Count: {i}",color)
        counter_win.refresh() # refresh screen
        time.sleep(0.1)

    #screen.addstr(10,10,"hello world", COLOR_RED_BLUE)
    #screen.addstr(15,20,"test2", curses.A_REVERSE | COLOR_GREEN)

    screen.getch() # user input
    

wrapper(main)