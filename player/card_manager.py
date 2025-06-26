from card.card import Card
from player.hand import Hand
from player.deck import Deck

from enum import Enum

class DrawResultType(Enum):
    SUCCESS = "success"
    HAND_FULL = "hand_full"
    DECK_EMPTY = "deck_empty"

class CardManager:
    def __init__(self, deck_filepath:str):
        """Initialize the CardManager with a deck file path."""
        self.deck = Deck(deck_filepath)
        self.hand = Hand()
        self.used_cards=[]
    
    def draw_HQ(self):
        """Draw the HQ card from the deck."""
        return self.deck.draw_HQ()
        
    def draw_a_card(self) -> tuple[DrawResultType, Card|None]:
        if card := self.deck.draw():
            if self.hand.add_card(card):
                return DrawResultType.HAND_FULL, card
            else:
                return DrawResultType.SUCCESS, card
        else:
            return DrawResultType.DECK_EMPTY, None
        
    def shuffle_deck(self):
        """Shuffle the deck."""
        self.deck.shuffle()
        
    def show_hand(self):
        """Display the cards in the hand."""
        self.hand.show()    
        
    def get_hand_size(self):
        return self.hand.size()
    
    def put_hand_card_back_to_deck_by_idx(self, index: int) -> None:
        """Put a card back to the deck by its index in the hand."""
        if not 0 <= index < self.hand.size():
            raise IndexError(f"Invalid index: {index}. Hand size is {self.hand.size()}.")
        card = self.hand.cards.pop(index)
        self.deck.add_card(card)
        
    def use_hand_card(self, usedCard: Card):
        """use a hand card. Put in used pile.

        Args:
            usedCard (Card): used card
        """
        self.hand.remove_card(usedCard)
        self.used_cards.append(usedCard)
        