from enum import Enum

class Nation(Enum):
    USA = "USA"
    JAPAN = "Japan"
    GERMANY = "Germany"
    SOVIET = "Soviet"
    UK = "UK"
    @staticmethod
    def from_str(str_nation: str):
        try:
            return Nation[str_nation.upper()]
        except KeyError:
            raise ValueError(f"Invalid nation: {str_nation}. Must be one of {list(Nation)}.")
        
    
class CardType(Enum):
    INFANTRY = "Infantry"
    @staticmethod
    def from_str(str_type: str):
        try:
            return CardType[str_type.upper()]
        except KeyError:
            raise ValueError(f"Invalid card type: {str_type}. Must be one of {list(CardType)}.")
    
class UnitType(Enum):
    INFANTRY = "Infantry"
    ARMOR = "Armor"
    ARTILLERY = "Artillery"
    @staticmethod
    def from_str(str_type: str):
        try:
            return UnitType[str_type.upper()]
        except KeyError:
            raise ValueError(f"Invalid unit type: {str_type}. Must be one of {list(UnitType)}.")
        
class UnitSpecial(Enum):
    BLITZ = "Blitz"
    @staticmethod
    def from_str(str_type: str):
        try:
            return UnitSpecial[str_type.upper()]
        except KeyError:
            raise ValueError(f"Invalid unit special: {str_type}. Must be one of {list(UnitSpecial)}.")
    