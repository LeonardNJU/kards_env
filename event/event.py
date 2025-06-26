from enum import Enum

class EventType(Enum):
    CARD_PLAYED = "card_played"
    UNIT_DEPLOYED = "unit_deployed"
    UNIT_DIED = "unit_died"
    TURN_START = "turn_start"
    ATTACK = "attack"
    CARD_DRAWN = "card_drawn"
    UNIT_MOVED = "unit_moved"

class Event:
    def __init__(self, event_type: EventType, data: dict):
        self.type = event_type
        self.data = data
