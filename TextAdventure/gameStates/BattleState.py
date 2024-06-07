from enum import Enum

class BattleSubState(Enum):
    DEFAULT = 0


class BattleState:
    def __init__(self, game):
        self.game = game
        self.substate = BattleSubState.DEFAULT
        self.substates = {
            BattleSubState.DEFAULT: BattleDefaultSubState(game)
        }
    
    def set_substate(self, new_substate):
        self.substate = new_substate
    
    def handle_input(self):
        current_substate = self.substates[self.substate]
        current_substate.handle_input()
    
    def update(self):
        current_substate = self.substates[self.substate]
        current_substate.update()
    
    def render(self):
        current_substate = self.substates[self.substate]
        current_substate.render()


class BattleDefaultSubState:
    def __init__(self, game):
        self.game = game

    def handle_input(self):
        pass

    def update(self):
        pass

    def render(self):
        pass