from collections import namedtuple


def create_constant(name:str, values:list) -> namedtuple:
    return namedtuple(name, values)(*[i.lower() for i in values])


SIGNALS = create_constant('SIGNALS', ['WIN', 'KILLED', 'HIT', 'MISS'])
SEA_CELLS = create_constant('SEA_CELLS', ['EMPTY', 'BORDER', 'SHIP'])
TARGET_CELLS = create_constant('TARGET_CELLS', ['EMPTY', 'MISS', 'HIT', 'BORDER', 'PROBABLY_SHIP'])



STANDARD_SHIP_FLEET = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
DEFAULT_MAX_X = 10
DEFAULT_MAX_Y = 10