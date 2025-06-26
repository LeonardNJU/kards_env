from enum import Enum

class Nation(Enum):
    USA = "USA"
    JAPAN = "Japan"
    GERMANY = "Germany"
    SOVIET = "Soviet Union"
    UK = "United Kingdom"
    def from_str(cls, str_nation: str) :
        match str_nation.strip().upper():
            case "USA":
                return cls.USA
            case "JAPAN":
                return cls.JAPAN
            case "GERMANY":
                return cls.GERMANY
            case "SOVIET":
                return cls.SOVIET
            case "UK":
                return cls.UK
            case _:
                raise ValueError(f"Invalid nation name: {str_nation}. Must be one of {list(Nation)}.")
    
class CardType(Enum):
    INFANTRY = "Infantry"
    def from_str(cls, str_type: str) :
        match str_type.strip().upper():
            case "INFANTRY":
                return cls.INFANTRY
            case _:
                raise ValueError(f"Invalid card type: {str_type}. Must be 'Infantry'.")
    
class UnitType(Enum):
    INFANTRY = "Infantry"
    ARMOR = "Armor"
    ARTILLERY = "Artillery"
    def from_str(cls, str_type: str) :
        match str_type.strip().upper():
            case "INFANTRY":
                return cls.INFANTRY
            case "ARMOR":
                return cls.ARMOR
            case "ARTILLERY":
                return cls.ARTILLERY
            case _:
                raise ValueError(f"Invalid unit type: {str_type}. Must be one of {list(UnitType)}.")
        