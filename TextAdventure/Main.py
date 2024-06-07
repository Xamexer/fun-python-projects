from curses import wrapper
from dictionaries.colors import initialize_colors
from Game import Game

def main(screen) -> None:
    initialize_colors()
    mainGame = Game(screen)
    mainGame.run()

if __name__ == "__main__":
    wrapper(main)