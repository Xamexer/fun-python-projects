import time
import random
import curses
from enum import Enum
from map import Map
from utlis.curses_utilities import CursesUtilities

from dictionaries.state_enums import GameState

from player import Player

from game_states.battle_state import BattleState
from game_states.character_menu_state import CharacterMenuState
from game_states.main_menu_state import MainMenuState
from game_states.world_map_state import WorldMapState

FRAMERATE = 30

class Game:
    def __init__(self, screen, map_file=None) -> None:
        self.screen = screen
        self.c_utils = CursesUtilities(screen)
        self.screen.nodelay(True)
        self.state = GameState.WORLD_MAP

        if map_file:
            self.current_map = Map(map_file=map_file)
        else:
            default_map = Map(120, 30, 0.85, 0.13, 0.02)
            self.current_map = default_map
        self.player = Player(self.current_map.width, self.current_map.height)

        #self.cave_map = Map(400, 400, 0.90, 0.10, 0.00)

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
            try:
                key = self.screen.getkey()
                if key == curses.KEY_RESIZE:
                    self.resize()
                else:
                    current_state.handle_input(key)
            except:
                pass
            current_state.update()
            self.screen.clear()
            current_state.render()
            self.screen.refresh()
            time.sleep(1/FRAMERATE)

    def resize(self):
        self.screen.clear()
        self.screen.refresh()
        current_state = self.states[self.state]
        current_state.render()
