from .constant import FIELD_WIDTH, FIRST_PLAYER_CARDS, SECOND_PLAYER_CARDS
from .field import Field
from .player import Player
from .utils.logger import setup_logger

logger=setup_logger(__name__)

class Game:
    def __init__(self, player1 : Player, player2 : Player) -> None:
        self.players = [player1, player2]
        self.field=Field()
        self.current_turn = 0  
        self.current_player_num = 0
        
    def start(self):
        # Show the players' names and put HQ on board
        logger.info(f"Starting game between {self.players[0].name} and {self.players[1].name}")
        self.field.insert_object(self.players[0].place_HQ(), 0)
        self.field.insert_object(self.players[1].place_HQ(), 2)
        self.reschedule_phase()
        self.show()
        
    def reschedule_phase(self):
        logger.info("Rescheduling phase")
        # Logic for rescheduling phase would go here
        self.players[0].reschedule_phase(FIRST_PLAYER_CARDS)
        self.players[1].reschedule_phase(SECOND_PLAYER_CARDS)
        
        
    def show(self):
        print("#"*FIELD_WIDTH)
        print(f"Current turn: {self.current_turn}")
        opponent=self.players[self.get_opponent_num()]
        us= self.players[self.current_player_num]
        print(f"[{opponent.kredits}/{opponent.kredits_slot}] {opponent.name}  -  {opponent.hand.size()} cards")
        self.field.show(current_player_num=self.current_player_num)
        print(f"[{us.kredits}/{us.kredits_slot}] {us.name}")
        us.hand.show()
        print("#"*FIELD_WIDTH)
    
    def get_opponent_num(self):
        return (self.current_player_num + 1) % 2
    

