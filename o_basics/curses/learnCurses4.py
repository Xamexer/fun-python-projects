import curses
import time
from curses import wrapper
from curses.textpad import Textbox,rectangle

def main(screen):
    curses.init_pair(1,curses.COLOR_GREEN,curses.COLOR_BLACK)
    GREEN = curses.color_pair(1)

    win = curses.newwin(3,18,2,2)
    box = Textbox(win)
    rectangle(screen, 1,1,5,20)

    screen.refresh()
    
    box.edit()
    text = box.gather().strip().replace("\n","")

    screen.addstr(10,40,text)
    screen.getch()

wrapper(main)