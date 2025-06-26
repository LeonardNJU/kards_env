from card.card import Card
from utils.constant import MAX_HAND_SIZE


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

    def show(self):
        for i, card in enumerate(self.cards):
            print(f"#{i}: {card.name} ({card.nation}, {card.type}, {card.kredits}K)")
    
    def size(self) -> int:
        """Get the number of cards in the hand."""
        return len(self.cards)
    
    def get_card_by_idx(self, card_id: str) -> Card:
        """Get a card by its index in the hand.

        Args:
            card_id (str): The index of the card.

        Returns:
            Card: The card at the specified index.
        """
        try:
            idx = int(card_id)
            return self.cards[idx]
        except (ValueError, IndexError) as e:
            raise ValueError(f"Invalid card index: {card_id}") from e
    
    def remove_card(self, card: Card) -> None:
        """Remove a card from the hand.

        Args:
            card (Card): The card to be removed.
        """
        if card in self.cards:
            self.cards.remove(card)
        else:
            raise ValueError(f"Card {card.name} not found in hand.")