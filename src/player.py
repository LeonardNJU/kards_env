from .deck import Deck


class Player:
    def __init__(self, name: str) -> None:
        self.name = name
        self.deck = None

    def bind_deck(self, deck_filepath: str) -> None:
        """Bind a deck to the player."""
        self.deck = Deck(deck_filepath)
