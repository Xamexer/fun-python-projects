import curses
from curses import wrapper
import time
import random
import winsound
import time


ALPHABET = 'abcdefghijklmnopqrstuvwxyz'

MAX_LIVES = 10
WORD_LENGTH = 4

class Game:
    def __init__(self) -> None:
        self.wordToGuess = None
        with open('.\\words.txt','r') as file:
            self.words = [line.strip() for line in file]
       
        self.lives = MAX_LIVES

        self.totalScore = 0
        self.wordGuesses = []
        self.correctCharResult = []
        self.existingCharResult = []

        self.currentWord = ""
        self.gameRunning = True
        self.gameWon = False
        winsound.PlaySound(".\\mind.wav", winsound.SND_ASYNC | winsound.SND_ALIAS )
        self.start_time = time.time()

    def initGame(self,screen) -> None:
        self.screen = screen
        self.initColors()
        self.newGame()
        self.screen.nodelay(True)
        self.mainGameLoop()

    def initColors(self) -> None:
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(1, curses.COLOR_RED, -1)
        curses.init_pair(2, 6, -1)
        curses.init_pair(3, curses.COLOR_GREEN, -1)
        self.COLOR_RED = curses.color_pair(1)
        self.COLOR_ORANGE = curses.color_pair(2)
        self.COLOR_GREEN = curses.color_pair(3)

    def mainGameLoop(self) -> None:
        while True:
            self.screen.clear()
            self.drawScreen()
            self.screen.refresh()
            try:
                key = self.screen.getkey()
                self.gameLogic(key)
            except:
                pass

            
            time.sleep(0.01)

    def newGame(self):
        self.gameWon = False
        self.gameRunning = True
        self.currentWord = ""
        self.lives = MAX_LIVES
        self.wordGuesses = []
        self.correctCharResult = []
        self.existingCharResult = []
        self.wordToGuess = self.words[random.randint(0, len(self.words)-1)]
    
    def drawScreen(self):
        for i in range(30):
            self.screen.addstr(i,0,f'#')
            self.screen.addstr(i,29,f'#')
            self.screen.addstr(3,i,f'#')
        self.screen.addstr(1,13,f'{self.currentWord}')
        for i,word in enumerate(self.wordGuesses):
            self.screen.addstr(5+2*i,10,f'{word}')
            self.screen.addstr(5+2*i,16,f'{self.correctCharResult[i]}',self.COLOR_GREEN)
            self.screen.addstr(5+2*i,18,f'{self.existingCharResult[i]}',self.COLOR_ORANGE)
        self.screen.addstr(0,2,f'LIVES: {self.lives}')
        self.screen.addstr(0, 19,f'SCORE: {self.totalScore}')
        #self.screen.addstr(0,40,f'DEBUG: {self.wordToGuess}')

        elapsed_time = int(time.time() - self.start_time)
        minutes = elapsed_time // 60
        seconds = elapsed_time % 60
        self.screen.addstr(3,21, f" {minutes:02d}:{seconds:02d} ")
        self.screen.move(1,13+len(self.currentWord))

        if not self.gameRunning:
            if self.gameWon:
                self.screen.addstr(5+MAX_LIVES*2,10,f'GAME WON !',self.COLOR_GREEN)
            else:
                self.screen.addstr(5+MAX_LIVES*2,10,f'GAME LOST !',self.COLOR_RED)
            self.screen.addstr(6+MAX_LIVES*2,3,f'"q" to continue playing')

    def evaluateWord(self):
        currentWord = [*self.currentWord]
        wordToGuess = [*self.wordToGuess]
        correctChars = 0
        existingChars = 0
        correctIndexes = []

        for index, char in enumerate(self.currentWord):
            if char == self.wordToGuess[index]:
                correctIndexes.append(index)
                
        currentWord = [char for i, char in enumerate(currentWord) if i not in correctIndexes]
        wordToGuess = [char for i, char in enumerate(wordToGuess) if i not in correctIndexes]

        correctChars = len(correctIndexes)

        for index, char in enumerate(currentWord):
            if char in wordToGuess:
                existingChars += 1
                indexToDelete = wordToGuess.index(char)
                wordToGuess.pop(indexToDelete)
        
        self.correctCharResult.append(correctChars)
        self.existingCharResult.append(existingChars)

    def gameLogic(self, key):
        if self.gameRunning:
            if key in ALPHABET and len(self.currentWord) < WORD_LENGTH:
                self.currentWord += key
            elif key == '\b' and len(self.currentWord) > 0:
                self.currentWord = self.currentWord[:-1]
            elif key == '\n' and len(self.currentWord) == WORD_LENGTH:
                self.wordGuesses.append(self.currentWord)
                
                if self.currentWord == self.wordToGuess:
                    self.gameRunning = False
                    self.gameWon = True
                    self.totalScore += 1
                    self.correctCharResult.append(WORD_LENGTH)
                    self.existingCharResult.append(0)

                else:
                    self.evaluateWord()
                    self.lives -= 1
                    self.currentWord = ""
                    if self.lives == 0:
                        self.totalScore = 0
                        self.gameRunning = False
        else:
            if key == 'q':
                self.newGame()
        return

if __name__ == '__main__':
    game = Game()
    wrapper(game.initGame)
    exit