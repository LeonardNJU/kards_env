from card import Card
from constant import MAX_HAND_SIZE


class Hand:
    def __init__(self) -> None:
        self.cards = []
    def add_card(self, card:Card):
        """Add a card to the hand.

        Args:
            card (Card): The card to be added.

        Returns:
            None if the card was added, otherwise the card if the hand is full.
        """
        if self.is_full():
            return card
        self.cards.append(card)
        return None
            
    def is_full(self) -> bool:
        """Check if the hand is full."""
        return len(self.cards) >= MAX_HAND_SIZE