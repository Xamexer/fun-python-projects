import random
from dictionaries.tiles import tiles
from dictionaries.tiles import get_tiles_and_colliders


class Map:
    def __init__(self, width=None, height=None, empty_prob=None, grass_prob=None, tree_prob=None, map_file=None):
        self.tiles, self.colliders = get_tiles_and_colliders()
        if map_file:
            self.load_map(map_file)
        else:
            self.width = width
            self.height = height
            self.grid = self.generate_map(width, height, empty_prob, grass_prob, tree_prob)
            

    def generate_map(self, width, height, empty_prob, grass_prob, tree_prob):
        return [
            [
                self.random_tile(empty_prob, grass_prob, tree_prob)
                for _ in range(width)
            ]
            for _ in range(height)
        ]

    def random_tile(self, empty_prob, grass_prob, tree_prob):
        rand = random.random()
        
        if rand < empty_prob:
            return self.tiles['air']
        elif rand < empty_prob + grass_prob:
            return self.tiles['grass']
        else:
            return self.tiles['tree']

    def load_map(self, map_file):
        with open(map_file, 'r') as f:
            lines = f.readlines()
            self.grid = [list(line.strip()) for line in lines]
            self.height = len(self.grid)
            self.width = len(max(self.grid, key=len)) if self.height > 0 else 0

    def get_visible_section(self, player_x, player_y, screen_width, screen_height):
        half_screen_width = screen_width // 2
        half_screen_height = screen_height // 2

        start_x = max(0, player_x - half_screen_width)
        end_x = min(self.width, player_x + half_screen_width + 1)
        start_y = max(0, player_y - half_screen_height)
        end_y = min(self.height, player_y + half_screen_height + 1)

        if end_x - start_x < screen_width:
            if start_x == 0:
                end_x = min(screen_width, self.width)
            elif end_x == self.width:
                start_x = max(self.width - screen_width, 0)

        if end_y - start_y < screen_height:
            if start_y == 0:
                end_y = min(screen_height, self.height)
            elif end_y == self.height:
                start_y = max(self.height - screen_height, 0)

        return [
            row[start_x:end_x]
            for row in self.grid[start_y:end_y]
        ]
