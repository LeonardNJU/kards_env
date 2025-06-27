from action.action import ActionType, Action
from event.event_manager import EventManager
from game.field import Field
from player.player import Player
from utils.constant import FIELD_WIDTH
from event.event import Event, EventType
from utils.unit_registry import unit_registry 

from utils.logger import setup_logger
logger = setup_logger(__name__)

class GameContext:
    def __init__(self, player1 : Player, player2 : Player) -> None:
        self.players = [player1, player2]
        self.field = Field()
        self.current_turn = 0  
        self.current_player_id = 0
        self.event_manager=EventManager()
        
    def place_HQ(self):
        """Place HQ for both players on the field."""
        self.players[0].place_HQ()
        self.players[0].HQ.bind_owner(0)
        self.players[1].place_HQ()
        self.players[1].HQ.bind_owner(1)
        self.field.insert_object(self.players[0].HQ, 0)
        self.field.insert_object(self.players[1].HQ, 2)
        
    def start_player_turn(self):
        """Start the current player's turn."""
        player= self.players[self.current_player_id]
        logger.info(f"Player {player.name}'s turn starts.")
        # A new game turn
        if self.current_player_id == 0:
            self.current_turn += 1

        # add kredits slot until the max slot is reached
        player.add_kredits_slot()
        player.refill_kredits()
        
        # except the first turn, each player draws a card at the start of their turn
        if self.current_turn != 1 or self.current_player_id != 0:
            player.draw_card()
            
        
    def act_player_turn(self):
        """Handle the actions of the current player during their turn."""
        action=None
        while not action or action.type != ActionType.END_TURN:
            self.show()
            if action := self.players[self.current_player_id].choose_action():
                try:
                    self.execute_action(action)
                except Exception:
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
            f"[{opponent.kredits}/{opponent.kredits_slot}] {opponent.name}  -  {opponent.card_manager.get_hand_size()} cards"
        )
        self.field.show(self.current_player_id)
        print(f"[{us.kredits}/{us.kredits_slot}] {us.name}")
        us.card_manager.show_hand()
        print("#" * FIELD_WIDTH)

    def execute_action(self, action: Action):
        """Executes the given action.
        Will check if the action is valid and then perform it on the game field.

        Args:
            action (Action): The action to be executed.
        """
        match action.type:
            case ActionType.END_TURN:
                pass
            case ActionType.PLAY_CARD:
                self.execute_play_card(action)
            case ActionType.ATTACK:
                pass
                # self.field.attack(action.attacker_id, action.target_id)
            case ActionType.MOVE:
                pass
                # self.field.move_object(action.object_id, action.new_position)
            case ActionType.SURRENDER:
                logger.info(f"Player {self.players[self.current_player_id].name} has surrendered.")
                self.winning(get_opponent_player_id(self.current_player_id))
            case _:
                raise ValueError(f"Unknown action type: {action.type}")

    def execute_play_card(self, action: Action):
        player = self.players[self.current_player_id]

        # checkers
        if player.kredits < action.card.kredits:
            logger.warning(f"Player {player.name} tried to play a card with insufficient kredits: {action.card.name}")
            raise ValueError("Not enough kredits to play this card.")

        self.play_card(action)
        self.event_manager.dispatch(Event(EventType.CARD_PLAYED, {"owner_id": self.current_player_id, "card": action.card}))
        player.kredits -= action.card.kredits
        player.card_manager.use_hand_card(action.card)

    def play_card(self, action: Action):
        for ef in action.card.effects:
            match ef["action"]:
                case "deploy":
                    unit = unit_registry.get_unit_by_name(ef["unit"])
                    if "deploy_position" not in action.card_args or not isinstance(action.card_args["deploy_position"], int):
                        logger.error(f"Invalid deploy position: {action.card_args['deploy_position']}")
                        raise ValueError(f"Invalid deploy position: {action.card_args['deploy_position']}")
                    self.field.insert_object(unit, Field.player_id_to_row(self.current_player_id), action.card_args["deploy_position"])
                    unit.bind_owner(self.current_player_id)
                    
    def winning(self, winner_id: int):
        """Declare the winner of the game."""
        logger.info(f"Player {self.players[winner_id].name} wins!")
        exit(0)

        
        
def get_opponent_player_id(current_player_id: int) -> int:
    """Returns the opponent's player ID."""
    return 1 - current_player_id