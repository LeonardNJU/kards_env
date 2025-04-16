from enum import Enum

class Nation(Enum):
    USA = "USA"
    SOVIET = "SOVIET UNION"
    
class CardType(Enum):
    UNIT= "UNIT"
    INSTRUCTION= "INSTRUCTION"

class UnitType(Enum):
    INFANTRY = "INFANTRY"
    TANK = "TANK"