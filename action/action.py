from enum import Enum
from player.hand import Hand

from utils.logger import setup_logger
logger = setup_logger(__name__)


class ActionType(Enum):
    PLAY_CARD = "play_card"
    MOVE = "move"
    ATTACK = "attack"
    END_TURN = "end_turn"
    SURRENDER = "surrender"

    def __str__(self):
        return self.value
    
class Action:
    def __init__(self, hand: Hand, cmd_str: str):
        """generate an action from a command string.

        Args:
            content (GameContext): the game context, which contains the players and their hands.
            cmd_str (str): the command string to parse for the action.

        Raises:
            ValueError: if the command string does not match any known action.
        """
        commands=cmd_str.split(" ")
        self.type = None
        self.args = commands[1:] if len(commands) > 1 else []

        match commands[0]:
            case "p" | "pl":
                self.type = ActionType.PLAY_CARD
                self.card = hand.get_card_by_idx(self.args[0])
                self.card_str_args = self.args[1:] if len(self.args) > 1 else []
                self.card_args = self.card.args_bind(self.card_str_args)
            case "m" | "mv":
                self.type = ActionType.MOVE
                if (
                    commands[0] == 'm' and len(self.args) == 1
                ):  # shorthand for 'mv xx 5'
                    self.args.append('5')
                if len(self.args) != 2 or not all(
                    arg.isdigit() for arg in self.args
                ):
                    logger.warning(
                        f"Invalid move command: {commands[0]} {self.args}"
                    )
                    raise ValueError(
                        f"Invalid move command: {commands[0]} {self.args}"
                    )
                self.from_idx = int(self.args[0])
                self.to_idx = int(self.args[1])
            case "a" | "at":
                self.type = ActionType.ATTACK
                if len(self.args) != 2 or any(
                    len(str(arg)) != 2 for arg in self.args
                ):
                    logger.warning(
                        f"Invalid attack command: {commands[0]} {self.args}"
                    )
                    raise ValueError(
                        f"Invalid attack command: {commands[0]} {self.args}"
                    )
                self.attacker_idx = self.args[0]
                self.defender_idx = self.args[1]
            case "e" | "end":
                self.type = ActionType.END_TURN
                if len(self.args) != 0:
                    logger.warning(
                        f"Invalid end turn command: {commands[0]} {self.args}"
                    )
                    raise ValueError(
                        f"Invalid end turn command: {commands[0]} {self.args}"
                    )
            case "surrender":
                self.type = ActionType.SURRENDER
            case _:
                logger.warning(f"Unknown action command: {commands[0]}")
                raise ValueError(f"Unknown action command: {commands[0]}")
        
    def __str__(self):
        return f"Action(type={self.type}, args={self.args})"