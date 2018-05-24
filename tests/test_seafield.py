import unittest

from seawar_skeleton.seaplayground import SeaPlayground, Cell, IncorrectShipPosition, NoSpaceLeft


class SeaFieldTest(unittest.TestCase):

    def test_set_ship(self):
        base = SeaPlayground(5, 5)
        base.set_ship(1, 1, 3)
        ship = [(1, 1), (2, 1), (3, 1)]
        for cell in base.cells:
            if (cell.x, cell.y) in ship:
                assert cell.value == Cell.SHIP
            else:
                assert cell.value == Cell.EMPTY

    def test_set_border(self):
        base = SeaPlayground(5, 5)
        base.set_border(1, 1, 3)
        border = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0),
                  (0, 1), (4, 1),
                  (0, 2), (1, 2), (2, 2), (3, 2), (4, 2)]
        for cell in base.cells:
            if (cell.x, cell.y) in border:
                assert cell.value == Cell.BORDER
            else:
                assert cell.value == Cell.EMPTY

    def test_set_border_edge(self):
        base = SeaPlayground(4, 4)
        base.set_border(0, 0, 2, True)
        base.set_border(2, 3, 2)
        border = [(1, 0), (1, 1), (0, 2), (1, 2),
                  (2, 2), (3, 2), (1, 3)]
        for cell in base.cells:
            if (cell.x, cell.y) in border:
                assert cell.value == Cell.BORDER
            else:
                assert cell.value == Cell.EMPTY

    def test_put_ship(self):
        base = SeaPlayground(5, 5)
        base.put_ship(2, 1, 3, True)
        ship = [(2, 1), (2, 2), (2, 3)]
        border = [(1, 0), (1, 1), (1, 2), (1, 3), (1, 4),
                  (2, 0), (2, 4),
                  (3, 0), (3, 1), (3, 2), (3, 3), (3, 4)]

        for cell in base.cells:
            if (cell.x, cell.y) in ship:
                assert cell.value == Cell.SHIP
            elif (cell.x, cell.y) in border:
                assert cell.value == Cell.BORDER
            else:
                assert cell.value == Cell.EMPTY

    def test_suitable_cell(self):
        base = SeaPlayground(5, 5)
        assert base.is_cell_correct(1, 1, 1)
        assert base.is_cell_correct(1, 1, 3)
        assert base.is_cell_correct(1, 1, 3, True)

        assert not base.is_cell_correct(-1, 1, 1)
        assert not base.is_cell_correct(5, 1, 1)
        assert not base.is_cell_correct(1, 1, 11)

        base.put_ship(1, 1, 3)

        assert not base.is_cell_correct(0, 0, 1)
        assert not base.is_cell_correct(0, 2, 2, True)

    def test_incorrect_placement(self):
        base = SeaPlayground(5, 5)
        base.put_ship(1, 1, 3)
        with self.assertRaises(IncorrectShipPosition):
            base.put_ship(0, 2, 2, True)

    def test_get_suitable_cells(self):
        base = SeaPlayground(3, 3)
        base.put_ship(0, 0, 1)
        assert base.get_suitable_cells(3) == [(2, 0, True), (0, 2, False)]
        assert base.get_suitable_cells(2) == [(2, 0, True), (2, 1, True), (0, 2, False), (1, 2, False)]

        assert base.get_suitable_cells(1) == [(2, 0, True), (2, 0, False), (2, 1, True), (2, 1, False),
                                              (0, 2, True), (0, 2, False), (1, 2, True), (1, 2, False),
                                              (2, 2, True), (2, 2, False)]

    def test_put_random_ship(self):
        base = SeaPlayground(4, 4)
        base.put_ship_random(3)
        with self.assertRaises(NoSpaceLeft):
            base.put_ship_random(3)
            base.put_ship_random(3)
