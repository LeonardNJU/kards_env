from enum import Enum

class Nation(Enum):
    USA = "USA"
    SOVIET = "SOVIET"
    
class CardType(Enum):
    INFANTRY = "INFANTRY"
    TANK = "TANK"
    FIGHTER="FIGHTER"
    BOMBER="BOMBER"
    ARTILLERY="ARTILLERY"
    INSTRUCTION= "INSTRUCTION"
    TRAP="TRAP"

class UnitType(Enum):
    INFANTRY = "INFANTRY"
    TANK = "TANK"
    FIGHTER="FIGHTER"
    BOMBER="BOMBER"
    ARTILLERY="ARTILLERY"
    

class DamageSource(Enum):
    DIRECT = "DIRECT"
    FATIQUE = "FATIGUE"

class SpecialAbility(Enum):
    BLITZ="BLITZ"
    ATKWITHMOVE="ATK_WITH_MOVE"
    DOUBLEHIT="DOUBLE_HIT"
    SMOKE="SMOKE"
    GUARD="GUARD"
    SHOCK="SHOCK"