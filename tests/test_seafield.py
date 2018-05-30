import unittest
from itertools import chain, starmap

from seawar_skeleton.seaplayground import SeaPlayground, Cell, IncorrectShipPosition, NoSpaceLeft, SeaField, \
    IncorrectCoordinate, ComputerPlayer, Matrix
from seawar_skeleton import SIGNALS, SEA_CELLS


class CellTest(unittest.TestCase):
    
    def test_shoot_miss(self):
        c = Cell(4, 4)
        self.assertFalse(c.is_shooted)
        self.assertFalse(c.shoot())
        self.assertTrue(c.is_shooted)
        
    def test_shoot_hit(self):
        c = Cell(4, 4, SEA_CELLS.SHIP)
        self.assertFalse(c.is_shooted)
        self.assertTrue(c.shoot())
        self.assertTrue(c.is_shooted)


class SeaFieldTest(unittest.TestCase):

    def test_has_any_alive_ship(self):
        base = SeaField(5, 5)
        base.set_ship(1, 1, 2)
        assert base.has_any_alive_ship() is True
        base.set(0, 1, Cell.HIT)
        assert base.has_any_alive_ship() is True
        base.set(1, 1, Cell.HIT)
        assert base.has_any_alive_ship() is True
        base.set(2, 1, Cell.HIT)
        assert base.has_any_alive_ship() is False


