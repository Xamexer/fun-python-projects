import curses
import time
from curses import wrapper
from curses.textpad import Textbox,rectangle

def main(screen):
    curses.init_pair(1,curses.COLOR_GREEN,curses.COLOR_BLACK)
    GREEN = curses.color_pair(1)

    curses.echo()

    screen.border()

    screen.attron(GREEN)
    rectangle(screen, 1,1,5,20)
    screen.attroff(GREEN)
    screen.addstr(20,20,"HEY")

    screen.move(10,20)

    screen.refresh()
    while True:
        key = screen.getkey()
        if key == "q":
            break

wrapper(main)