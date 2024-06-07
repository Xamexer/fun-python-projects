class CursesUtilities:
    def __init__(self, screen):
        self.screen = screen

    def draw_line(self, start: tuple, end: tuple, char: str, color) -> None:
        y1, x1 = start
        y2, x2 = end
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        err = dx - dy

        while True:
            self.screen.addch(y1, x1, char, color)
            if x1 == x2 and y1 == y2:
                break
            e2 = err * 2
            if e2 > -dy:
                err -= dy
                x1 += sx
            if e2 < dx:
                err += dx
                y1 += sy

    def draw_box(self, start: tuple, end: tuple, char: str, color) -> None:
        y1, x1 = min(start[0], end[0]), min(start[1], end[1])
        y2, x2 = max(start[0], end[0]), max(start[1], end[1])

        for x in range(x1, x2 + 1):
            for y in range(y1, y2 + 1):
                self.screen.addch(y, x, char, color)

    def draw_border(self, start: tuple, end: tuple, char: str, color) -> None:
        y1, x1 = min(start[0], end[0]), min(start[1], end[1])
        y2, x2 = max(start[0], end[0]), max(start[1], end[1])

        for x in range(x1, x2 + 1):
            self.screen.addch(y1, x, char, color)
            self.screen.addch(y2, x, char, color)

        for y in range(y1, y2 + 1):
            self.screen.addch(y, x1, char, color)
            self.screen.addch(y, x2, char, color)