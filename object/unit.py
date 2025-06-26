from dataclasses import dataclass, field
from typing import Any, Dict, List

from object.object import Object
from utils.symbols import Nation, UnitType


@dataclass
class Unit(Object):
    name: str
    nation: Nation
    type: UnitType
    HP: int
    attack: int
    oil: int

    sp: List[str] = field(default_factory=list)
    abilities: Dict[str, Any] = field(default_factory=dict)

