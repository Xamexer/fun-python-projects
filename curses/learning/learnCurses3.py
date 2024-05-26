import curses
import time
from curses import wrapper

def main(screen):
    curses.init_pair(1,curses.COLOR_GREEN,curses.COLOR_BLACK)
    GREEN = curses.color_pair(1)
    screen.nodelay(True)

    x,y = 0,0
    string_x = 0
    while True:
        try:
            key = screen.getkey()
        except:
            key = None

        match key:
            case "KEY_LEFT":
                x -= 1
            case "KEY_RIGHT":
                x += 1
            case "KEY_UP":
                y -= 1
            case "KEY_DOWN":
                y += 1
            case "q":
                exit()
        screen.clear()
        string_x +=1
        screen.addstr(0, string_x//100,"hello world")
        screen.addstr(y,x, "0")
        screen.refresh()

wrapper(main)