import time
import curses
import random
from curses import wrapper

with open('.\\sentences.txt', 'r') as file:
    sentences = [line.strip() for line in file]

def main(screen):
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    COLOR_GREEN = curses.color_pair(1)
    COLOR_RED = curses.color_pair(2)
    screen.nodelay(True)

    sentence = sentences[random.randint(0, len(sentences)-1)]
    mySentence = ""
    points, seconds,minPos,words,wpm = 0, 0, 0, 0,0
    start_time = time.time()
    while True:
        elapsed_time = int(time.time() - start_time)
        minutes = elapsed_time // 60
        seconds = elapsed_time % 60

        try:
            key = screen.getkey()
            if (key == '\b' or key == ' ') and minPos == len(mySentence):
                continue
            elif key == '\b' and minPos < len(mySentence):
                mySentence = mySentence[:-1]
            elif key == ' ' and mySentence + key == sentence[:-(len(sentence) - (len(mySentence + key)))]:
                mySentence += key
                minPos = len(mySentence)
                words += 1
            else:
                mySentence += key
        except:
            key = None

        if mySentence == sentence:
            mySentence = ""
            sentence = sentences[random.randint(0, len(sentences)-1)]
            minPos = 0
            words += 1
            points += 1

        if mySentence == sentence[:-(len(sentence) - (len(mySentence)))]:
            MY_COLOR = COLOR_GREEN
        else:
            MY_COLOR = COLOR_RED
        if words != 0 and elapsed_time != 0:
            wpm = int(words/(elapsed_time/60))
        screen.clear()
        screen.addstr(0, 0, sentence)
        screen.addstr(0, 0, mySentence, MY_COLOR)
        screen.addstr(3, 0, f"Points: {points}")
        screen.addstr(3, 22, f"WPM: {wpm}")
        screen.addstr(3, 15, f"{minutes:02d}:{seconds:02d}")
        screen.move(0, len(mySentence))
        screen.refresh()

wrapper(main)