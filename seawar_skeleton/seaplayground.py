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
    KILLED = -20
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

    def is_ship_cell(self, coord_x, coord_y):
        return self.get(coord_x, coord_y) in (Cell.SHIP, Cell.HIT, Cell.KILLED)


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
    def _set_border(field, coord_x, coord_y, length=None, is_vertical=False):
        if length:
            cells = SeaPlayground._find_border_cells(field, coord_x, coord_y, length, is_vertical)
        else:
            cells = SeaPlayground._find_cell_corners(coord_x, coord_y)

        [field.set(value=Cell.BORDER, *cell) for cell in cells if field.get(*cell) == Cell.EMPTY]

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
        result = Cell.HIT if field.is_ship_cell(coord_x, coord_y) else Cell.MISSED
        field.set(coord_x, coord_y, result)
        return result == Cell.HIT and SeaPlayground._is_ship_killed(field, coord_x, coord_y) and Cell.KILLED or result

    @staticmethod
    def find_target(field):
        return choice([(cell.x, cell.y) for cell in field.cells if cell.value is Cell.EMPTY])

    @staticmethod
    @check_coordinate
    def target_answer(field, coord_x, coord_y, answer=Cell.MISSED):
        shooted_cells = SeaPlayground._target_answer_mark_cell(field, coord_x, coord_y, answer)
        SeaPlayground._target_answer_mark_border(field, shooted_cells, answer)

    @staticmethod
    def _target_answer_mark_cell(field, coord_x, coord_y, answer):
        field.set(coord_x, coord_y, answer)
        if answer is Cell.KILLED:
            ship_cells = SeaPlayground._find_ship_cells(field, coord_x, coord_y)
            [field.set(value=answer, *cell) for cell in ship_cells]
        else:
            ship_cells = [(coord_x, coord_y)]
        return ship_cells

    @staticmethod
    def _target_answer_mark_border(field, shooted_cells, answer):
        if answer == Cell.KILLED:
            SeaPlayground._set_border(field, *SeaPlayground._find_ship_vector(shooted_cells))
        elif answer == Cell.HIT:
            SeaPlayground._set_border(field, *shooted_cells[0])

    @staticmethod
    def _find_ship_cells(field, coord_x, coord_y):
        out = [(coord_x, coord_y)] if field.is_ship_cell(coord_x, coord_y) else []
        for step, is_vertical in product([-1, 1], [True, False]):
            out.extend(takewhile(
                lambda cell: (field.is_coord_correct(*cell) and field.is_ship_cell(*cell)),
                field.next_cell(coord_x, coord_y, is_vertical, None, step)))
        return out

    @staticmethod
    def _is_ship_killed(field, coord_x, coord_y):
        return all([field.get(*cell) == Cell.HIT for cell in SeaPlayground._find_ship_cells(field, coord_x, coord_y)])

    @staticmethod
    def _find_ship_vector(ship_cells):
        (x1, y1), (x2, y2) = map(min, zip(*ship_cells)), map(max, zip(*ship_cells))
        length = max(x2 - x1, y2 - y1)
        is_vertical = y1 + length == y2
        return x1, y1, length + 1, is_vertical

    @staticmethod
    def _find_border_cells(field, coord_x, coord_y, length, is_vertical=False):

        v_length, h_length = (length, 1) if is_vertical else (1, length)

        cells = (list(SeaField.next_cell(coord_x - 1, coord_y - 1, True, v_length + 2)) +
                 list(SeaField.next_cell(coord_x + h_length, coord_y - 1, True, v_length + 2)) +
                 list(SeaField.next_cell(coord_x, coord_y - 1, False, h_length)) +
                 list(SeaField.next_cell(coord_x, coord_y + v_length, False, h_length)))

        return filter(lambda cell: field.is_coord_correct(*cell), cells)

    @staticmethod
    def _find_cell_corners(*coords):
        return list(map(lambda c, d: (c[0] + d[0], c[1] + d[1]), [coords] * 4, product((-1, 1), (-1, 1))))
