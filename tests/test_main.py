import unittest

from seawar_skeleton.main import get_cell_class, Matrix, Field, ShipService


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

    def test_coord_by_vector_decrement(self):
        self.assertEqual(
            Matrix.coords_by_vektor(1, 1, 3, True, False),
            [(1, -1), (1, 0), (1, 1)])

    def test_borders_by_vektor(self):
        borders = Matrix.borders_by_vektor(0, 0, 2)
        self.assertFalse(
            set([(-1, -1), (0, -1), (1, -1), (2, -1),
                 (-1, 1), (0, 1), (1, 1), (2, 1),
                 (-1, 0), (2, 0)]).difference(borders))

    def test_is_coord_correct(self):
        self.assertTrue(Matrix.is_coord_correct(3, 3, 5, 5))
        self.assertTrue(Matrix.is_coord_correct(0, 0, 5, 5))
        self.assertTrue(Matrix.is_coord_correct(4, 4, 5, 5))

        self.assertFalse(Matrix.is_coord_correct(-1, 4, 5, 5))
        self.assertFalse(Matrix.is_coord_correct(1, 44, 5, 5))
        self.assertFalse(Matrix.is_coord_correct(1, 5, 5, 5))


class FieldTest(unittest.TestCase):

    def test_init(self):
        f = Field(5, 3)
        self.assertEqual(f.max_y, 3)
        self.assertEqual(f.max_x, 5)
        self.assertEqual(len(f.cells), 15)
        for c in f.cells:
            self.assertEqual(c.value, 'empty')

    def test_is_coord_correct(self):
        f = Field(5, 5)
        self.assertTrue(f.is_coord_correct(0, 0))
        self.assertFalse(f.is_coord_correct(5, 0))
        self.assertFalse(f.is_coord_correct(2, -1))

    def test_get(self):
        f = Field(5, 5)
        cell = f.get(3, 3)
        self.assertEqual(cell.x, 3)
        self.assertEqual(cell.y, 3)

    def test_draw_ship(self):
        f = Field(5, 5)
        f.draw_ship([(1, 1), (1, 2)])
        for c in f.cells:
            if (c.x, c.y) in ((1, 1), (1, 2)):
                self.assertEqual(c.value, 'ship')
            else:
                self.assertEqual(c.value, 'empty')

    def test_draw_border(self):
        f = Field(5, 5)
        f.draw_border([(1, 1), (1, 2)])
        for c in f.cells:
            if (c.x, c.y) in ((1, 1), (1, 2)):
                self.assertEqual(c.value, 'border')
            else:
                self.assertEqual(c.value, 'empty')

    def test_is_suitable_vector(self):
        f = Field(5, 5)

        self.assertTrue(f.is_suitable_vektor(1, 1, 3))
        self.assertTrue(f.is_suitable_vektor(1, 1, 3, True))

        self.assertFalse(f.is_suitable_vektor(3, 3, 3))
        self.assertFalse(f.is_suitable_vektor(3, 3, 3, True))
        self.assertFalse(f.is_suitable_vektor(-1, 1, 3))
        self.assertFalse(f.is_suitable_vektor(1, 11, 3, True))


class ShipServiceTest(unittest.TestCase):
    def test_get_available_vectors(self):
        f = Field(3, 3)
        f.get(0, 0).mark_ship()
        f.get(0, 1).mark_border()
        f.get(1, 0).mark_border()
        f.get(1, 1).mark_border()

        self.assertEqual(
            ShipService.get_available_vectors(f, 3),
            [(2, 0, 3, True), (0, 2, 3, False)])
        self.assertEqual(
            ShipService.get_available_vectors(f, 2),
            [(2, 0, 2, True), (2, 1, 2, True), (0, 2, 2, False), (1, 2, 2, False)])
        self.assertEqual(
            ShipService.get_available_vectors(f, 1),
            [(2, 0, 1, True), (2, 0, 1, False), (2, 1, 1, True), (2, 1, 1, False),
             (0, 2, 1, True), (0, 2, 1, False), (1, 2, 1, True), (1, 2, 1, False),
             (2, 2, 1, True), (2, 2, 1, False)])

    def test_put_ship(self):
        f = Field(3, 3)
        ShipService.put_ship(f, 0, 0, 2)
        for cell in f.cells:
            if (cell.x, cell.y) in ((0, 0), (1, 0)):
                self.assertTrue(self.is_ship)
            if (cell.x, cell.y) in ((1, 0), (1, 1), (1, 2), (2, 1)):
                self.assertTrue(self.is_border)
            else:
                self.assertTrue(self.is_empty)
