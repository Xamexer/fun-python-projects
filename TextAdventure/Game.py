import time
from enum import Enum
from dictionaries import COLORS, Color
from CursesUtilities import CursesUtilities

from Player import Player

from gameStates.MainMenuState import MainMenuState
from gameStates.WorldMapState import WorldMapState
from gameStates.CharacterMenuState import CharacterMenuState
from gameStates.BattleState import BattleState

class GameState(Enum):
    DEFAULT = 0
    MAIN_MENU = 1
    WORLD_MAP = 2
    CHARACTER_MENU = 3
    BATTLE = 4

class Game:
    def __init__(self, screen) -> None:
        self.screen = screen
        self.cUtils = CursesUtilities(screen)
        self.state = GameState.MAIN_MENU
        self.states = {
            GameState.MAIN_MENU: MainMenuState(self),
            GameState.WORLD_MAP: WorldMapState(self),
            GameState.CHARACTER_MENU: CharacterMenuState(self),
            GameState.BATTLE: BattleState(self)
        }

    def set_state(self, new_state):
        self.state = new_state

    def run(self):
        while True:
            current_state = self.states[self.state]
            current_state.handle_input()
            current_state.update()
            current_state.render()
            time.sleep(0.1)