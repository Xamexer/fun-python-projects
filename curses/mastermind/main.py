import curses
from curses import wrapper
import time
import random

MAX_LIVES = 5
ALPHABET = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

class Game:
    def __init__(self) -> None:
        self.wordToGuess = None
        with open('.\\words.txt','r') as file:
            self.words = [line.strip() for line in file]
        self.lives = MAX_LIVES

    def initializeGame(self,screen):
        self.screen = screen
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
        self.COLOR_RED = curses.color_pair(1)
        self.COLOR_YELLOW = curses.color_pair(2)
        self.COLOR_GREEN = curses.color_pair(3)

        self.mainGameLoop()


    def mainGameLoop(self) -> None:
        self.drawScreen()
        self.screen.refresh()
        while True:
            key = self.screen.getkey()
            if key in ALPHABET:
                self.enterKey(key)
            self.screen.clear()
            self.drawScreen()
            self.screen.refresh()
            time.sleep(0.01)

    def newGame(self):
        self.wordToGuess= self.words[random.randint(0, len(self.words)-1)]
    
    def drawScreen(self):
        self.screen.addstr(10,10,f'TEST')
            
    def enterKey(self):
        pass

if __name__ == '__main__':
    game = Game()
    wrapper(game.initializeGame)