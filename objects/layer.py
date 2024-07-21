from enum import auto, IntEnum


class Layer(IntEnum):
    BACKGROUND = auto()
    PLAYER = auto()
    INGREDIENT_BUN_BOTTOM = auto()
    INGREDIENT_MEAT = auto()
    INGREDIENT_CHEESE = auto()
    INGREDIENT_TOPPING = auto()
    INGREDIENT_VEGGI = auto()
    INGREDIENT_BUN_TOP = auto()
    FLOOR = auto()
    CUSTOMERS = auto()
    HAMBURGER = auto() #A hamburger that is to be made or being made
    UI = auto()