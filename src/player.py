from hand import Hand
from .deck import Deck
from src.utils.logger import setup_logger
logger=setup_logger(__name__)

class Player:
    def __init__(self, name: str) -> None:
        self.name = name
        self.deck = None
        self.hand = Hand()
        self.fatigue = 0

    def bind_deck(self, deck_filepath: str) -> None:
        """Bind a deck to the player."""
        self.deck = Deck(deck_filepath)
        
    def draw_card(self) -> None:
        """Draw a card from the deck and add it to the player's hand."""
        if self.deck is None:
            logger.error("Attempted to draw a card without a bound deck.")
            raise RuntimeError("Player deck is not bound. Please bind a deck before drawing cards.")
        if card := self.deck.draw():
            if self.hand.add_card(card):
                logger.info(f"{self.name}'s hand is full, card {card} was not added to the hand.")
            else:
                logger.info(f"{self.name} drew a card: {card}")
        else:
            logger.info(f"{self.name}'s deck is empty, no card drawn.")
            self.fatigue += 1
            logger.info(f"{self.name} has taken {self.fatigue} fatigue damage.")
            # [TODO] Implement fatigue effects on player actions.
