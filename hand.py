import weakref
from card import Card
from deck import Deck


class Hand:
    MAX_HAND_SIZE=9
    def __init__(self,player):
        self.cards = []
        self._player_ref=weakref.ref(player)
        self.player = self._player_ref()
        if self.player is None:
            raise ValueError("Player is None")
    def __str__(self):
        result=""
        for i,card in enumerate(self.cards):
            result += f"{i}: {card}\n"
        return result
    def __len__(self):
        """
        Return the number of cards in the hand.
        """
        return len(self.cards)
    def is_full(self):
        return len(self)>=self.MAX_HAND_SIZE
    def draw(self,deck:Deck=None):
        """
        Draw a card from the deck and add it to the hand.
        Deck defaults to the player's deck.
        If the deck is empty, increment the player's fatigue.
        If hand is full, discard the drawn card.
        """
        if deck is None:
            deck = self.player.deck
        try:
            card = deck.draw()
        except IndexError:
            print("No more cards in the deck")
            self.player.inc_fatigue()

        if self.is_full():
            print("Hand is full, discarding drawn card")
            print("Discarding card:", card)
            return
        self.cards.append(card)
    def pop(self, index:int):
        """
        Pop a card from the hand.
        """
        assert index in range(len(self.cards)), "Index out of range"
        return self.cards.pop(index)