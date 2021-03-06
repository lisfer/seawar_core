from functools import partial
from itertools import product, chain, takewhile
from random import choice

DEFAULT_MAX_X = 10
DEFAULT_MAX_Y = 10
STANDART_FLEET = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]


class CoordOutOfRange(Exception):
    pass


class UnknownCellValue(Exception):
    pass


def base_cell(values=None, default=None):

    def decor(_classes=None):

        _classes = _classes and (_classes if type(_classes) is list else [_classes]) or []
        _values = values or []

        class Cell(*_classes):

            default_value = None

            def is_value(self, value):
                return self.value == value

            def mark_value(self, value):
                self.value = value

            def __init__(self, x, y, value=None):
                super(Cell, self).__init__()
                self.x = x
                self.y = y
                self.value = value or self.default_value

            def __str__(self):
                return f'[{self.x}: {self.y} => {self.value}]'

            def __setattr__(self, attr, value):
                if attr == 'value' and value and self.VALUES and (
                        value not in self.VALUES and value != self.default_value):
                    raise UnknownCellValue()
                return super(Cell, self).__setattr__(attr, value)

        setattr(Cell, 'VALUES', values)

        for v in _values:
            setattr(Cell, f'is_{v}', property(lambda s, v=v: s.is_value(value=v)))
            setattr(Cell, f'mark_{v}', (lambda s, v=v: s.mark_value(value=v)))
            setattr(Cell, 'default_value',  default or values[0] or None)
        return Cell
    return decor


@base_cell(['empty', 'ship', 'border'])
class CellField:

    def __init__(self):
        self.is_shooted = False

    def shoot(self):
        self.is_shooted = True
        return self.is_ship


@base_cell(['hit', 'border', 'miss', 'probable'], 'empty')
class CellTarget:
    @property
    def is_empty(self):
        return self.value in ('empty', 'probable')

    def mark_empty(self):
        self.mark_value('empty')


def filter_correct_coord(func):
    def decor(*args, **kwargs):
        def pop_field(args):
            for i, v in enumerate(args[:2]):
                if isinstance(v, Field):
                    return v, args[:i] + args[i + 1:]
            return None, args
        field, args = args and pop_field(args)
        if field:
            return [c for c in func(*args, **kwargs) if field.is_correct_coord(*c)]
        return func(*args, **kwargs)
    return decor


def check_coord(func):

    def decor(field, x, y, *args, **kwargs):
        if not field.is_correct_coord(x, y):
            raise CoordOutOfRange(
                f'Coordinate ({x}, {y}) is out of Field ranges: (0 => {field.max_x}, 0 => {field.max_y})')
        return func(field, x, y, *args, **kwargs)

    return decor


class Matrix:

    @staticmethod
    def next_coord(coord_x, coord_y, is_vertical=False, step=1):
        x, y = coord_x, coord_y
        while True:
            yield x, y
            x, y = x + step * (not is_vertical), y + step * is_vertical

    @staticmethod
    @filter_correct_coord
    def coords_by_vektor(coord_x, coord_y, length, is_vertical=False, incremental=True):
        _range = range(length) if incremental else range(1 - length, 1)
        return [(coord_x + i * (not is_vertical), coord_y + i * is_vertical) for i in _range]

    @classmethod
    @filter_correct_coord
    def borders_by_vektor(cls, coord_x, coord_y, length, is_vertical=False):
        v_length, h_length = (length, 1) if is_vertical else (1, length)
        return list(set(sum([
            cls.coords_by_vektor(coord_x - 1, coord_y - 1, h_length + 2, False),
            cls.coords_by_vektor(coord_x - 1, coord_y - 1, v_length + 2, True),
            cls.coords_by_vektor(coord_x + h_length, coord_y + v_length, h_length + 2, False, False),
            cls.coords_by_vektor(coord_x + h_length, coord_y + v_length, v_length + 2, True, False)], [])))

    @staticmethod
    @filter_correct_coord
    def ribs_for_coord(coord_x, coord_y):
        return map(lambda c, d: (c[0] + d[0], c[1] + d[1]), [(coord_x, coord_y)] * 4,
                   ((-1, 0), (1, 0), (0, -1), (0, 1)))

    @staticmethod
    @filter_correct_coord
    def conrers_for_coord(coord_x, coord_y):
        return map(lambda c, d: (c[0] + d[0], c[1] + d[1]), [(coord_x, coord_y)] * 4, product((-1, 1), (-1, 1)))

    @staticmethod
    def vektor_by_coords(cells):
        # noinspection PyTupleAssignmentBalance
        x1, y1, x2, y2 = *min(cells), *max(cells)
        return x1, y1, len(cells), y2 > y1


