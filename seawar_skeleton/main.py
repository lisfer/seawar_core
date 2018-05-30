class Cell:

    def __init__(self, x, y, value=None):
        pass


class Matrix:
    
    def cells_by_vektor(self, coord_x, coord_y, length, is_vertical=False):
        pass
    
    def borders_by_vektor(self, coord_x, coord_y, length, is_vertical=False):
        pass
    
    def ribs_for_cell(self, coord_x, coord_y):
        pass
    
    def conrers_for_cell(self, coord_x, coord_y):
        pass
    
    def vektor_by_cells(self, cells):
        pass


class Field:

    def __init__(self, max_x, max_y):
        pass
    
    def draw_ship(self, cells):
        pass
    
    def draw_border(self, cells):
        pass
    
    def is_suitable(self, cells):
        pass
    

class ShipService:

    def get_ship_by_cell(self, field, coord_x, coord_y):
        pass

    def get_ship_if_killed(self, coord_x, coord_y):
        pass

    def get_available_coord(self, coord_x, coord_y, length):
        pass

    def put_ship(self, coord_x, coord_y, length, is_vertical=False):
        pass

    def put_ship_random(self, coord_x, coord_y, length):
        pass

    def put_ships_random(self, fleet):
        pass


class TargetField:
    def select_cell(self):
        pass

    def shoot_response(self, result):
        pass

    def killed(self, ship):
        pass