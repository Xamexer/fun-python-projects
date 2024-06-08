from game_states.base_state import BaseState, BaseSubState
from dictionaries.state_enums import WorldMapSubState
from dictionaries.input import input

class WorldMapDefaultSubState(BaseSubState):
    def handle_input(self,key):
        self.game.screen.addstr(10,10,"TEST")
        match key:
            case k if k in input['menu']:
                pass
            case k if k in input['confirm']:
                pass
            case k if k in input['back']:
                pass
            case k if k in input['up']:
                self.game.screen.addstr(20,20,"UP")
                pass
            case k if k in input['down']:
                self.game.screen.addstr(20,20,"DW")
                pass
            case k if k in input['right']:
                self.game.screen.addstr(20,20,"RG")
                pass
            case k if k in input['left']:
                self.game.screen.addstr(20,20,"LF")
                pass
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