from object.HQ import HQ
from action.action import Action

from player.card_manager import CardManager, DrawResultType
from utils.constant import NORMAL_MAX_KREDITS_SLOT
from utils.logger import setup_logger

logger = setup_logger(__name__)


class Player:
    def __init__(self, name: str, deck_filepath: str) -> None:
        self.name = name
        self.card_manager = CardManager(deck_filepath)
        self.fatigue = 0
        self.obj_on_field = []
        self.kredits = 0
        self.kredits_slot = 0

    def draw_card(self, num: int = 1) -> None:
        """Draw a card from the deck and add it to the player's hand."""
        for _ in range(num):
            result, card = self.card_manager.draw_a_card()
            match result:
                case DrawResultType.SUCCESS:
                    logger.info(f"{self.name} drawn a card: {card}")
                case DrawResultType.HAND_FULL:
                    logger.info(
                        f"{self.name}'s hand is full, card {card} was not added to the hand."
                    )
                case DrawResultType.DECK_EMPTY:
                    logger.info(f"{self.name}'s deck is empty, no card drawn.")
                    self.fatigue += 1
                    logger.info(f"{self.name} has taken {self.fatigue} fatigue damage.")
                    self.HQ.take_damage(self.fatigue)
                case _:
                    logger.error(f"Unexpected draw result: {result}")
                    raise RuntimeError(
                        f"Unexpected draw result: {result} for player {self.name}"
                    )

    def place_HQ(self):
        """create HQ and added to registry, waiting to be placed on the field."""
        self.HQ = HQ(self.card_manager.draw_HQ())
        logger.info(f"{self.name} placed HQ: {self.HQ}")
        self.obj_on_field.append(self.HQ)
        return self.HQ

    def reschedule_phase(self, cards_to_draw: int = 0) -> None:
        """Reschedule the player's phase, e.g., draw cards and redraw."""
        logger.info(f"{self.name} in rescheduling phase.")
        self.card_manager.shuffle_deck()  # Shuffle the deck before drawing cards

        self.draw_card(cards_to_draw)
        self.card_manager.show_hand()
        cards_to_redraw = sorted(
            [
                int(num.strip())
                for num in input(
                    "input the numbers of cards to redraw, e.g. 1,4,5 (-1 to skip): "
                ).split(",")
            ]
        )
        if cards_to_redraw and cards_to_redraw[0] != -1:
            cards_to_redraw = [
                num for num in cards_to_redraw if len(cards_to_redraw) >= num >= 0
            ][
                ::-1
            ]  # Reverse to remove from the end of the list first
            for num in cards_to_redraw:
                try:
                    self.card_manager.put_hand_card_back_to_deck_by_idx(num)
                except IndexError as e:
                    logger.info(f"Error while redrawing card: {e}")
                    continue
                self.draw_card()
                logger.info("redrew a card.")
        else:
            logger.info(f"{self.name} chose not to redraw any cards.")
        print(f"{self.name} finished rescheduling phase.")
        self.card_manager.show_hand()

    def choose_action(self):
        try:
            return Action(self.card_manager.hand, input(f"{self.name}, please type your command: "))
        except Exception:
            # log has done when ValueError is raised in Action
            return None
    def add_kredits_slot(self):
        """Add a kredits slot to the player."""
        if self.kredits_slot < NORMAL_MAX_KREDITS_SLOT:
            self.kredits_slot += 1
            logger.info(f"{self.name} added a kredits slot. Total slots: {self.kredits_slot}")
            
    def refill_kredits(self):
        """Refill the player's kredits to the maximum slot."""
        self.kredits = self.kredits_slot
        logger.info(f"{self.name} refilled kredits to {self.kredits}.")