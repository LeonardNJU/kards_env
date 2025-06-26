from game.context import GameContext
from utils.constant import FIELD_WIDTH, FIRST_PLAYER_CARDS, SECOND_PLAYER_CARDS
from game.field import Field
from player.player import Player
from utils.logger import setup_logger

logger = setup_logger(__name__)


class Game:
    def __init__(self, player1: Player, player2: Player) -> None:
        self.content = GameContext(player1, player2)

    def start(self):
        # Show the players' names and put HQ on board
        logger.info(
            f"Starting game between {self.content.players[0].name} and {self.content.players[1].name}"
        )
        self.content.place_HQ()

        self.reschedule_phase()

        self.combat_phase()

    def reschedule_phase(self):
        logger.info("Rescheduling phase")
        # Logic for rescheduling phase would go here
        self.content.players[0].reschedule_phase(FIRST_PLAYER_CARDS)
        self.content.players[1].reschedule_phase(SECOND_PLAYER_CARDS)

    def combat_phase(self):
        logger.info("Combat phase started")
        while True:
            self.content.start_player_turn()
            self.content.act_player_turn()
            self.content.end_player_turn()
