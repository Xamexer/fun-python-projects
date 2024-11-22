import curses
from game_states.base_state import BaseState, BaseSubState
from dictionaries.state_enums import WorldMapSubState
from dictionaries.input import input, Input
from player import Direction

class WorldMapDefaultSubState(BaseSubState):
    def handle_input(self, key):
        match key:
            case k if k in input[Input.MENU]:
                pass
            case k if k in input[Input.CONFIRM]:
                pass
            case k if k in input[Input.BACK]:
                pass
            case k if k in input[Input.DOWN]:
                self.game.player.direction = Direction.DOWN
                self.try_move(Direction.DOWN)
            case k if k in input[Input.UP]:
                self.game.player.direction = Direction.UP
                self.try_move(Direction.UP)
            case k if k in input[Input.RIGHT]:
                self.game.player.direction = Direction.RIGHT
                self.try_move(Direction.RIGHT)
            case k if k in input[Input.LEFT]:
                self.game.player.direction = Direction.LEFT
                self.try_move(Direction.LEFT)

    def try_move(self, direction_or_coords):
        direction_mapping = {
            Direction.UP: (0, -1),
            Direction.DOWN: (0, 1),
            Direction.LEFT: (-1, 0),
            Direction.RIGHT: (1, 0),
        }
        if isinstance(direction_or_coords, Direction):
            delta = direction_mapping.get(direction_or_coords)
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

        self.execute_collision_logic(new_x,new_y,x_change,y_change)



    def execute_collision_logic(self, new_x, new_y, x_change, y_change):
        # Check for tile collisions
        collidable_tile = self.game.current_map.grid[new_y][new_x]
        if collidable_tile in self.game.current_map.colliders['solid']:
            return  # Tile is solid, so no movement

        # Check for sprite collisions
        for sprite in self.game.current_map.sprites:
            if sprite.coordinate_x == new_x and sprite.coordinate_y == new_y:
                if sprite.type in self.game.current_map.colliders['solid_sprites']:
                    return  # Sprite is solid, so no movement

        # If no collisions, move the player
        self.game.player.move(x_change, y_change)


    def update(self):
        pass

    def render(self):
        max_y, max_x = self.game.screen.getmaxyx()

        self.game.screen.clear()

        # Get the visible section of the map based on the player's position and screen size
        visible_section = self.game.current_map.get_visible_section(
            self.game.player.coordinate_x, 
            self.game.player.coordinate_y, 
            max_x, 
            max_y
        )

        # Calculate offsets for centering the visible map section on the screen
        map_height = len(visible_section)
        map_width = len(visible_section[0]) if map_height > 0 else 0

        offset_y = (max_y - map_height) // 2
        offset_x = (max_x - map_width) // 2

        # Render the tiles
        for y, row in enumerate(visible_section):
            for x, tile in enumerate(row):
                if 0 <= y + offset_y < max_y and 0 <= x + offset_x < max_x:
                    try:
                        self.game.screen.addstr(y + offset_y, x + offset_x, tile.tile, tile.color)
                    except curses.error:
                        pass

        # Centering calculations for the player
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

        # Draw the player
        if 0 <= center_y + offset_y < max_y and 0 <= center_x + offset_x < max_x:
            try:
                self.game.screen.addstr(center_y + offset_y, center_x + offset_x, self.game.player.symbol, self.game.player.color)
            except curses.error:
                pass

        # Render sprites
        for sprite in self.game.current_map.sprites:
            sprite_screen_x = sprite.coordinate_x - self.game.player.coordinate_x + center_x
            sprite_screen_y = sprite.coordinate_y - self.game.player.coordinate_y + center_y

            if 0 <= sprite_screen_y + offset_y < max_y and 0 <= sprite_screen_x + offset_x < max_x:
                try:
                    self.game.screen.addstr(sprite_screen_y + offset_y, sprite_screen_x + offset_x, sprite.symbol, sprite.color)
                except curses.error:
                    pass

        # Reset cursor position to top-left corner
        self.game.screen.move(0, 0)



class WorldMapState(BaseState):
    def __init__(self, game):
        super().__init__(game, WorldMapSubState.DEFAULT)
        self.substates = {
            WorldMapSubState.DEFAULT: WorldMapDefaultSubState(game)
        }
