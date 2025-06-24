from action.action import ActionType, Action
from game.field import Field
from game.player import Player
from utils.constant import FIELD_WIDTH

from utils.logger import setup_logger
logger = setup_logger(__name__)

class GameContext:
    def __init__(self, player1 : Player, player2 : Player) -> None:
        self.players = [player1, player2]
        self.field=Field()
        self.current_turn = 0  
        self.current_player_id = 0
        
    def place_HQ(self):
        """Place HQ for both players on the field."""
        self.players[0].place_HQ()
        self.players[1].place_HQ()
        self.field.insert_object(self.players[0].HQ, 0)
        self.field.insert_object(self.players[1].HQ, 2)
        
    def start_player_turn(self):
        """Start the current player's turn."""
        logger.info(f"Player {self.players[self.current_player_id].name}'s turn starts.")
        # A new game turn
        if self.current_player_id == 0:
           self.current_turn += 1

        # except the first turn, each player draws a card at the start of their turn
        if self.current_turn != 1 or self.current_player_id != 0:
            self.players[self.current_player_id].draw_card()
            
        
    def act_player_turn(self):
        """Handle the actions of the current player during their turn."""
        action=None
        while not action or action.type != ActionType.END_TURN:
            self.show()
            if action := self.players[self.current_player_id].choose_action():
                try:
                    self.execute_action(action)
                except Exception as e:
                    logger.info(f"Error while executing action: {e}")
                    continue
            
    
    def end_player_turn(self):
        """End the current player's turn."""
        logger.info(f"Player {self.players[self.current_player_id].name}'s turn ends.")
        self.current_player_id = get_opponent_player_id(self.current_player_id)
        self.show()
        

    def show(self):
        print("#" * FIELD_WIDTH)
        print(f"Current turn: {self.current_turn}")
        opponent = self.players[get_opponent_player_id(self.current_player_id)]
        us = self.players[self.current_player_id]
        print(
            f"[{opponent.kredits}/{opponent.kredits_slot}] {opponent.name}  -  {opponent.hand.size()} cards"
        )
        self.field.show(self.current_player_id)
        print(f"[{us.kredits}/{us.kredits_slot}] {us.name}")
        us.hand.show()
        print("#" * FIELD_WIDTH)

    def execute_action(self, action: Action):
        """Executes the given action.

        Args:
            action (Action): The action to be executed.
        """
        match action.type:
            case ActionType.END_TURN:
                pass
            case ActionType.PLAY_CARD:
                
            case ActionType.ATTACK:
                self.field.attack(action.attacker_id, action.target_id)
            case ActionType.MOVE_OBJECT:
                self.field.move_object(action.object_id, action.new_position)
            case _:
                raise ValueError(f"Unknown action type: {action.type}")

def get_opponent_player_id(current_player_id: int) -> int:
    """Returns the opponent's player ID."""
    return 1 - current_player_id