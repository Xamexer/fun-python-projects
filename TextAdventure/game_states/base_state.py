class BaseSubState:
    def __init__(self, game):
        self.game = game

    def handle_input(self,key):
        pass

    def update(self):
        pass

    def render(self):
        pass

class BaseState:
    def __init__(self, game, default_substate):
        self.game = game
        self.substate = default_substate
        self.substates = {}
    
    def set_substate(self, new_substate):
        self.substate = new_substate
    
    def handle_input(self,key):
        current_substate = self.substates[self.substate]
        current_substate.handle_input(key)
    
    def update(self):
        current_substate = self.substates[self.substate]
        current_substate.update()
    
    def render(self):
        current_substate = self.substates[self.substate]
        current_substate.render()
