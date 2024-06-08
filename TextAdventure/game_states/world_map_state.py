from game_states.base_state import BaseState, BaseSubState
from dictionaries.state_enums import WorldMapSubState

class WorldMapDefaultSubState(BaseSubState):
    def handle_input(self):
        pass

    def update(self):
        pass

    def render(self):
        pass

class WorldMapState(BaseState):
    def __init__(self, game):
        super().__init__(game, WorldMapSubState.DEFAULT)
        self.substates = {
            WorldMapSubState.DEFAULT: WorldMapDefaultSubState(game)
        }
