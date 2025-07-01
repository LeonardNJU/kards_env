from enum import Enum

class Nation(Enum):
    USA = "USA"
    JAPAN = "Japan"
    GERMANY = "Germany"
    SOVIET = "Soviet"
    UK = "UK"
    @staticmethod
    def from_str(str_nation: str) :

        
    
class CardType(Enum):
    INFANTRY = "Infantry"
    @staticmethod
    def from_str(str_type: str) :
        match str_type.strip().upper():
            case "INFANTRY":
                return CardType.INFANTRY
            case _:
                raise ValueError(f"Invalid card type: {str_type}. Must be 'Infantry'.")
    
class UnitType(Enum):
    INFANTRY = "Infantry"
    ARMOR = "Armor"
    ARTILLERY = "Artillery"
    @staticmethod
    def from_str(str_type: str) :
        match str_type.strip().upper():
            case "INFANTRY":
                return UnitType.INFANTRY
            case "ARMOR":
                return UnitType.ARMOR
            case "ARTILLERY":
                return UnitType.ARTILLERY
            case _:
                raise ValueError(f"Invalid unit type: {str_type}. Must be one of {list(UnitType)}.")
        
class UnitSpecial(Enum):
    BLITZ = "Blitz"
    