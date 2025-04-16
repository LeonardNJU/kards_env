from const import UnitType
from object import Object


class Unit(Object):
    def __init__(self, name:str, type:UnitType, HP:int, ATK:int, oil:int, DEF:int=0):
        super().__init__(HP)
        self.name = name
        self.ATK = ATK
        self.DEF = DEF
        self.oil = oil
        self.type = type
    def __str__(self):
        return f"{self.name}({self.ATK}/{self.HP})"