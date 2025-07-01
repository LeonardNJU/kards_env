from dataclasses import dataclass

from event.event import Event, EventType
from event.event_manager import EventManager


@dataclass
class Object:
    name: str
    HP: int
    
    def take_damage(self, damage:int, event_manager: EventManager) -> int:
        """Reduce the object's HP by the specified damage amount.
        Args:
            damage (int): The amount of damage to apply.
        Returns:
            int: The remaining HP after taking damage. If HP falls below 0, it is set to 0.
        """
        event_manager.dispatch(Event(EventType.TAKE_DAMAGE, {"object":self, "damage": damage}))
        self.HP -= damage
        self.HP = max(self.HP, 0)
        return self.HP
    
    def __str__(self) -> str:
        return f"[{self.name}({self.HP})]"

    def bind_owner(self, owner_id: int):
        self.owner = owner_id
        