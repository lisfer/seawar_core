import unittest
from itertools import chain, starmap, takewhile

from seawar_skeleton.constants import TARGET_CELLS
from seawar_skeleton.seaplayground import SeaPlaygroundShips, SeaPlayground, SeaFieldCell, IncorrectShipPosition, \
    NoSpaceLeft, \
    SeaField, \
    IncorrectCoordinate, Matrix, SeaPlaygroundShoots, TargetField
from seawar_skeleton import SIGNALS, SEA_CELLS

# TODO: replace asserts to self.assert

class CellTest(unittest.TestCase):
    
    def test_shoot_miss(self):
        c = SeaFieldCell(4, 4)
        self.assertFalse(c.is_shooted)
        self.assertFalse(c.shoot())
        self.assertTrue(c.is_shooted)
        
    def test_shoot_hit(self):
        c = SeaFieldCell(4, 4, SEA_CELLS.SHIP)
        self.assertFalse(c.is_shooted)
        self.assertTrue(c.shoot())
        self.assertTrue(c.is_shooted)
        
        
class MatrixTest(unittest.TestCase):
    
    def test_coord_correct(self):
        m = Matrix(5, 5)
        self.assertTrue(m.is_coord_correct(0, 0))
        self.assertTrue(m.is_coord_correct(0, 4))
        self.assertTrue(m.is_coord_correct(4, 0))
        self.assertFalse(m.is_coord_correct(-1, 0))
        self.assertFalse(m.is_coord_correct(1, 5))
        
    def test_next_cell_length(self):
        cells = [cell for cell in Matrix.next_cell(1, 1, True, 3)]
        self.assertEqual(cells, [(1, 1), (1, 2), (1, 3)])
        cells = [cell for cell in Matrix.next_cell(4, 4, False, 3, -1)]
        self.assertEqual(cells, [(4, 4), (3, 4), (2, 4)])

    def test_next_cell(self):
        cell = [*takewhile(lambda c: c[0] < 4, Matrix.next_cell(2, 2, False))]
        self.assertEqual(cell, [(2, 2), (3, 2)])
        
    def test_find_ship_vector(self):
        assert Matrix.find_vector([(1, 1), (2, 1), (3, 1)]) == (1, 1, 3, False)
        assert Matrix.find_vector([(1, 0), (1, 1), (1, 2), (1, 3)]) == (1, 0, 4, True)

    def test_find_corners(self):
        m = Matrix(5, 5)
        assert set(m.find_cell_corners(3, 3)) == {(2, 2), (4, 2), (2, 4), (4, 4)}
        assert set(m.find_cell_corners(0, 0)) == {(1, 1)}


class SeaPlayGroundShipsTest(unittest.TestCase):
    
    def test_put_ship(self):
        base = SeaField(5, 5)
        SeaPlaygroundShips.put_ship(base, 2, 1, 3, True)
        ship = [(2, 1), (2, 2), (2, 3)]
        border = [(1, 0), (1, 1), (1, 2), (1, 3), (1, 4),
                  (2, 0), (2, 4),
                  (3, 0), (3, 1), (3, 2), (3, 3), (3, 4)]

        for cell in base.cells:
            if (cell.x, cell.y) in ship:
                self.assertEqual(cell.value, SEA_CELLS.SHIP)
            elif (cell.x, cell.y) in border:
                self.assertEqual(cell.value, SEA_CELLS.BORDER)
            else:
                self.assertEqual(cell.value, SEA_CELLS.EMPTY)

    def test_incorrect_placement(self):
        base = SeaField(5, 5)
        SeaPlaygroundShips.put_ship(base, 1, 1, 3)
        with self.assertRaises(IncorrectCoordinate):
            SeaPlaygroundShips.put_ship(base, -1, 2, 2, True)
        with self.assertRaises(IncorrectShipPosition):
            SeaPlaygroundShips.put_ship(base, 0, 2, 2, True)

    def test_get_suitable_cells(self):
        base = SeaField(3, 3)
        SeaPlaygroundShips.put_ship(base, 0, 0, 1)

        self.assertEqual(
            set(SeaPlaygroundShips.get_suitable_cells(base, 3)),
            {(2, 0, True), (0, 2, False)})

        self.assertEqual(
            set(SeaPlaygroundShips.get_suitable_cells(base, 2)),
            {(2, 0, True), (2, 1, True), (0, 2, False), (1, 2, False)})

        self.assertEqual(
            set(SeaPlayground.get_suitable_cells(base, 1)),
            {(2, 0, True), (2, 0, False), (2, 1, True), (2, 1, False),
             (0, 2, True), (0, 2, False), (1, 2, True), (1, 2, False),
             (2, 2, True), (2, 2, False)})

    def test_put_random_ship(self):
        base = SeaField(4, 4)
        SeaPlaygroundShips._put_ship_random(base, 3)
        with self.assertRaises(NoSpaceLeft):
            SeaPlaygroundShips._put_ship_random(base, 3)
            SeaPlaygroundShips._put_ship_random(base, 3)

    def test_put_random_many(self):
        base = SeaField()
        SeaPlaygroundShips.put_ships_random(base)
        assert len([cell for cell in base.cells if cell.value == SEA_CELLS.SHIP]) == 20


