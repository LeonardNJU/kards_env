from const import Nation, SpecialAbility, UnitType
from units.unit import Unit


class Unit_light_Infantry(Unit):
    """
    Light infantry unit class.
    """

    def __init__(self, HP: int=1, attack: int=1,oil=0, defense: int=0):
        super().__init__("轻步兵", 
                         UnitType.INFANTRY, 
                         Nation.SOVIET,
                         HP, 
                         attack, 
                         oil, 
                         defense,
                         [])
