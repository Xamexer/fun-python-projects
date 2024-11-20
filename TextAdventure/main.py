from curses import wrapper
from dictionaries.colors import initialize_colors, Color, COLORS
from game import Game


def main(screen) -> None:
    initialize_colors()
    main_game = Game(screen) #,"D:\\Hobby\\Programmieren\\learnPython\\TextAdventure\\testMap.txt"
    main_game.run()


if __name__ == "__main__":
    wrapper(main)
