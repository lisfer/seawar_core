class CellValues:
    EMPTY = 0


class SeaField:

    def __init__(self, max_x, max_y, value=CellValues.EMPTY):
        self.max_x = max_x
        self.max_y = max_y
        self._field = [[value for x in range(max_x)] for y in range(max_y)]

    def mark_cell(self, coord_x, coord_y, value):
        self._field[coord_x][coord_y] = value
