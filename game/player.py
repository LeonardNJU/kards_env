from game.hand import Hand
from game.deck import Deck
from object.HQ import HQ
from action.action import Action

from utils.logger import setup_logger

logger = setup_logger(__name__)


class Player:
    def __init__(self, name: str) -> None:
        self.name = name
        self.deck = None
        self.hand = Hand()
        self.fatigue = 0
        self.obj_on_field = (
            []
        )  # List to hold objects on the field, e.g., HQ, units, etc.
        self.kredits = (
            0  # Player's kredits, can be used to play cards or activate abilities
        )
        self.kredits_slot = (
            0  # Kredits slot, used to track kredits spent or available for use
        )

    def bind_deck(self, deck_filepath: str) -> None:
        """Bind a deck to the player."""
        self.deck = Deck(deck_filepath)

    def draw_card(self, num: int = 1) -> None:
        """Draw a card from the deck and add it to the player's hand."""
        if self.deck is None:
            logger.error("Attempted to draw a card without a bound deck.")
            raise RuntimeError(
                "Player deck is not bound. Please bind a deck before drawing cards."
            )
        for _ in range(num):
            if card := self.deck.draw():
                if self.hand.add_card(card):
                    logger.info(
                        f"{self.name}'s hand is full, card {card} was not added to the hand."
                    )
                else:
                    logger.info(f"{self.name} drew a card: {card}")
            else:
                logger.info(f"{self.name}'s deck is empty, no card drawn.")
                self.fatigue += 1
                logger.info(f"{self.name} has taken {self.fatigue} fatigue damage.")
                self.HQ.take_damage(self.fatigue)

    def place_HQ(self):
        """create HQ and added to registry, waiting to be placed on the field."""
        assert self.deck is not None, "Deck must be bound before placing HQ."
        self.HQ = HQ(self.deck.draw_HQ())
        logger.info(f"{self.name} placed HQ: {self.HQ}")
        self.obj_on_field.append(self.HQ)
        return self.HQ

    def reschedule_phase(self, cards_to_draw: int = 0) -> None:
        """Reschedule the player's phase, e.g., draw cards and redraw."""
        logger.info(f"{self.name} in rescheduling phase.")
        assert self.deck is not None, "Deck must be bound before rescheduling phase."
        self.deck.shuffle()  # Shuffle the deck before drawing cards

        self.draw_card(cards_to_draw)
        self.hand.show()
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
                if num < 0 or num >= self.hand.size():
                    logger.error(f"Invalid card number {num} for redraw.")
                    continue
                card = self.hand.cards.pop(num)
                self.deck.add_card(card)
                self.draw_card()
                logger.info(f"redrew card from {card}")
        else:
            logger.info(f"{self.name} chose not to redraw any cards.")
        print(f"{self.name} finished rescheduling phase.")
        self.hand.show()

    def choose_action(self):
        try:
            return Action(self.hand, input(f"{self.name}, please type your command: "))
        except Exception as e:
            logger.info(f"Error while parsing action: {e}")
            return None
