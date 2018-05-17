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
        for cell in self._generate_cells(coord_x, coord_y, ship_length, direction):
            cell.value = Cell.SHIP
        return True

    def _correct_coord(self, coord_x, coord_y):
        return 0 <= coord_y < self.max_y and 0 <= coord_x < self.max_x

    def _get_border_corners(self, coord_x, coord_y, ship_length, direction):

        if direction == SeaField.VERTICAL:
            return [(coord_x - 1, coord_y - 1, ship_length + 2, direction),
                    (coord_x + 1, coord_y - 1, ship_length + 2, direction),
                    (coord_x, coord_y - 1, 1, None),
                    (coord_x, coord_y + ship_length, 1, None)]
        else:
            return [(coord_x - 1, coord_y - 1, ship_length + 2, direction),
                    (coord_x - 1, coord_y + 1, ship_length + 2, direction),
                    (coord_x - 1, coord_y, 1, None),
                    (coord_x + ship_length, coord_y, 1, None)]

    def _draw_border(self, coord_x, coord_y, ship_length, direction=None):
        cell_generators = [
            self._generate_cells(*row, strict=False)
            for row in self._get_border_corners(coord_x, coord_y, ship_length, direction)]

        for cell in chain(*cell_generators):
            cell.value = Cell.BORDER

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
                    out.append((cell.x, cell.y, SeaField.VERTICAL))
        return out

    def _is_cell_suitable(self, cell, ship_length, direction):
        try:
            for cell in self._generate_cells(cell.x, cell.y, ship_length, direction):
                if cell.value != Cell.EMPTY:
                    return False
        except ShipCouldNotBePlaced:
            return False
        return True

    def _generate_next_coord(self, coord_x, coord_y, direction):
        if direction == SeaField.VERTICAL:
            return coord_x, coord_y + 1
        return coord_x + 1, coord_y

    def _generate_cells(self, coord_x, coord_y, ship_length, direction, strict=True):
        nx, ny = coord_x, coord_y
        for i in range(ship_length):
            if not self._correct_coord(nx, ny):
                if strict:
                    raise ShipCouldNotBePlaced()
            else:
                yield self._field[ny][nx]
            nx, ny = self._generate_next_coord(nx, ny, direction)
