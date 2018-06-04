# seawar_core

Core part of the game "SeaWar". 
It provides the main logic of the game: Field and Cell classes,
Services for setting ship and services for shooting them

## Intallation

It can be installed through pip:

`git+git://github.com/lisfer/seawar_core.git#egg=seawar_core`

## What is inside?

Some conceptions:
- **Vektor** - it's a name for way how lines of cells are specified. Actually, it's
a tuple of (*x*, *y*, *length*, *is_vertical*) parameters. It's used
to pass information between methods and classes inside the package.

Inside the package we have several main classes:

- **Field** - class that containes matrix (list of list of cells) 
with inforamation about ship placement
- **CellField** - cells of the **Field**. Contain some properties of the cell:
is it empty or there is a ship or a border of the ship 
(ship can not be placed close one to other. There should be an empty cell between them.
These empty cells are marked as *border*s). Is it shoted or not.
- **Matrix** - class that provides base operations with Matrix. 
It generates next coordinates for specified cell in different directions. It 
can find *border* of the cell, get cell for some *vektor* or figure out a *vektor* for several cells.
- **ShipService** - class that knows about existence of the ships. Represent methods for
setting ships on the field to specified or random positions. Has methods for
checking if the ship was killed and if there left some alive ships. Also provides
method for shooting to the field
- **TargetField** - other type of the Field (actually, child of *Field* class).
is used for keeping information about computer shoots.
- **CellTarget** - cell of *TargetField*. Differs from *CellField* with different set
of values.

## How to use it ?

You just need to call several methods:

#### Creating fields:

```python
from seawar_core import Field, ShipService, TargetField

# Creating user field
user_field = Field()
ShipService.put_ships_random(user_field)

# Creating computer field
comp_field = Field()
ShipService.put_ships_random(comp_field)

# target field - there computer will keep result of shooting. And will look for next targer
target_field = TargetField()
```

#### User shoots

```python

# select coordinated of the cell
x, y = 5, 5  
hit = ShipService.shoot_to(comp_field, x, y)  # -> bool
# check if ship is killed
killed_cells = ShipService.get_ship_if_killed(comp_field, x, y)  # -> dict(border, ship) or {}
# check if user has won:
win = ShipService.is_fleet_killed(comp_field)  # -> bool
        
print (win and 'User has won' or killed_cells and 'Ship killed' 
       or hit and 'Ship wounded' or 'Miss')
```

#### Computer shoots

```python
# select coordinated of the cell
x, y = target_field.select_cell()

# make shoot and save responce to target_field
hit = ShipService.shoot_to(user_field, x, y)  # -> bool
target_field.shoot_response(x, y, hit)

# if the ship was killed - notify target_field. It will draw a border
# to avoid shooting between ships
killed_cells = ShipService.get_ship_if_killed(user_field, x, y)  # -> dict(border, ship) or {}
if killed_cells:
    target_field.mark_killed(killed_cells['border'])
    
win = ShipService.is_fleet_killed(user_field)  # -> bool
print (win and 'Computer has won' or killed_cells and 'Ship killed' 
       or hit and 'Ship wounded' or 'Miss')
 
```
