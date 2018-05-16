import unittest
from seafield import SeaField, Cell


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

    def test_set_ship(self):
        ff = SeaField(5, 5)
        # ff.set_ship(0, 2, 4, SeaField.HORIZONTAL)