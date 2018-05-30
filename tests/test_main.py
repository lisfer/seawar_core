import unittest

from seawar_skeleton.main import get_cell_class


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
