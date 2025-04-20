from const import Nation, SpecialAbility, UnitType
from units.unit import Unit


class Unit_15th_CAVALRY(Unit):
    """
    习致野骑兵
    """
    def __init__(self, HP: int=1, attack: int=2, oil=0, defense: int=0):
        super().__init__("习致野",
                         UnitType.INFANTRY,
                         Nation.JAPAN, 
                         HP, 
                         attack, 
                         oil, 
                         defense,
                         [SpecialAbility.BLITZ])

