from game_states.base_state import BaseState, BaseSubState
from dictionaries.state_enums import WorldMapSubState
from dictionaries.input import input

class WorldMapDefaultSubState(BaseSubState):
    def handle_input(self,key):
        xxx = self.game.screen.getmaxyx()
        match key:
            case k if k in input['menu']:
                pass
            case k if k in input['confirm']:
                pass
            case k if k in input['back']:
                pass
            case k if k in input['down']:
                if self.game.player.coordinate_y < self.game.screen.getmaxyx()[0]-1:
                    self.game.player.move_player_y(1)
                pass
            case k if k in input['up']:
                if self.game.player.coordinate_y > 0:
                    self.game.player.move_player_y(-1)
                pass
            case k if k in input['right']:
                if self.game.player.coordinate_x < self.game.screen.getmaxyx()[1]-1:
                    self.game.player.move_player_x(1)
                pass
            case k if k in input['left']:
                if self.game.player.coordinate_x > 0:
                    self.game.player.move_player_x(-1)
                pass
        pass

    def update(self):
        pass

    def render(self):
        self.game.screen.addstr(self.game.player.coordinate_y,self.game.player.coordinate_x,f"{self.game.player.symbol}")
        pass

class WorldMapState(BaseState):
    def __init__(self, game):
        super().__init__(game, WorldMapSubState.DEFAULT)
        self.substates = {
            WorldMapSubState.DEFAULT: WorldMapDefaultSubState(game)
        }