class SeaPlaygroundTest(unittest.TestCase):

    def test_create(self):
        base = SeaField()
        assert len(base._cells) == 100

    def test_set_ship(self):
        base = SeaField(5, 5)
        base.set_ship(1, 1, 3)
        ship = [(1, 1), (2, 1), (3, 1)]
        for cell in base._cells:
            if (cell.x, cell.y) in ship:
                assert cell.value == Cell.SHIP
            else:
                assert cell.value == Cell.EMPTY

    def test_set_border(self):
        base = SeaField(5, 5)
        base.set_border(1, 1, 3)
        border = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0),
                  (0, 1), (4, 1),
                  (0, 2), (1, 2), (2, 2), (3, 2), (4, 2)]
        for cell in base._cells:
            if (cell.x, cell.y) in border:
                assert cell.value == Cell.BORDER
            else:
                assert cell.value == Cell.EMPTY

    def test_set_border_edge(self):
        base = SeaField(4, 4)
        base.set_border(0, 0, 2, True)
        base.set_border(2, 3, 2)
        border = [(1, 0), (1, 1), (0, 2), (1, 2),
                  (2, 2), (3, 2), (1, 3)]
        for cell in base._cells:
            if (cell.x, cell.y) in border:
                assert cell.value == Cell.BORDER
            else:
                assert cell.value == Cell.EMPTY

    def test_put_ship(self):
        base = SeaField(5, 5)
        SeaPlayground.put_ship(base, 2, 1, 3, True)
        ship = [(2, 1), (2, 2), (2, 3)]
        border = [(1, 0), (1, 1), (1, 2), (1, 3), (1, 4),
                  (2, 0), (2, 4),
                  (3, 0), (3, 1), (3, 2), (3, 3), (3, 4)]

        for cell in base._cells:
            if (cell.x, cell.y) in ship:
                assert cell.value == Cell.SHIP
            elif (cell.x, cell.y) in border:
                assert cell.value == Cell.BORDER
            else:
                assert cell.value == Cell.EMPTY

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

    def test_incorrect_placement(self):
        base = SeaField(5, 5)
        SeaPlayground.put_ship(base, 1, 1, 3)
        with self.assertRaises(IncorrectCoordinate):
            SeaPlayground.put_ship(base, -1, 2, 2, True)
        with self.assertRaises(IncorrectShipPosition):
            SeaPlayground.put_ship(base, 0, 2, 2, True)

    def test_get_suitable_cells(self):
        base = SeaField(3, 3)
        SeaPlayground.put_ship(base, 0, 0, 1)
        assert SeaPlayground.get_suitable_cells(base, 3) == [(2, 0, True), (0, 2, False)]
        assert SeaPlayground.get_suitable_cells(base, 2) == [(2, 0, True), (2, 1, True), (0, 2, False), (1, 2, False)]

        assert SeaPlayground.get_suitable_cells(base, 1) == [(2, 0, True), (2, 0, False), (2, 1, True), (2, 1, False),
                                                             (0, 2, True), (0, 2, False), (1, 2, True), (1, 2, False),
                                                             (2, 2, True), (2, 2, False)]

    def test_put_random_ship(self):
        base = SeaField(4, 4)
        SeaPlayground._put_ship_random(base, 3)
        with self.assertRaises(NoSpaceLeft):
            SeaPlayground._put_ship_random(base, 3)
            SeaPlayground._put_ship_random(base, 3)

    def test_put_random_many(self):
        base = SeaField()
        SeaPlayground.put_ships_random(base)
        assert len([cell for cell in base._cells if cell.value == Cell.SHIP]) == 20

    def test_income_shoot(self):
        base = SeaField()
        SeaPlayground.put_ship(base, 2, 2, 3)
        assert SeaPlayground.income_shoot_to(base, 3, 0) == dict(signal=SIGNALS.MISS, cells=[(3, 0)])
        assert SeaPlayground.income_shoot_to(base, 3, 1) == dict(signal=SIGNALS.MISS, cells=[(3, 1)])
        assert SeaPlayground.income_shoot_to(base, 3, 2) == dict(signal=SIGNALS.HITTING, cells=[(3, 2)])
        assert SeaPlayground.income_shoot_to(base, 3, 3) == dict(signal=SIGNALS.MISS, cells=[(3, 3)])
        assert SeaPlayground.income_shoot_to(base, 3, 4) == dict(signal=SIGNALS.MISS, cells=[(3, 4)])

    def test_incorrect_income_shoot(self):
        base = SeaField()
        with self.assertRaises(IncorrectCoordinate):
            SeaPlayground.income_shoot_to(base, -3, 0)
        with self.assertRaises(IncorrectCoordinate):
            SeaPlayground.income_shoot_to(base, 11, 0)

    def test_target_anwer_mark_cell(self):
        base = SeaField(5, 5)
        SeaPlayground._shoot_answer_mark_cell(base, SIGNALS.MISS, [(1, 1)])
        SeaPlayground._shoot_answer_mark_cell(base, SIGNALS.HITTING, [(2, 2)])
        SeaPlayground._shoot_answer_mark_cell(base, SIGNALS.MISS, [(3, 3)])
        for cell in base._cells:
            if (cell.x, cell.y) in ((1, 1), (3, 3)):
                assert cell.value == Cell.MISSED
            elif cell.x == 2 and cell.y == 2:
                assert cell.value == Cell.HIT
            else:
                assert cell.value == Cell.EMPTY

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

    def test_is_killed_ship_alive(self):
        base = SeaField(5, 5)
        base.set(1, 2, Cell.SHIP)
        base.set(1, 3, Cell.SHIP)
        base.set(1, 4, Cell.SHIP)
        assert SeaPlayground._get_killed_ship(base, 1, 3) == []

    def test_is_killed_ship_injured(self):
        base = SeaField(5, 5)
        base.set(1, 2, Cell.HIT)
        base.set(1, 3, Cell.HIT)
        base.set(1, 4, Cell.SHIP)
        assert SeaPlayground._get_killed_ship(base, 1, 3) == []

        base.set(1, 2, Cell.HIT)
        base.set(1, 3, Cell.SHIP)
        base.set(1, 4, Cell.HIT)
        assert SeaPlayground._get_killed_ship(base, 1, 3) == []

    def test_is_killed_ship_killed(self):
        base = SeaField(5, 5)
        base.set(1, 2, Cell.HIT)
        base.set(1, 3, Cell.HIT)
        base.set(1, 4, Cell.HIT)
        assert SeaPlayground._get_killed_ship(base, 1, 3) == {(1, 2), (1, 3), (1, 4)}

    def test_find_ship_vector(self):
        assert SeaField.find_ship_vector([(1, 1), (2, 1), (3, 1)]) == (1, 1, 3, False)
        assert SeaField.find_ship_vector([(1, 0), (1, 1), (1, 2), (1, 3)]) == (1, 0, 4, True)

    def test_answer_target_mark_border(self):
        base = SeaField(5, 5)
        base.set(2, 2, Cell.MISSED)
        SeaPlayground._shoot_answer_mark_border(base, SIGNALS.KILLED, [(0, 0)])
        SeaPlayground._shoot_answer_mark_border(base, SIGNALS.HITTING, [(3, 3)])
        SeaPlayground._shoot_answer_mark_border(base, SIGNALS.MISS, [(0, 4)])
        SeaPlayground._shoot_answer_mark_border(base, SIGNALS.MISS, [(4, 0)])
        for cell in base._cells:
            if (cell.x, cell.y) in ((0, 1), (1, 0), (1, 1),
                                    (2, 4), (4, 2), (4, 4)):
                assert cell.value == Cell.BORDER
            elif cell.x == 2 and cell.y == 2:
                assert cell.value == Cell.MISSED
            else:
                assert cell.value == Cell.EMPTY

    def test_answer_target_incorrect_cell(self):
        base = SeaField(4, 4)
        with self.assertRaises(IncorrectCoordinate):
            SeaPlayground.handle_shoot_answer(base, SIGNALS.HITTING, [(-1, 0)])
        with self.assertRaises(IncorrectCoordinate):
            SeaPlayground.handle_shoot_answer(base, SIGNALS.HITTING, [(1, 11110)])
        with self.assertRaises(IncorrectCoordinate):
            SeaPlayground.handle_shoot_answer(base, SIGNALS.HITTING, [(i, i) for i in range(10)])

    def test_answet_target(self):
        base = SeaField(4, 4)
        SeaPlayground.handle_shoot_answer(base, SIGNALS.HITTING, [(0, 1)])
        SeaPlayground.handle_shoot_answer(base, SIGNALS.MISS, [(1, 1)])
        SeaPlayground.handle_shoot_answer(base, SIGNALS.MISS, [(2, 1)])
        SeaPlayground.handle_shoot_answer(base, SIGNALS.KILLED, [(3, 1)])
        for cell in base._cells:
            if cell.x in (1, 2, 3) and cell.y in (0, 2):
                assert cell.value == Cell.BORDER
            elif (cell.x, cell.y) in ((1, 1), (2, 1)):
                assert cell.value == Cell.MISSED
            elif (cell.x, cell.y) in ((0, 1), (3, 1)):
                assert cell.value == Cell.HIT
            else:
                assert cell.value == Cell.EMPTY

    def test_find_corners(self):
        base = SeaField(5, 5)
        assert set(base._find_cell_corners(3, 3)) == {(2, 2), (4, 2), (2, 4), (4, 4)}
        assert set(base._find_cell_corners(0, 0)) == {(1, 1)}


