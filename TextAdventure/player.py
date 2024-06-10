class Player:
    def __init__(self, map_width, map_height):
        self.symbol = "o"
        self.name = "z"
        self.coordinate_x = map_width // 2
        self.coordinate_y = map_height // 2

    def move(self, x_change, y_change, map_width, map_height) -> None:
        new_x = self.coordinate_x + x_change
        new_y = self.coordinate_y + y_change

        # Move within the map boundaries
        if 0 <= new_x < map_width:
            self.coordinate_x = new_x

        if 0 <= new_y < map_height:
            self.coordinate_y = new_y
