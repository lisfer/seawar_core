from itertools import product, chain
from random import choice


DEFAULT_MAX_X = 10
DEFAULT_MAX_Y = 10


def get_cell_class(values, default=None):

    class Cell:

        def is_value(self, value):
            return self.value == value

        def mark_value(self, value):
            self.value = value

        def default_value(self):
            return None

        def __init__(self, x, y, value=None):
            self.x = x
            self.y = y
            self.value = value or self.default_value()

    for v in values:
        setattr(Cell, f'is_{v}', property(lambda s, v=v: s.is_value(value=v)))
        setattr(Cell, f'mark_{v}', (lambda s, v=v: s.mark_value(value=v)))
        setattr(Cell, 'default_value', (lambda s: default or values[0] or None))
    return Cell


class Matrix:

    @staticmethod
    def coords_by_vektor(coord_x, coord_y, length, is_vertical=False):
        return [(coord_x + i * (not is_vertical), coord_y + i * is_vertical)
                for i in range(length)]

    @staticmethod
    def borders_by_vektor(coord_x, coord_y, length, is_vertical=False):
        pass

    @staticmethod
    def ribs_for_coord(coord_x, coord_y):
        pass

    @staticmethod
    def conrers_for_coord(coord_x, coord_y):
        pass

    @staticmethod
    def vektor_by_coords(cells):
        pass

    @staticmethod
    def is_coord_correct(x, y, max_x, max_y):
        return (0 <= x < max_x) and (0 <= y < max_y)


class Field:

    _field: 'matrix of cells (actually list of lists of Cells)'

    def __init__(self, max_x=DEFAULT_MAX_X, max_y=DEFAULT_MAX_Y):
        self.max_x = max_x
        self.max_y = max_y
        Cell = get_cell_class(['empty', 'ship', 'border'])
        self._field = [[Cell(x, y) for x in range(max_x)] for y in range(max_y)]

    @property
    def cells(self):
        return list(chain(*self._field))

    def is_coord_correct(self, x, y):
        return Matrix.is_coord_correct(x, y, self.max_x, self.max_y)

    def get(self, x, y):
        return self._field[y][x]
    
    def draw_ship(self, coords):
        [self.get(*coord).mark_ship() for coord in coords]
    
    def draw_border(self, coords):
        [self.get(*coord).mark_border() for coord in coords]

    def is_suitable_vektor(self, coord_x, coord_y, length, is_vertical=False):
        coords = Matrix.coords_by_vektor(coord_x, coord_y, length, is_vertical)
        _check = lambda x, y: self.is_coord_correct(x, y) and self.get(x, y).is_empty
        return coords and all([_check(*coord) for coord in coords])
    

class ShipService:

    def get_ship_by_cell(self, field, coord_x, coord_y):
        pass

    def get_ship_if_killed(self, coord_x, coord_y):
        pass

    @staticmethod
    def get_available_vectors(field, length) -> 'list(tuple(x, y, length, is_vert))':
        return [(cell.x, cell.y, length, is_vertical)
                for cell, is_vertical in product(field.cells, (True, False))
                if field.is_suitable_vektor(cell.x, cell.y, length, is_vertical)]

    @staticmethod
    def put_ship(field, coord_x, coord_y, length, is_vertical=False):
        field.draw_ship(Matrix.coords_by_vektor(coord_x, coord_y, length, is_vertical))
        field.draw_border(Matrix.borders_by_vektor(coord_x, coord_y, length, is_vertical))

    @staticmethod
    def put_ship_random(field, length):
        cells = ShipService.get_available_vectors(field, length)
        ShipService.put_ship(*choice(cells))

    def put_ships_random(self, fleet):
        pass


class TargetField:
    def select_cell(self):
        pass

    def shoot_response(self, result):
        pass

    def killed(self, ship):
        pass