class ComputerPlayerTest(unittest.TestCase):

    def test_find_target(self):
        comp = ComputerPlayer(2, 2)
        list(starmap(comp.target_field.set, [(0, 0, 1), (0, 1, 1), (1, 0, 1)]))
        assert comp.select_target() == (1, 1)

    def test_find_target_preferred(self):
        comp = ComputerPlayer()
        comp.target_field.set(5, 5, Cell.PROBABLY_SHIP)
        for i in range(10):
            assert comp.select_target() == (5, 5)

    def test_target_answer_no_rate(self):
        comp = ComputerPlayer(4, 4)
        comp.handle_shoot_answer(SIGNALS.MISS, [(0, 0)])
        comp.handle_shoot_answer(SIGNALS.MISS, [(2, 2)])
        comp.handle_shoot_answer(SIGNALS.KILLED, [(2, 2)])
        assert len([cell for cell in comp.target_field._cells if cell.value == Cell.PROBABLY_SHIP]) == 0

    def test_target_answer_rate(self):
        comp = ComputerPlayer(5, 5)
        comp.handle_shoot_answer(SIGNALS.HITTING, [(0, 0)])
        comp.handle_shoot_answer(SIGNALS.HITTING, [(2, 2)])
        for cell in comp.target_field._cells:
            if (cell.x, cell.y) in ((0, 1), (1, 0), (2, 1), (1, 2), (3, 2), (2, 3)):
                assert cell.value is Cell.PROBABLY_SHIP
            elif (cell.x, cell.y) in ((0, 0), (2, 2)):
                assert cell.value is Cell.HIT
            elif (cell.x, cell.y) in ((1, 1), (3, 1), (1, 3), (3, 3)):
                assert cell.value is Cell.BORDER
            else:
                assert cell.value is Cell.EMPTY

    def test_target_answer_clean_rate(self):
        comp = ComputerPlayer(5, 5)
        probably_cells = lambda: [(cell.x, cell.y) for cell in comp.target_field._cells if cell.value == Cell.PROBABLY_SHIP]
        comp.handle_shoot_answer(SIGNALS.HITTING, [(2, 2)])
        assert set(probably_cells()) == {(2, 1), (2, 3), (1, 2), (3, 2)}
        comp.handle_shoot_answer(SIGNALS.KILLED, [(2, 2)])
        assert set(probably_cells()) == set()

    def test_make_shoots(self):
        enemy_field = SeaField()
        comp = ComputerPlayer()

        SeaPlayground.put_ship(enemy_field, 1, 3, 3)
        SeaPlayground.put_ship(enemy_field, 7, 7, 1)

        comp.target_field.set(0, 3, Cell.MISSED)
        comp.target_field.set(1, 2, Cell.MISSED)
        comp.target_field.set(1, 4, Cell.MISSED)
        comp.target_field.set(1, 3, Cell.PROBABLY_SHIP)

        assert SeaPlayground.make_shoot_by_computer(comp, enemy_field) == {'signal': SIGNALS.HITTING, 'cells': [(1, 3)]}
        assert SeaPlayground.make_shoot_by_computer(comp, enemy_field) == {'signal': SIGNALS.HITTING, 'cells': [(2, 3)]}
        assert SeaPlayground.make_shoot_by_computer(comp, enemy_field) == {'signal': SIGNALS.KILLED, 'cells': [(1, 3), (2, 3), (3, 3)]}

        comp.target_field.set(7, 7, Cell.PROBABLY_SHIP)
        assert SeaPlayground.make_shoot_by_computer(comp, enemy_field) == {'signal': SIGNALS.WIN, 'cells': [(7, 7)]}
