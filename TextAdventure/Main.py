from curses import wrapper
from colors import initializeColors
from Game import Game

def main(screen) -> None:
    initializeColors()
    mainGame = Game(screen)

if __name__ == "__main__":
    wrapper(main)