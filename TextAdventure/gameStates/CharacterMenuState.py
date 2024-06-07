from enum import Enum

class CharacterMenuSubState(Enum):
    DEFAULT = 0
    STATS = 1
    MAGIC = 2
    EQUIPMENT = 3
    INVENTORY = 4


class CharacterMenuState:
    def __init__(self, game):
        self.game = game
        self.substate = CharacterMenuSubState.DEFAULT
        self.substates = {
            CharacterMenuSubState.STATS: CharacterMenuStatsSubState(game),
            CharacterMenuSubState.MAGIC: CharacterMenuMagicSubState(game),
            CharacterMenuSubState.EQUIPMENT: CharacterMenuEquipmentSubState(game),
            CharacterMenuSubState.INVENTORY: CharacterMenuInventorySubState(game)
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


class CharacterMenuDefaultSubState:
    def __init__(self, game):
        self.game = game

    def handle_input(self):
        pass

    def update(self):
        pass

    def render(self):
        pass

class CharacterMenuStatsSubState:
    def __init__(self, game):
        self.game = game

    def handle_input(self):
        pass

    def update(self):
        pass

    def render(self):
        pass

class CharacterMenuMagicSubState:
    def __init__(self, game):
        self.game = game

    def handle_input(self):
        pass

    def update(self):
        pass

    def render(self):
        pass

class CharacterMenuEquipmentSubState:
    def __init__(self, game):
        self.game = game

    def handle_input(self):
        pass

    def update(self):
        pass

    def render(self):
        pass

class CharacterMenuInventorySubState:
    def __init__(self, game):
        self.game = game

    def handle_input(self):
        pass

    def update(self):
        pass

    def render(self):
        pass