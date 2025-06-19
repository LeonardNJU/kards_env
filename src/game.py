from .player import Player
from .utils.logger import setup_logger

logger=setup_logger(__name__)

class Game:
    def __init__(self, player1 : Player, player2 : Player) -> None:
        self.player1 = player1
        self.player2 = player2
        
    def start(self):
        logger.info(f"Starting game between {self.player1.name} and {self.player2.name}")
        
    def reschedule_phase(self):
        logger.info("Rescheduling phase")
        # Logic for rescheduling phase would go here
        