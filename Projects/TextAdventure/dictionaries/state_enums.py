from enum import Enum

class GameState(Enum):
    DEFAULT = 0
    MAIN_MENU = 1
    WORLD_MAP = 2
    CHARACTER_MENU = 3
    BATTLE = 4

class BattleSubState(Enum):
    DEFAULT = 0

class CharacterMenuSubState(Enum):
    DEFAULT = 0
    STATS = 1
    MAGIC = 2
    EQUIPMENT = 3
    INVENTORY = 4

class MainMenuSubState(Enum):
    DEFAULT = 0

class WorldMapSubState(Enum):
    DEFAULT = 0
