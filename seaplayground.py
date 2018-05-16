class Coord:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Cell(Coord):
    BORDER = 1
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

    def _draw_border(self, coord_x, coord_y, ship_length, direction=None):
        if direction is None:
            direction = SeaField.HORIZONTAL
        if direction == SeaField.HORIZONTAL:
            for x in range(coord_x - 1, coord_x + ship_length + 1):
                if 0 <= coord_y - 1 < self.max_y and 0 <= x < self.max_x:
                    self._field[coord_y - 1][x].value = Cell.BORDER
                if 0 <= coord_y + 1 < self.max_y and 0 <= x < self.max_x:
                    self._field[coord_y + 1][x].value = Cell.BORDER
            self._field[coord_y][coord_x - 1].value = Cell.BORDER
            self._field[coord_y][coord_x + ship_length].value = Cell.BORDER
        else:
            for y in range(coord_y - 1, coord_y + ship_length + 1):
                if 0 <= coord_x - 1 < self.max_x and 0 <= y < self.max_y:
                    self._field[y][coord_x - 1].value = Cell.BORDER
                if 0 <= coord_x + 1 < self.max_x and 0 <= y < self.max_y:
                    self._field[y][coord_x + 1].value = Cell.BORDER
            self._field[coord_y - 1][coord_x].value = Cell.BORDER
            self._field[coord_y + ship_length][coord_x].value = Cell.BORDER

    def pprint(self):
        for row in self._field:
            for cell in row:
                print('{0.x:5}: {0.y} == {0.value:2}'.format(cell), end='')
            print()



