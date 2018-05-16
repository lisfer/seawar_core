import unittest
from seaplayground import SeaField, Cell


class SeaFieldTest(unittest.TestCase):

    def test_mark_cell(self):
        ff = SeaField(5, 5)
        ff.mark_cell(2, 2, 10)
        for row_i, row in enumerate(ff._field):
            for cell_i, cell in enumerate(row):
                if cell_i == 2 and row_i == 2:
                    self.assertEqual(cell.value, 10)
                else:
                    self.assertEqual(cell.value, Cell.EMPTY)

    def test_draw_ship(self):
        ff = SeaField(5, 5)
        ff._draw_ship(1, 2, 4, SeaField.HORIZONTAL)
        for row_i, row in enumerate(ff._field):
            for cell_i, cell in enumerate(row):
                if row_i == 2 and cell_i in [1, 2, 3, 4]:
                    self.assertEqual(cell.value, Cell.SHIP)
                else:
                    self.assertEqual(cell.value, Cell.EMPTY)