from itertools import chain


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


class ShipCouldNotBePlaced(Exception):
    pass


class OutOfRange(Exception):
    pass


class SeaField:

    HORIZONTAL = 0
    VERTICAL = 1

    def __init__(self, max_x, max_y):
        self.max_x = max_x
        self.max_y = max_y
        self._field = [[Cell(x, y) for x in range(max_x)] for y in range(max_y)]

    def mark_cell(self, coord_x, coord_y, value):
        if self._correct_coord(coord_x, coord_y):
            self._field[coord_y][coord_x].value = value
            return True
        else:
            return False

    def _draw_ship(self, coord_x, coord_y, ship_length, direction=None):
        if direction is None:
            direction = SeaField.HORIZONTAL
        ship_cells = self._get_cells(coord_x, coord_y, ship_length, direction)
        for cell in ship_cells:
            cell.value = Cell.SHIP
        return True

    def _get_cells(self, coord_x, coord_y, ship_length, direction):
        cells = []
        for i in range(ship_length):
            try:
                if direction == SeaField.HORIZONTAL:
                    cells.append(self._field[coord_y][coord_x + i])
                else:
                    cells.append(self._field[coord_y + i][coord_x])
            except IndexError:
                raise ShipCouldNotBePlaced()
        return cells

    def _correct_coord(self, coord_x, coord_y):
        return 0 <= coord_y < self.max_y and 0 <= coord_x < self.max_x

    def _draw_border(self, coord_x, coord_y, ship_length, direction=None):
        if direction is None:
            direction = SeaField.HORIZONTAL
        if direction == SeaField.HORIZONTAL:
            for x in range(coord_x - 1, coord_x + ship_length + 1):
                self.mark_cell(x, coord_y - 1, Cell.BORDER)
                self.mark_cell(x, coord_y + 1, Cell.BORDER)
            self.mark_cell(coord_x - 1, coord_y, Cell.BORDER)
            self.mark_cell(coord_x + ship_length, coord_y, Cell.BORDER)
        else:
            for y in range(coord_y - 1, coord_y + ship_length + 1):
                self.mark_cell(coord_x - 1, y, Cell.BORDER)
                self.mark_cell(coord_x + 1, y, Cell.BORDER)
            self.mark_cell(coord_x, coord_y - 1, Cell.BORDER)
            self.mark_cell(coord_x, coord_y + ship_length, Cell.BORDER)

    def set_ship(self, coord_x, coord_y, ship_length, direction=None):
        self._draw_ship(coord_x, coord_y, ship_length, direction)
        self._draw_border(coord_x, coord_y, ship_length, direction)

    def pprint(self):
        print()
        for row in self._field:
            for cell in row:
                print('{0.x:5}: {0.y} == {0.value:2}'.format(cell), end='')
            print()

    def get_suitable_cells(self, ship_length):
        """
        :param ship_length:
        :return: List of tuples [(x, y, <direction>), ..] or empty list
        """
        out = []
        for cell in chain(*self._field):
            if cell.value == Cell.EMPTY:
                if self._is_cell_suitable(cell, ship_length, SeaField.HORIZONTAL):
                    out.append((cell.x, cell.y, SeaField.HORIZONTAL))
                if self._is_cell_suitable(cell, ship_length, SeaField.VERTICAL):
                    out.append((cell.x, cell.y, SeaField.HORIZONTAL))
        return out

    def _is_cell_suitable(self, cell, ship_length, direction):
        coord_x = cell.x
        coord_y = cell.y
        if direction == SeaField.HORIZONTAL:
            for i in range(ship_length):
                if not (self._correct_coord(coord_x + i, coord_y) and self._field[coord_y][coord_x + i].value == Cell.EMPTY):
                    return False
            return True
        else:
            for i in range(ship_length):
                if not (self._correct_coord(coord_x, coord_y + i) and self._field[coord_y + i][coord_x].value == Cell.EMPTY):
                    return False
            return True
