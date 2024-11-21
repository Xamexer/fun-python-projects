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
                self.try_to_move("down")
            case k if k in input['up']:
                self.try_to_move("up")
            case k if k in input['right']:
                self.try_to_move("right")
            case k if k in input['left']:
                self.try_to_move("left")

    def try_to_move(self, direction_or_coords):
        direction_mapping = {
            "up": (0, -1),
            "down": (0, 1),
            "left": (-1, 0),
            "right": (1, 0),
        }

        if isinstance(direction_or_coords, str):
            delta = direction_mapping.get(direction_or_coords.lower())
            if not delta:
                raise ValueError(f"Invalid direction: {direction_or_coords}")
        elif isinstance(direction_or_coords, (tuple, list)) and len(direction_or_coords) == 2:  # Handle coordinates
            delta = direction_or_coords
        else:
            raise ValueError("Invalid input; must be a direction string or a tuple of (x_change, y_change)")
        x_change, y_change = delta

        new_x = self.game.player.coordinate_x + x_change
        new_y = self.game.player.coordinate_y + y_change
        # boundries
        if not (0 <= new_x < self.game.current_map.width and 0 <= new_y < self.game.current_map.height):
            return
        
        collidable_object = self.game.current_map.grid[new_y][new_x]
        next_collidable_object = self.game.current_map.grid[new_y + y_change][new_x + x_change]
        
        match self.collide_logic(self.game.player ,collidable_object, next_collidable_object):
            case 'stay':
                pass
            case 'move':
                self.game.player.move(x_change, y_change)
            case 'push' :
                self.game.current_map.grid[new_y + y_change][new_x + x_change] = collidable_object
                self.game.current_map.grid[new_y][new_x] = self.game.current_map.tiles['air']
                self.game.player.move(x_change, y_change)
            case 'fight':
                pass
            
    def collide_logic(self, player, collidable_object, next_collidable_object):
        match collidable_object:
            case obj if ((obj in self.game.current_map.colliders['solid']) or (obj in self.game.current_map.colliders['moveable'] and next_collidable_object not in self.game.current_map.colliders['walkable'])):
                return 'stay'
            case obj if obj in self.game.current_map.colliders['moveable'] and next_collidable_object in self.game.current_map.colliders['walkable']:
                return 'push'
            case _:
                return 'move'

    def update(self):
        pass

    def render(self):
        max_y, max_x = self.game.screen.getmaxyx()

        self.game.screen.clear()

        visible_section = self.game.current_map.get_visible_section(
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
                        self.game.screen.addstr(y + offset_y, x + offset_x, tile.tile, tile.color)
                    except curses.error:
                        pass

        center_y = min(max_y // 2, self.game.current_map.height - max_y // 2)
        center_x = min(max_x // 2, self.game.current_map.width - max_x // 2)

        if self.game.player.coordinate_y < max_y // 2:
            center_y = self.game.player.coordinate_y
        elif self.game.player.coordinate_y >= self.game.current_map.height - max_y // 2:
            center_y = max_y - (self.game.current_map.height - self.game.player.coordinate_y)

        if self.game.player.coordinate_x < max_x // 2:
            center_x = self.game.player.coordinate_x
        elif self.game.player.coordinate_x >= self.game.current_map.width - max_x // 2:
            center_x = max_x - (self.game.current_map.width - self.game.player.coordinate_x)

        if 0 <= center_y + offset_y < max_y and 0 <= center_x + offset_x < max_x:
            try:
                self.game.screen.addstr(center_y + offset_y, center_x + offset_x, self.game.player.symbol, self.game.player.color)
                self.game.screen.move(0,0)
            except curses.error:
                pass


class WorldMapState(BaseState):
    def __init__(self, game):
        super().__init__(game, WorldMapSubState.DEFAULT)
        self.substates = {
            WorldMapSubState.DEFAULT: WorldMapDefaultSubState(game)
        }
