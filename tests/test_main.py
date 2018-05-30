import unittest

from seawar_skeleton.main import get_cell_class, Matrix


class CellTest(unittest.TestCase):

    def test_default_value(self):
        cell_class = get_cell_class(['ship', 'empty'])
        cell = cell_class(1, 1)
        self.assertEqual(cell.value, 'ship')

        cell_class = get_cell_class(['empty', 'ship'])
        cell = cell_class(1, 1)
        self.assertEqual(cell.value, 'empty')

        cell_class = get_cell_class(['empty', 'ship'], 'border')
        cell = cell_class(1, 1)
        self.assertEqual(cell.value, 'border')

        cell_class = get_cell_class(['empty', 'ship'])
        cell = cell_class(1, 1, 'border')
        self.assertEqual(cell.value, 'border')

    def test_init_wo_data(self):
        cell_class = get_cell_class([])
        cell = cell_class(1, 1)
        self.assertIsNone(cell.value)

    def test_is_value(self):
        cell_class = get_cell_class(['empty', 'ship'])
        cell = cell_class(1, 1)
        self.assertTrue(cell.is_empty)
        self.assertFalse(cell.is_ship)

        cell = cell_class(2, 2, 'ship')
        self.assertFalse(cell.is_empty)
        self.assertTrue(cell.is_ship)

    def test_mark(self):
        cell_class = get_cell_class(['empty', 'ship'])
        cell = cell_class(1, 1)
        self.assertEqual(cell.value, 'empty')

        cell.mark_ship()
        self.assertEqual(cell.value, 'ship')


class MatrixTest(unittest.TestCase):

    def test_coord_by_vektor_hor(self):
        self.assertEqual(
            Matrix.coords_by_vektor(1, 1, 3),
            [(1, 1), (2, 1), (3, 1)])

    def test_coord_by_vektor_ver(self):
        self.assertEqual(
            Matrix.coords_by_vektor(1, 1, 3, True),
            [(1, 1), (1, 2), (1, 3)])

    def test_is_coord_correct(self):
        self.assertTrue(Matrix.is_coord_correct(3, 3, 5, 5))
        self.assertTrue(Matrix.is_coord_correct(0, 0, 5, 5))
        self.assertTrue(Matrix.is_coord_correct(4, 4, 5, 5))

        self.assertFalse(Matrix.is_coord_correct(-1, 4, 5, 5))
        self.assertFalse(Matrix.is_coord_correct(1, 44, 5, 5))
        self.assertFalse(Matrix.is_coord_correct(1, 5, 5, 5))


class FieldTest(unittest.TestCase):
    pass