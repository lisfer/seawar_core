class Coord:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Cell(Coord):
    SHIP = 10
    EMPTY = 0

    def __init__(self, x, y):
        super(Cell, self).__init__(x, y)
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

    def _draw_ship(self, coord_x, coord_y, ship_length, direction):
        try:
            ship_cells = self._get_cells(coord_x, coord_y, ship_length, direction)
        except IndexError:
            return False
        for cell in ship_cells:
            cell.value = Cell.SHIP
        return True

    def _get_cells(self, coord_x, coord_y, ship_length, direction):
        cells = []
        for i in range(ship_length):
            if direction == SeaField.HORIZONTAL:
                cells.append(self._field[coord_y][coord_x + i])
            else:
                cells.append(self._field[coord_y + i][coord_x])
        return cells


