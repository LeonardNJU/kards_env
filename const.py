from enum import Enum

class Nation(Enum):
    USA = "USA"
    SOVIET = "SOVIET"
    
class CardType(Enum):
    INFANTRY = "INFANTRY"
    INSTRUCTION= "INSTRUCTION"

class UnitType(Enum):
    INFANTRY = "INFANTRY"
    TANK = "TANK"

class DamageSource(Enum):
    DIRECT = "DIRECT"
    FATIQUE = "FATIGUE"