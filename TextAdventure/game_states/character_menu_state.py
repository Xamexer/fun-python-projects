from game_states.base_state import BaseState, BaseSubState
from dictionaries.state_enums import CharacterMenuSubState


class CharacterMenuDefaultSubState(BaseSubState):
    def handle_input(self,key):
        pass

    def update(self):
        pass

    def render(self):
        pass


class CharacterMenuStatsSubState(BaseSubState):
    def handle_input(sel,keyf):
        pass

    def update(self):
        pass

    def render(self):
        pass


class CharacterMenuMagicSubState(BaseSubState):
    def handle_input(self,key):
        pass

    def update(self):
        pass

    def render(self):
        pass


class CharacterMenuEquipmentSubState(BaseSubState):
    def handle_input(self,key):
        pass

    def update(self):
        pass

    def render(self):
        pass


class CharacterMenuInventorySubState(BaseSubState):
    def handle_input(self,key):
        pass

    def update(self):
        pass

    def render(self):
        pass


class CharacterMenuState(BaseState):
    def __init__(self, game):
        super().__init__(game, CharacterMenuSubState.DEFAULT)
        self.substates = {
            CharacterMenuSubState.STATS: CharacterMenuStatsSubState(game),
            CharacterMenuSubState.MAGIC: CharacterMenuMagicSubState(game),
            CharacterMenuSubState.EQUIPMENT: CharacterMenuEquipmentSubState(game),
            CharacterMenuSubState.INVENTORY: CharacterMenuInventorySubState(game)
        }
