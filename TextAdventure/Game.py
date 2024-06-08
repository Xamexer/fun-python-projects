import time
from enum import Enum
from utlis.curses_utilities import CursesUtilities

from dictionaries.state_enums import GameState
from dictionaries.colors import Color, COLORS

from player import Player

from game_states.battle_state import BattleState
from game_states.character_menu_state import CharacterMenuState
from game_states.main_menu_state import MainMenuState
from game_states.world_map_state import WorldMapState



class Game:
    def __init__(self, screen) -> None:
        self.screen = screen
        self.cUtils = CursesUtilities(screen)
        self.state = GameState.MAIN_MENU
        self.player = Player()
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