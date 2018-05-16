import unittest
from itertools import chain

from seaplayground import SeaField, Cell, ShipCouldNotBePlaced


class SeaFieldTest(unittest.TestCase):

    def _check_cells(self, ff, conditions, default_value=Cell.EMPTY):
        for cell in chain(*ff._field):
            # print (f'{cell.x}: {cell.y} = {cell.value}', end = ' <=> ')
            for condition, value in conditions.items():
                if condition(cell):
                    # print(value)
                    self.assertEqual(cell.value, value, f'({cell.x}; {cell.y}) = {cell.value} != {value}')
                    break
            else:
                #print(default_value)
                self.assertEqual(cell.value, default_value, f'{cell.x} : {cell.y} = {cell.value} != {default_value}')

    def test_mark_cell(self):
        ff = SeaField(5, 5)
        self.assertEqual(ff.mark_cell(2, 2, 10), True)
        conditions = {lambda cell: cell.x == 2 and cell.y == 2: 10}
        self._check_cells(ff, conditions)

    def test_mark_outrange(self):
        ff = SeaField(5, 5)
        self.assertEqual(ff.mark_cell(21, 2, 10), False)
        self._check_cells(ff, dict())

    def test_draw_ship(self):
        ff = SeaField(5, 5)
        self.assertEqual(ff._draw_ship(1, 2, 4, SeaField.HORIZONTAL), True)
        conditions = {lambda cell: cell.y == 2 and cell.x in [1,2,3,4]: Cell.SHIP}
        self._check_cells(ff, conditions)

    def test_fail_draw_ship(self):
        ff = SeaField(5, 5)
        with self.assertRaises(ShipCouldNotBePlaced):
            ff._draw_ship(1, 2, 10, SeaField.HORIZONTAL)
        with self.assertRaises(ShipCouldNotBePlaced):
            ff._draw_ship(4, 2, 5, SeaField.HORIZONTAL)
        with self.assertRaises(ShipCouldNotBePlaced):
            ff._draw_ship(14, 2, 5, SeaField.HORIZONTAL)

    def test_draw_border_one_cell(self):
        ff = SeaField(5, 5)
        ff._draw_border(2, 2, 1)

        conditions = {
            lambda cell: cell.y in (1, 3) and cell.x in (1, 2, 3): Cell.BORDER,
            lambda cell: cell.y == 2 and cell.x in (1, 3): Cell.BORDER
        }
        self._check_cells(ff, conditions)

    def test_draw_several_borders_horizont(self):
        ff = SeaField(5, 5)
        ff._draw_border(1, 1, 3)
        ff._draw_border(2, 3, 3)
        conditions = {
            lambda cell: cell.y in (0, 2) and cell.x in (0, 1, 2, 3, 4): Cell.BORDER,
            lambda cell: cell.y == 1 and cell.x in (0, 4): Cell.BORDER,
            lambda cell: cell.y == 4 and cell.x in (1, 2, 3, 4): Cell.BORDER,
            lambda cell: cell.y == 3 and cell.x == 1: Cell.BORDER
        }
        self._check_cells(ff, conditions)

    def test_draw_border_vertical(self):
        ff = SeaField(5, 5)
        ff._draw_border(1, 1, 3, SeaField.VERTICAL)
        conditions = {
            lambda cell: cell.x in (0, 2) and cell.y in (0, 1, 2, 3, 4): Cell.BORDER,
            lambda cell: cell.x == 1 and cell.y in (0, 4): Cell.BORDER,
        }
        self._check_cells(ff, conditions)

    def test_set_ship_horizontal(self):
        ff = SeaField(5, 5)
        ff.set_ship(2, 2, 3)
        conditions = {
            lambda cell: cell.y in (1, 3) and cell.x in (1, 2, 3, 4): Cell.BORDER,
            lambda cell: cell.y == 2 and cell.x == 1: Cell.BORDER,
            lambda cell: cell.y == 2 and cell.x in (2, 3, 4): Cell.SHIP
        }
        self._check_cells(ff, conditions)

    def test_set_ship_vertical(self):
        ff = SeaField(5, 5)
        ff.set_ship(2, 2, 3, SeaField.VERTICAL)
        conditions = {
            lambda cell: cell.x in (1, 3) and cell.y in (1, 2, 3, 4): Cell.BORDER,
            lambda cell: cell.x == 2 and cell.y == 1: Cell.BORDER,
            lambda cell: cell.x == 2 and cell.y in (2, 3, 4): Cell.SHIP
        }
        self._check_cells(ff, conditions)

    def test_get_suitable_cells_none(self):
        ff = SeaField(5, 5)
        ff.set_ship(0, 1, 1)
        ff.set_ship(1, 3, 4)
        suitable_cells = ff.get_suitable_cells(4)
        self.assertEqual(len(suitable_cells), 0)

    def test_get_suitable_cells_success(self):
        ff = SeaField(5, 5)
        ff.set_ship(0, 1, 1)
        ff.set_ship(1, 3, 4)
        ff.pprint()
        suitable_cells = ff.get_suitable_cells(3)
        self.assertEqual(len(suitable_cells), 2)
        for cell in suitable_cells:
            self.assertTrue(cell in [(2, 0, SeaField.HORIZONTAL), (2, 1, SeaField.HORIZONTAL)])