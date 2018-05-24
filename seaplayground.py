from functools import partial
from itertools import chain


class CouldNotPlaceShip(Exception):
    pass


class Cell:

    EMPTY = 0
    BORDER = 1
    SHIP = 10

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.value = Cell.EMPTY

    def __str__(self):
        return f'<Cell: ({self.x}; {self.y} = {self.value})>'


class Field:

    def __init__(self, max_x, max_y):
        self.max_x = max_x
        self.may_y = max_y
        self._field = [[Cell(i, j) for i in range(max_x)] for j in range(max_y)]
        self._cells = list(chain(*self._field))

    def __str__(self):
        out = 'Field (max_x={}; max_y={})'.format(self.max_x, self.may_y)
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

    def is_cell_correct(self, coord_x, coord_y):
        return (0 <= coord_x < self.max_x) and (0 <= coord_y < self.may_y)


class SeaPlayground:

    def __init__(self, max_x, max_y):
        self._field = Field(max_x, max_y)

    def __str__(self):
        return '<SeaPlayground>:\n' + str(self._field)

    @property
    def cells(self):
        return self._field._cells

    def set_ship(self, coord_x, coord_y, length, is_vertical=False):
        next_cell = partial(Field.next_cell, coord_x, coord_y, is_vertical=is_vertical)
        [self._field.set(value=Cell.SHIP, *next_cell(i)) for i in range(length)]

    def set_border(self, coord_x, coord_y, length, is_vertical=False):
        v_length, h_length = (length, 1) if is_vertical else (1, length)
        cells = []
        for i in range(v_length + 2):
            cells.append(Field.next_cell(coord_x - 1, coord_y - 1, i, True))
            cells.append(Field.next_cell(coord_x + h_length, coord_y - 1, i, True))
        for i in range(h_length):
            cells.append(Field.next_cell(coord_x, coord_y - 1, i, False))
            cells.append(Field.next_cell(coord_x, coord_y + v_length, i, False))
        [self._field.set(value=Cell.BORDER, *cell) for cell in cells if self._field.is_cell_correct(*cell)]

    def put_ship(self, coord_x, coord_y, length, is_vertical=False):
        if self.is_cell_correct(coord_x, coord_y, length, is_vertical):
            self.set_ship(coord_x, coord_y, length, is_vertical)
            self.set_border(coord_x, coord_y, length, is_vertical)
        else:
            raise CouldNotPlaceShip()

    def is_cell_correct(self, coord_x, coord_y, length, is_vertical=False):
        next_cell = partial(Field.next_cell, coord_x, coord_y, is_vertical=is_vertical)
        check = lambda x, y: self._field.is_cell_correct(x, y) and self._field.get(x, y) is Cell.EMPTY
        return all([check(*next_cell(i)) for i in range(length)])
