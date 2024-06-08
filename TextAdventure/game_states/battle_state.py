from game_states.base_state import BaseState, BaseSubState
from dictionaries.state_enums import BattleSubState

class BattleDefaultSubState(BaseSubState):
    def handle_input(self):
        pass

    def update(self):
        pass

    def render(self):
        pass

class BattleState(BaseState):
    def __init__(self, game):
        super().__init__(game, BattleSubState.DEFAULT)
        self.substates = {
            BattleSubState.DEFAULT: BattleDefaultSubState(game)
        }
