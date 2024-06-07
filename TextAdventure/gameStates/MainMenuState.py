from enum import Enum

class MainMenuSubState(Enum):
    DEFAULT = 0


class MainMenuState:
    def __init__(self, game):
        self.game = game
        self.substate = MainMenuSubState.DEFAULT
        self.substates = {
            MainMenuSubState.DEFAULT: MainMenuDefaultSubState(game)
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


class MainMenuDefaultSubState:
    def __init__(self, game):
        self.game = game

    def handle_input(self):
        pass

    def update(self):
        pass

    def render(self):
        pass