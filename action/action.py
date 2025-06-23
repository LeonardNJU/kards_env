from enum import Enum
from venv import logger
class Action(Enum):
    PLAY_CARD = "play_card"
    MOVE= "move"
    ATTACK = "attack"
    END_TURN = "end_turn"
    
    def __init__(self, cmd_str: str):
        commands=cmd_str.split(" ")
        self.type = None
        self.args = commands[1:] if len(commands) > 1 else []
        
        match commands[0]:
            case "p" | "pl":
                self.type = Action.PLAY_CARD
            case "m" | "mv":
                self.type = Action.MOVE
            case "a" | "at":
                self.type = Action.ATTACK
            case "e" | "et":
                self.type = Action.END_TURN
            case _:
                logger.warning(f"Unknown action command: {commands[0]}")
                raise ValueError(f"Unknown action command: {commands[0]}")
        
    def __str__(self):
        return f"Action(type={self.type}, args={self.args})"