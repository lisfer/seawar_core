from itertools import chain, product, takewhile
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

    def __repr__(self):
        return f'<Cell: ({self.x}; {self.y} = {self.value})>'


class SeaField:

    def __init__(self, max_x=10, max_y=10):
        self.max_x = max_x
        self.max_y = max_y
        self._field = [[Cell(i, j) for i in range(max_x)] for j in range(max_y)]
        self.cells = list(chain(*self._field))

    def __repr__(self):
        out = 'Field (max_x={}; max_y={})'.format(self.max_x, self.max_y)
        for row in self._field:
            out += '\n\t'
            for cell in row:
                out += f'{cell.value:4}'
        return out + '\n'

    @staticmethod
    def next_cell(coord_x, coord_y, is_vertical=False, length=None, step=1):
        cond = (lambda l: (lambda: True) if l is None else (lambda i=iter(range(l, -1, -1)): next(i)))(length)
        while cond():
            yield (coord_x, coord_y)
            coord_x, coord_y = coord_x + step * (not is_vertical), coord_y + step * is_vertical

    def set(self, coord_x, coord_y, value):
        self._field[coord_y][coord_x].value = value

    def get(self, coord_x, coord_y):
        return self._field[coord_y][coord_x].value

    def is_coord_correct(self, coord_x, coord_y):
        return (0 <= coord_x < self.max_x) and (0 <= coord_y < self.max_y)


def check_coordinate(f):
    def decor(field, coord_x, coord_y, *args, **kwargs):
        if field.is_coord_correct(coord_x, coord_y):
            return f(field, coord_x, coord_y, *args, **kwargs)
        raise IncorrectCoordinate(f'({coord_x}: {coord_y}) for Field({field.max_x}:{field.max_y})')
    return decor


class SeaPlayground:

    @staticmethod
    def _set_ship(field, coord_x, coord_y, length, is_vertical=False):
        [field.set(value=Cell.SHIP, *cell) for cell in SeaField.next_cell(coord_x, coord_y, is_vertical, length)]

    @staticmethod
    def _set_border(field, coord_x, coord_y, length, is_vertical=False):
        v_length, h_length = (length, 1) if is_vertical else (1, length)
        cells = []

        cells.extend([cell for cell in SeaField.next_cell(coord_x - 1, coord_y - 1, True, v_length + 2)])
        cells.extend([cell for cell in SeaField.next_cell(coord_x + h_length, coord_y - 1, True, v_length + 2)])
        cells.extend([cell for cell in SeaField.next_cell(coord_x, coord_y - 1, False, h_length)])
        cells.extend([cell for cell in SeaField.next_cell(coord_x, coord_y + v_length, False, h_length)])

        [field.set(value=Cell.BORDER, *cell) for cell in cells if field.is_coord_correct(*cell)]

    @staticmethod
    @check_coordinate
    def put_ship(field, coord_x, coord_y, length, is_vertical=False):
        if SeaPlayground.is_cell_suitable(field, coord_x, coord_y, length, is_vertical):
            SeaPlayground._set_ship(field, coord_x, coord_y, length, is_vertical)
            SeaPlayground._set_border(field, coord_x, coord_y, length, is_vertical)
        else:
            raise IncorrectShipPosition()

    @staticmethod
    def is_cell_suitable(field, coord_x, coord_y, length, is_vertical=False):
        check = lambda x, y: field.is_coord_correct(x, y) and field.get(x, y) is Cell.EMPTY
        return all([check(*cell) for cell in SeaField.next_cell(coord_x, coord_y, is_vertical, length)])

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
    @check_coordinate
    def income_shoot(field, coord_x, coord_y):
        result = Cell.HIT if field.get(coord_x, coord_y) == Cell.SHIP else Cell.MISSED
        field.set(coord_x, coord_y, result)
        return result == Cell.HIT

    @staticmethod
    def find_target(field):
        return choice([(cell.x, cell.y) for cell in field.cells if cell.value is Cell.EMPTY])

    @staticmethod
    @check_coordinate
    def target_answer(field, coord_x, coord_y, hit=False):
        answer = Cell.HIT if hit else Cell.MISSED
        field.set(coord_x, coord_y, answer)

    @staticmethod
    def _find_ship(field, coord_x, coord_y):
        if field.get(coord_x, coord_y) != Cell.SHIP:
            return []
        out = [(coord_x, coord_y)]
        for step, is_vertical in product([-1, 1], [True, False]):
            out.extend(takewhile(
                lambda cell: (field.is_coord_correct(*cell) and field.get(*cell) == Cell.SHIP),
                field.next_cell(coord_x, coord_y, is_vertical, None, step)))
        return out
