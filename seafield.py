
class Cell:
    EMPTY = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.value = Cell.EMPTY


class SeaField:

    HORIZONTAL = 0
    VERTICAL = 1

    def __init__(self, max_x, max_y):
        self.max_x = max_x
        self.max_y = max_y
        self._field = [[Cell(x, y) for x in range(max_x)] for y in range(max_y)]

    def mark_cell(self, coord_x, coord_y, value):
        self._field[coord_x][coord_y].value = value
