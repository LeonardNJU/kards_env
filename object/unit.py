from dataclasses import dataclass, field
from typing import Any, Dict, List

from event.event import Event, EventType
from event.event_manager import EventManager
from object.object import Object
from utils.symbols import Nation, UnitType

@dataclass
class Unit(Object):
    id: str
    name: str
    nation: Nation
    type: UnitType
    HP: int
    atk: int
    oil: int

    sp: List[str] = field(default_factory=list)
    abilities: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        self.flags = ["move_in"]

    def can_move(self) -> bool:
        """Check if the unit can move."""
        if "move_in" in self.flags and "blitz" not in self.sp:
            return False
        if "moved" in self.flags:
            return False
        return True
    
    def can_attack(self) -> bool:
        """Check if the unit can attack."""
        if "move_in" in self.flags and "blitz" not in self.sp:
            return False
        if "moved" in self.flags and not self.type == UnitType.ARMOR:
            return False
        if "attacked" in self.flags and "fury" not in self.sp:
            return False
        if "2-attacked" in self.flags:
            return False
        return True
        
    
    def moved(self) -> None:
        """Mark the unit as moved."""
        self.flags.append("moved")
        
    def attacked(self) -> None:
        """Mark the unit as attacked."""
        if "attacked" in self.flags:
            self.flags.remove("attacked")
            self.flags.append("2-attacked")
        else:
            self.flags.append("attacked")
        
    def clear_flags(self) -> None:
        """Clear the flags of the unit."""
        self.flags.clear()
    
    def start_turn_effects(self, event_manager) -> None:
        """Apply start turn effects."""
        pass
    
    def end_turn_effects(self, event_manager) -> None:
        """Apply end turn effects."""
        self.clear_flags()

    def attack(self, target:object, event_manager:EventManager):
        """attack the target object."""
        target.take_damage(self.atk, event_manager)
        event_manager.dispatch(Event(EventType.TAKE_DAMAGE, {"object": target, "damage": self.atk}))
        if target.HP == 0:
            event_manager.dispatch(Event(EventType.UNIT_DIED, {"object": target}))
            
        if isinstance(target, Unit) and self.type != UnitType.ARTILLERY:
            self.take_damage(target.atk, event_manager)
            event_manager.dispatch(Event(EventType.TAKE_DAMAGE, {"object": self, "damage": target.atk}))
            if self.HP == 0:
                event_manager.dispatch(Event(EventType.UNIT_DIED, {"object": self}))
            
        