class Field:
    _field: 'matrix of cells (actually list of lists of Cells)'

    def __init__(self, max_x=DEFAULT_MAX_X, max_y=DEFAULT_MAX_Y):
        self.max_x = max_x
        self.max_y = max_y
        self._field = [[CellField(x, y) for x in range(max_x)] for y in range(max_y)]

    @property
    def cells(self):
        return list(chain(*self._field))

    def __repr__(self):
        return '<Field (max_x={}; max_y={})>'.format(self.max_x, self.max_y)

    def cell_template(self, cell):
        return f"[{' ' if cell.is_empty else '.' if cell.is_border else 'X'}]"

    def __str__(self):
        out = repr(self)
        for row in self._field:
            out += '\n\t' + ''.join([self.cell_template(c) for c in row])
        return out + '\n'

    def get(self, x, y):
        return self._field[y][x]

    @check_coord
    def set(self, x, y, value, is_shooted=False):
        cell = self.get(x, y)
        cell.value = value
        cell.is_shooted = is_shooted

    def draw_ship(self, coords):
        [self.get(*coord).mark_ship() for coord in coords]

    def draw_border(self, coords):
        [self.get(*coord).mark_border() for coord in coords]

    def is_suitable_ship_vektor(self, coord_x, coord_y, length, is_vertical=False):
        coords = Matrix.coords_by_vektor(coord_x, coord_y, length, is_vertical)
        _check = lambda x, y: self.is_correct_coord(x, y) and self.get(x, y).is_empty
        return coords and all([_check(*coord) for coord in coords])

    def is_correct_coord(self, coord_x, coord_y):
        return 0 <= coord_x < self.max_x and 0 <= coord_y < self.max_y


class ShipService:

    @staticmethod
    def get_ship_by_cell(field, coord_x, coord_y) -> 'list(coord)':
        _check = lambda c: field.is_correct_coord(*c) and field.get(*c).is_ship
        _next = partial(Matrix.next_coord, coord_x, coord_y)

        return list(set(chain.from_iterable(
            takewhile(_check, _next(is_vert, step))
            for is_vert, step in product([True, False], [-1, 1]))))

    @staticmethod
    @check_coord
    def get_ship_if_killed(field, coord_x, coord_y) -> 'dict(ship, border) or {}':
        """
        Checks if the ship on (x; y) position is killed
        :param field: <Field> object
        :param coord_x: <int>
        :param coord_y: <int>
        :return: dict with coordinated of ship cells and border cells:
            {"ship": [(x, y), ...], "border": [(x, y), ...]}
            if ship was not killed - empty dict
        """
        cells = ShipService.get_ship_by_cell(field, coord_x, coord_y)
        response = cells and all([field.get(*c).is_shooted for c in cells]) and dict(ship=cells) or {}
        if response:
            response['border'] = Matrix.borders_by_vektor(field, *Matrix.vektor_by_coords(cells))
        return response

    @staticmethod
    def get_available_vectors(field, length) -> 'list(tuple(x, y, length, is_vert))':
        return [(cell.x, cell.y, length, is_vertical)
                for cell, is_vertical in product(field.cells, (True, False))
                if field.is_suitable_ship_vektor(cell.x, cell.y, length, is_vertical)]

    @staticmethod
    def put_ship(field, coord_x, coord_y, length, is_vertical=False):
        field.draw_ship(Matrix.coords_by_vektor(field, coord_x, coord_y, length, is_vertical))
        field.draw_border(Matrix.borders_by_vektor(field, coord_x, coord_y, length, is_vertical))

    @staticmethod
    def put_ship_random(field, length):
        cells = ShipService.get_available_vectors(field, length)
        ShipService.put_ship(field, *choice(cells))

    @staticmethod
    def put_ships_random(field, fleet=None):
        """
        :param field: <Field> object where ships should be placed
        :param fleet: <list> of <int> numbers. Every number - length of the ship
        :return:
        """
        fleet = fleet or STANDART_FLEET
        for length in fleet:
            ShipService.put_ship_random(field, length)

    @staticmethod
    @check_coord
    def shoot_to(field, coord_x, coord_y):
        """
        :param field: <Field> object to which shoot should be made
        :param coord_x: <int>
        :param coord_y: <int>
        :return: <bool>
        """
        return field.get(coord_x, coord_y).shoot()

    @staticmethod
    def is_fleet_killed(field: Field) -> bool:
        """
        Checks if all field were killed
        """
        return not any(not cell.is_shooted for cell in field.cells if cell.is_ship)


class TargetField(Field):

    # noinspection PyMissingConstructor
    def __init__(self, max_x=DEFAULT_MAX_X, max_y=DEFAULT_MAX_Y):
        self.max_x = max_x
        self.max_y = max_y
        self._field = [[CellTarget(x, y) for x in range(max_x)] for y in range(max_y)]

    def cell_template(self, cell):
        return f"[{' ' if cell.is_empty else cell.value[0].upper()}]"

    def select_cell(self) -> '(x, y)':
        cells = [(c.x, c.y) for c in self.cells if c.is_probable]         # trying to find probable cells
        cells = cells or [(c.x, c.y) for c in self.cells if c.is_empty]   # if none exists - select empty cells
        return choice(cells)

    def shoot_response(self, x, y, result: bool):
        if result:
            self.get(x, y).mark_hit()
            self.mark_probably_cells(x, y)
            self.mark_improbable_cells(x, y)
        else:
            self.get(x, y).mark_miss()

    def mark_probably_cells(self, x, y):
        [self.get(*c).mark_probable() for c in Matrix.ribs_for_coord(self, x, y) if self.get(*c).is_empty]

    def mark_improbable_cells(self, x, y):
        [self.get(*c).mark_border() for c in Matrix.conrers_for_coord(self, x, y) if self.get(*c).is_empty]

    def mark_killed(self, border: 'list((x, y), ...)'):
        for x, y in border:
            cell = self.get(x, y)
            cell.is_empty and cell.mark_border()
