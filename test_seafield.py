import unittest
from seafield import SeaField


class SeaFieldTest(unittest.TestCase):

    def test_mark_cell(self):
        ff = SeaField(4, 4)
        ff.mark_cell(2, 2, 10)
        for row_i, row in enumerate(ff._field):
            for cell_i, cell in enumerate(row):
                if cell_i == 2 and row_i == 2:
                    self.assertEqual(cell, 10)
                else:
                    self.assertEqual(cell, 0)