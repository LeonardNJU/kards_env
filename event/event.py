from enum import Enum

class EventType(Enum):
    CARD_PLAYED = "card_played"
    CARD_DRAWN = "card_drawn"

    UNIT_DEPLOYED = "unit_deployed"
    UNIT_DIED = "unit_died"
    UNIT_ATTACK = "attack"
    TAKE_DAMAGE = "take_damage"
    UNIT_MOVED = "unit_moved"

    TURN_START = "turn_start"

class Event:
    def __init__(self, event_type: EventType, data: dict):
        self.type = event_type
        self.data = data