class SeaFieldTest(unittest.TestCase):

    def test_create(self):
        base = SeaField()
        assert len(base.cells) == 100

    def test_set_ship(self):
        base = SeaField(5, 5)
        base.set_ship(1, 1, 3)
        ship = [(1, 1), (2, 1), (3, 1)]
        for cell in base.cells:
            if (cell.x, cell.y) in ship:
                assert cell.value == SEA_CELLS.SHIP
            else:
                assert cell.value == SEA_CELLS.EMPTY

    def test_set_border(self):
        base = SeaField(5, 5)
        base.set_border(1, 1, 3)
        border = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0),
                  (0, 1), (4, 1),
                  (0, 2), (1, 2), (2, 2), (3, 2), (4, 2)]
        for cell in base.cells:
            if (cell.x, cell.y) in border:
                assert cell.value == SEA_CELLS.BORDER
            else:
                assert cell.value == SEA_CELLS.EMPTY

    def test_set_border_edge(self):
        base = SeaField(4, 4)
        base.set_border(0, 0, 2, True)
        base.set_border(2, 3, 2)
        border = [(1, 0), (1, 1), (0, 2), (1, 2),
                  (2, 2), (3, 2), (1, 3)]
        for cell in base.cells:
            if (cell.x, cell.y) in border:
                assert cell.value == SEA_CELLS.BORDER
            else:
                assert cell.value == SEA_CELLS.EMPTY

    def test_suitable_cell(self):
        base = SeaField(5, 5)
        assert base.is_cell_suitable(1, 1, 1)
        assert base.is_cell_suitable(1, 1, 3)
        assert base.is_cell_suitable(1, 1, 3, True)

        assert not base.is_cell_suitable(-1, 1, 1)
        assert not base.is_cell_suitable(5, 1, 1)
        assert not base.is_cell_suitable(1, 1, 11)

        SeaPlayground.put_ship(base, 1, 1, 3)

        assert not base.is_cell_suitable(0, 0, 1)
        assert not base.is_cell_suitable(0, 2, 2, True)

    def test_find_ship(self):
        base = SeaField(5, 5)
        SeaPlayground.put_ship(base, 1, 1, 3)
        assert base.find_ship_by_cells(2, 1) == {(1, 1), (2, 1), (3, 1)}

    def test_find_ship_vertical(self):
        base = SeaField(5, 5)
        SeaPlayground.put_ship(base, 1, 1, 3, True)
        assert base.find_ship_by_cells(1, 2) == {(1, 1), (1, 2), (1, 3)}

    def test_find_abcent(self):
        base = SeaField(5, 5)
        assert base.find_ship_by_cells(1, 2) == set()

    def test_has_any_alive_ship(self):
        base = SeaField(5, 5)
        base.set_ship(1, 1, 2)
        assert base.has_any_alive_ship() is True
        base.get(0, 1).shoot()
        assert base.has_any_alive_ship() is True
        base.get(1, 1).shoot()
        assert base.has_any_alive_ship() is True
        base.get(2, 1).shoot()
        assert base.has_any_alive_ship() is False


class TargetFieldTest(unittest.TestCase):

    def test_find_target(self):
        base = TargetField(2, 2)
        list(starmap(base.set, [(0, 0, 1), (0, 1, 1), (1, 0, 1)]))
        assert base.select_target() == (1, 1)

    def test_find_target_preferred(self):
        base = TargetField()
        base.set(5, 5, TARGET_CELLS.PROBABLY_SHIP)
        for i in range(10):
            assert base.select_target() == (5, 5)


