from curses import wrapper
from dictionaries.colors import initialize_colors
from game import Game

def main(screen) -> None:
    initialize_colors()
    main_game = Game(screen)
    main_game.run()

if __name__ == "__main__":
    wrapper(main)
