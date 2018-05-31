import unittest

from seawar_skeleton.main import base_cell, Matrix, Field, ShipService, CellField


class CellTest2(unittest.TestCase):

    def test_default_value(self):
        cell_class = base_cell(values=['ship', 'empty'])()
        cell = cell_class(1, 1)
        self.assertEqual(cell.value, 'ship')

        cell_class = base_cell(values=['empty', 'ship'])()
        cell = cell_class(1, 1)
        self.assertEqual(cell.value, 'empty')

        cell_class = base_cell(values=['empty', 'ship'], default='border')()
        cell = cell_class(1, 1)
        self.assertEqual(cell.value, 'border')

        cell_class = base_cell(values=['empty', 'ship'])()
        cell = cell_class(1, 1, 'border')
        self.assertEqual(cell.value, 'border')

    def test_init_wo_data(self):
        cell_class = base_cell()()
        cell = cell_class(1, 1)
        self.assertIsNone(cell.value)

    def test_is_value(self):
        cell_class = base_cell(values=['empty', 'ship'])()
        cell = cell_class(1, 1)
        self.assertTrue(cell.is_empty)
        self.assertFalse(cell.is_ship)

        cell = cell_class(2, 2, 'ship')
        self.assertFalse(cell.is_empty)
        self.assertTrue(cell.is_ship)

    def test_mark(self):
        cell_class = base_cell(values=['empty', 'ship'])()
        cell = cell_class(1, 1)
        self.assertEqual(cell.value, 'empty')

        cell.mark_ship()
        self.assertEqual(cell.value, 'ship')


class CellSeaTest(unittest.TestCase):
    def test_shot_empty(self):
        c = CellField(2, 2)
        self.assertFalse(c.is_shooted)
        self.assertFalse(c.shoot())
        self.assertTrue(c.is_shooted)

    def test_shot_ship(self):
        c = CellField(2, 2, 'ship')
        self.assertFalse(c.is_shooted)
        self.assertTrue(c.shoot())
        self.assertTrue(c.is_shooted)


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
            {(-1, -1), (0, -1), (1, -1), (2, -1),
             (-1, 1), (0, 1), (1, 1), (2, 1),
             (-1, 0), (2, 0)}.difference(borders))

    def test_next_coord(self):
        n_coord = Matrix.next_coord(1, 1)
        for i in range(10):
            self.assertEqual(next(n_coord), (1 + i, 1))

        n_coord = Matrix.next_coord(1, 1, True, -1)
        for i in range(10):
            self.assertEqual(next(n_coord), (1, 1 - i))

    def test_vektor_by_coord_cell(self):
        self.assertEqual(
            Matrix.vektor_by_coords([(1, 1)]),
            (1, 1, 1, False))

    def test_vektor_by_coord_v(self):
        self.assertEqual(
            Matrix.vektor_by_coords([(1, 4), (1, 2), (1, 3)]),
            (1, 2, 3, True))

    def test_vektor_by_coord_h(self):
        self.assertEqual(
            Matrix.vektor_by_coords([(5, 4), (2, 4), (1, 4), (3, 4), (4, 4)]),
            (1, 4, 5, False))


class FieldTest(unittest.TestCase):

    def test_init(self):
        f = Field(5, 3)
        self.assertEqual(f.max_y, 3)
        self.assertEqual(f.max_x, 5)
        self.assertEqual(len(f.cells), 15)
        for c in f.cells:
            self.assertEqual(c.value, 'empty')

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

        self.assertTrue(f.is_suitable_ship_vektor(1, 1, 3))
        self.assertTrue(f.is_suitable_ship_vektor(1, 1, 3, True))

        self.assertFalse(f.is_suitable_ship_vektor(3, 3, 3))
        self.assertFalse(f.is_suitable_ship_vektor(3, 3, 3, True))
        self.assertFalse(f.is_suitable_ship_vektor(-1, 1, 3))
        self.assertFalse(f.is_suitable_ship_vektor(1, 11, 3, True))

    def test_is_coord_correct(self):
        f = Field(5, 5)
        self.assertTrue(f.is_correct_coord(3, 3))
        self.assertTrue(f.is_correct_coord(0, 0))
        self.assertTrue(f.is_correct_coord(4, 4))

        self.assertFalse(f.is_correct_coord(-1, 4))
        self.assertFalse(f.is_correct_coord(1, 44))
        self.assertFalse(f.is_correct_coord(1, 5))


class FilterCorrectCoord(unittest.TestCase):

    def test_wo_filter(self):
        coord = Matrix.coords_by_vektor(3, 3, 3, True)
        self.assertEqual(coord, [(3, 3), (3, 4), (3, 5)])

    def test_with_filter(self):
        field = Field(4, 4)
        coord = Matrix.coords_by_vektor(field, 3, 3, 3, True)
        self.assertEqual(coord, [(3, 3)])

    def test_filter_negative(self):
        field = Field(4, 4)
        coord = Matrix.coords_by_vektor(field, -1, 1, 3)
        self.assertEqual(coord, [(0, 1), (1, 1)])


class ShipServiceTestGetShip(unittest.TestCase):

    def test_get_ship_by_cell_h(self):
        f = Field(5, 5)
        f.get(1, 2).mark_ship()
        f.get(2, 2).mark_ship()
        f.get(3, 2).mark_ship()
        self.assertFalse(
            set(ShipService.get_ship_by_cell(f, 2, 2)).difference([(1, 2), (2, 2), (3, 2)]))

    def test_get_ship_by_cell_v(self):
        f = Field(5, 5)
        f.get(2, 1).mark_ship()
        f.get(2, 2).mark_ship()
        f.get(2, 3).mark_ship()
        self.assertFalse(
            set(ShipService.get_ship_by_cell(f, 2, 2)).difference([(2, 1), (2, 2), (2, 3)]))

    def test_get_ship_by_cell_surrounded(self):
        f = Field()
        f.get(3, 3).mark_ship()
        f.get(1, 3).mark_ship()
        f.get(3, 1).mark_ship()
        f.get(5, 3).mark_ship()
        f.get(3, 5).mark_ship()
        self.assertEqual(ShipService.get_ship_by_cell(f, 3, 3), [(3, 3)])


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
        ShipService.put_ship(f, 0, 0, 2, True)
        for cell in f.cells:
            if (cell.x, cell.y) in ((0, 0), (0, 1)):
                self.assertTrue(cell.is_ship)
            elif (cell.x, cell.y) in ((1, 0), (1, 1), (1, 2), (0, 2)):
                self.assertTrue(cell.is_border)
            else:
                self.assertTrue(cell.is_empty)

    def test_pit_ships_random(self):
        f = Field(5, 5)
        ShipService.put_ships_random(f, fleet=[5, 1])
        ships = set()
        for c in f.cells:
            if c.is_ship:
                ships.add(tuple( ShipService.get_ship_by_cell(f, c.x, c.y)))
        self.assertEqual(2, len(ships))
        self.assertEqual(sum([len(i) for i in ships]), 6)