class SeaPlaygroundShootTest(unittest.TestCase):

    def test_is_killed_ship_alive(self):
        base = SeaField(5, 5)
        base.set(1, 2, SEA_CELLS.SHIP)
        base.set(1, 3, SEA_CELLS.SHIP)
        base.set(1, 4, SEA_CELLS.SHIP)
        self.assertEqual(SeaPlaygroundShoots.get_killed_ship(base, 1, 3), {})

    def test_is_killed_ship_injured(self):
        base = SeaField(5, 5)
        base.set(1, 2, SEA_CELLS.SHIP)
        base.set(1, 3, SEA_CELLS.SHIP)
        base.set(1, 4, SEA_CELLS.SHIP)
        base.get(1, 2).shoot()
        base.get(1, 3).shoot()
        self.assertEqual(SeaPlayground.get_killed_ship(base, 1, 3), {})

    def test_is_killed_ship_killed(self):
        base = SeaField(5, 5)
        ship_cells = (0, 0), (0, 1), (0, 2)
        for x, y in ship_cells:
            base.set(x, y, SEA_CELLS.SHIP)
            base.get(x, y).shoot()

        resp = SeaPlayground.get_killed_ship(base, 0, 1)
        for cell in resp['ship']:
            self.assertIn((cell.x, cell.y), ((0, 0), (0, 1), (0, 2)))
        for cell in resp['border']:
            self.assertIn((cell.x, cell.y), ((1, 0), (1, 1), (1, 2), (1, 3), (0, 3)))

    def test_incorrect_income_shoot(self):
        base = SeaField()
        with self.assertRaises(IncorrectCoordinate):
            SeaPlayground.income_shoot_to(base, -3, 0)
        with self.assertRaises(IncorrectCoordinate):
            SeaPlayground.income_shoot_to(base, 11, 0)


class ComputerPlayerTest1():

    def test_target_answer_no_rate(self):
        comp = ComputerPlayer(4, 4)
        comp.handle_shoot_answer(SIGNALS.MISS, [(0, 0)])
        comp.handle_shoot_answer(SIGNALS.MISS, [(2, 2)])
        comp.handle_shoot_answer(SIGNALS.KILLED, [(2, 2)])
        assert len([cell for cell in comp.target_field._cells if cell.value == SeaFieldCell.PROBABLY_SHIP]) == 0

    def test_target_answer_rate(self):
        comp = ComputerPlayer(5, 5)
        comp.handle_shoot_answer(SIGNALS.HITTING, [(0, 0)])
        comp.handle_shoot_answer(SIGNALS.HITTING, [(2, 2)])
        for cell in comp.target_field._cells:
            if (cell.x, cell.y) in ((0, 1), (1, 0), (2, 1), (1, 2), (3, 2), (2, 3)):
                assert cell.value is SeaFieldCell.PROBABLY_SHIP
            elif (cell.x, cell.y) in ((0, 0), (2, 2)):
                assert cell.value is SeaFieldCell.HIT
            elif (cell.x, cell.y) in ((1, 1), (3, 1), (1, 3), (3, 3)):
                assert cell.value is SeaFieldCell.BORDER
            else:
                assert cell.value is SeaFieldCell.EMPTY

    def test_target_answer_clean_rate(self):
        comp = ComputerPlayer(5, 5)
        probably_cells = lambda: [(cell.x, cell.y) for cell in comp.target_field._cells if cell.value == SeaFieldCell.PROBABLY_SHIP]
        comp.handle_shoot_answer(SIGNALS.HITTING, [(2, 2)])
        assert set(probably_cells()) == {(2, 1), (2, 3), (1, 2), (3, 2)}
        comp.handle_shoot_answer(SIGNALS.KILLED, [(2, 2)])
        assert set(probably_cells()) == set()

    def test_make_shoots(self):
        enemy_field = SeaField()
        comp = ComputerPlayer()

        SeaPlayground.put_ship(enemy_field, 1, 3, 3)
        SeaPlayground.put_ship(enemy_field, 7, 7, 1)

        comp.target_field.set(0, 3, SeaFieldCell.MISSED)
        comp.target_field.set(1, 2, SeaFieldCell.MISSED)
        comp.target_field.set(1, 4, SeaFieldCell.MISSED)
        comp.target_field.set(1, 3, SeaFieldCell.PROBABLY_SHIP)

        assert SeaPlayground.make_shoot_by_computer(comp, enemy_field) == {'signal': SIGNALS.HITTING, 'cells': [(1, 3)]}
        assert SeaPlayground.make_shoot_by_computer(comp, enemy_field) == {'signal': SIGNALS.HITTING, 'cells': [(2, 3)]}
        assert SeaPlayground.make_shoot_by_computer(comp, enemy_field) == {'signal': SIGNALS.KILLED, 'cells': [(1, 3), (2, 3), (3, 3)]}

        comp.target_field.set(7, 7, SeaFieldCell.PROBABLY_SHIP)
        assert SeaPlayground.make_shoot_by_computer(comp, enemy_field) == {'signal': SIGNALS.WIN, 'cells': [(7, 7)]}
