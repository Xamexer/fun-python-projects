import curses
from game_states.base_state import BaseState, BaseSubState
from dictionaries.state_enums import WorldMapSubState
from dictionaries.input import input

class WorldMapDefaultSubState(BaseSubState):
    def handle_input(self, key):
        match key:
            case k if k in input['menu']:
                pass
            case k if k in input['confirm']:
                pass
            case k if k in input['back']:
                pass
            case k if k in input['down']:
                self.game.player.move(0, 1, self.game.world_map.width, self.game.world_map.height)
            case k if k in input['up']:
                self.game.player.move(0, -1, self.game.world_map.width, self.game.world_map.height)
            case k if k in input['right']:
                self.game.player.move(1, 0, self.game.world_map.width, self.game.world_map.height)
            case k if k in input['left']:
                self.game.player.move(-1, 0, self.game.world_map.width, self.game.world_map.height)

    def update(self):
        pass

    def render(self):
        max_y, max_x = self.game.screen.getmaxyx()

        self.game.screen.clear()

        visible_section = self.game.world_map.get_visible_section(
            self.game.player.coordinate_x, 
            self.game.player.coordinate_y, 
            max_x, 
            max_y
        )

        map_height = len(visible_section)
        map_width = len(visible_section[0]) if map_height > 0 else 0

        offset_y = (max_y - map_height) // 2
        offset_x = (max_x - map_width) // 2

        for y, row in enumerate(visible_section):
            for x, tile in enumerate(row):
                if 0 <= y + offset_y < max_y and 0 <= x + offset_x < max_x:
                    try:
                        self.game.screen.addstr(y + offset_y, x + offset_x, tile)
                    except curses.error:
                        pass

        center_y = min(max_y // 2, self.game.world_map.height - max_y // 2)
        center_x = min(max_x // 2, self.game.world_map.width - max_x // 2)

        if self.game.player.coordinate_y < max_y // 2:
            center_y = self.game.player.coordinate_y
        elif self.game.player.coordinate_y >= self.game.world_map.height - max_y // 2:
            center_y = max_y - (self.game.world_map.height - self.game.player.coordinate_y)

        if self.game.player.coordinate_x < max_x // 2:
            center_x = self.game.player.coordinate_x
        elif self.game.player.coordinate_x >= self.game.world_map.width - max_x // 2:
            center_x = max_x - (self.game.world_map.width - self.game.player.coordinate_x)

        if 0 <= center_y + offset_y < max_y and 0 <= center_x + offset_x < max_x:
            try:
                self.game.screen.addstr(center_y + offset_y, center_x + offset_x, self.game.player.symbol)
            except curses.error:
                pass


class WorldMapState(BaseState):
    def __init__(self, game):
        super().__init__(game, WorldMapSubState.DEFAULT)
        self.substates = {
            WorldMapSubState.DEFAULT: WorldMapDefaultSubState(game)
        }
