from enum import Enum

class WorldMapSubState(Enum):
    DEFAULT = 0


class WorldMapState:
    def __init__(self, game):
        self.game = game
        self.substate = WorldMapSubState.DEFAULT
        self.substates = {
            WorldMapSubState.DEFAULT: WorldMapDefaultSubState(game)
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


class WorldMapDefaultSubState:
    def __init__(self, game):
        self.game = game

    def handle_input(self):
        pass

    def update(self):
        pass

    def render(self):
        pass