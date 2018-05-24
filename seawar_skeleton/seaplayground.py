from functools import partial
from itertools import chain, product
from random import choice


STANDARD_SHIP_FLEET = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]


class IncorrectCoordinate(Exception):
    pass


class IncorrectShipPosition(IncorrectCoordinate):
    pass


class NoSpaceLeft(Exception):
    pass


class Cell:

    EMPTY = 0
    BORDER = 1
    SHIP = 10
    HIT = -10
    MISSED = -1

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.value = Cell.EMPTY

    def __str__(self):
        return f'<Cell: ({self.x}; {self.y} = {self.value})>'


class SeaField:

    def __init__(self, max_x=10, max_y=10):
        self.max_x = max_x
        self.max_y = max_y
        self._field = [[Cell(i, j) for i in range(max_x)] for j in range(max_y)]
        self.cells = list(chain(*self._field))

    def __str__(self):
        out = 'Field (max_x={}; max_y={})'.format(self.max_x, self.max_y)
        for row in self._field:
            out += '\n\t'
            for cell in row:
                out += f'{cell.value:4}'
        return out + '\n'

    @staticmethod
    def next_cell(coord_x, coord_y, step, is_vertical=False):
        return coord_x + step * (not is_vertical), coord_y + step * is_vertical

    def set(self, coord_x, coord_y, value):
        self._field[coord_y][coord_x].value = value

    def get(self, coord_x, coord_y):
        return self._field[coord_y][coord_x].value

    def is_coord_correct(self, coord_x, coord_y):
        return (0 <= coord_x < self.max_x) and (0 <= coord_y < self.max_y)


class SeaPlayground:

    @staticmethod
    def _set_ship(field, coord_x, coord_y, length, is_vertical=False):
        next_cell = partial(SeaField.next_cell, coord_x, coord_y, is_vertical=is_vertical)
        [field.set(value=Cell.SHIP, *next_cell(i)) for i in range(length)]

    @staticmethod
    def _set_border(field, coord_x, coord_y, length, is_vertical=False):
        v_length, h_length = (length, 1) if is_vertical else (1, length)
        cells = []
        for i in range(v_length + 2):
            cells.append(SeaField.next_cell(coord_x - 1, coord_y - 1, i, True))
            cells.append(SeaField.next_cell(coord_x + h_length, coord_y - 1, i, True))
        for i in range(h_length):
            cells.append(SeaField.next_cell(coord_x, coord_y - 1, i, False))
            cells.append(SeaField.next_cell(coord_x, coord_y + v_length, i, False))
        [field.set(value=Cell.BORDER, *cell) for cell in cells if field.is_coord_correct(*cell)]

    @staticmethod
    def put_ship(field, coord_x, coord_y, length, is_vertical=False):
        if SeaPlayground.is_cell_suitable(field, coord_x, coord_y, length, is_vertical):
            SeaPlayground._set_ship(field, coord_x, coord_y, length, is_vertical)
            SeaPlayground._set_border(field, coord_x, coord_y, length, is_vertical)
        else:
            raise IncorrectShipPosition()

    @staticmethod
    def is_cell_suitable(field, coord_x, coord_y, length, is_vertical=False):
        next_cell = partial(SeaField.next_cell, coord_x, coord_y, is_vertical=is_vertical)
        check = lambda x, y: field.is_coord_correct(x, y) and field.get(x, y) is Cell.EMPTY
        return all([check(*next_cell(i)) for i in range(length)])

    @staticmethod
    def get_suitable_cells(field, length):
        return [(cell.x, cell.y, is_vertical)
                for cell, is_vertical in product(field.cells, (True, False))
                if SeaPlayground.is_cell_suitable(field, cell.x, cell.y, length, is_vertical)]

    @staticmethod
    def _put_ship_random(field, length):
        cells = SeaPlayground.get_suitable_cells(field, length)
        if not cells:
            raise NoSpaceLeft()
        coord_x, coord_y, is_vertical = choice(cells)
        SeaPlayground._set_ship(field, coord_x, coord_y, length, is_vertical)
        SeaPlayground._set_border(field, coord_x, coord_y, length, is_vertical)

    @staticmethod
    def put_ships_random(field, fleet:list=None):
        fleet = fleet if fleet else STANDARD_SHIP_FLEET
        for length in fleet:
            SeaPlayground._put_ship_random(field, length)

    @staticmethod
    def income_shoot(field, coord_x, coord_y):
        if field.is_coord_correct(coord_x, coord_y):
            result = Cell.HIT if field.get(coord_x, coord_y) == Cell.SHIP else Cell.MISSED
            field.set(coord_x, coord_y, result)
            return result == Cell.HIT
        raise IncorrectCoordinate(f'({coord_x}: {coord_y}) for Field({field.max_x}:{field.max_y})')
