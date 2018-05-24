import unittest
from seaplayground import SeaPlayground, Cell


class SeaFieldTest(unittest.TestCase):

    # create seafild
    # add ship to coordinates
    # add border for ship
    # find out suitable place for ship
    # generate ships on the map
    # shoot

    def test_set_ship(self):
        base = SeaPlayground(5, 5)
        base.set_ship(1, 1, 3)
        ship = [(1, 1), (2, 1), (3, 1)]
        print(base)
        for cell in base.cells:
            if (cell.x, cell.y) in ship:
                assert cell.value == Cell.SHIP
            else:
                assert cell.value == Cell.EMPTY


