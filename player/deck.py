from card.card import Card
from utils.card_registry import card_registry
from utils.constant import DECK_SIZE
from utils.symbols import Nation
from utils.logger import setup_logger

logger = setup_logger(__name__)


class Deck:
    def __init__(self, deck_filepath) -> None:
        self.cards = []
        self.host = None
        self.allied = None
        self.load_deck(deck_filepath)

    def load_deck(self, deck_filepath):
        with open(deck_filepath, "r") as file:
            lines = file.readlines()

        assert lines[0].startswith(
            "HQ "
        ), "Deck file must start with 'HQ ' followed by the HQ nation name."
        self.host = Nation.from_str(lines[0].strip().split(" ")[1])

        assert lines[1].startswith(
            "Allied "
        ), "Deck file must start with 'Allied ' followed by the Allied nation name."
        self.allied = Nation.from_str(lines[1].strip().split(" ")[1])

        for line in lines[2:]:
            quantity, name = line.strip().split(" ", 1)
            assert quantity.isdigit(), "Each card line must be in the format '<quantity> <card_name>'."
            quantity = int(quantity)
            for _ in range(quantity):
                if card := card_registry.get_card_by_name(name):
                    self.cards.append(card)
                else:
                    raise ValueError(f"Card `{name}` not found in card pool.")
        assert (
            len(self.cards) == DECK_SIZE
        ), f"Deck size must be exactly {DECK_SIZE} cards, but found {len(self.cards)}."

    def draw(self):
        logger.debug("Drawing a card from the deck.")
        return self.cards.pop() if self.cards else None
    
    def draw_HQ(self)->Nation:
        assert self.host is not None, "Host nation must be set before drawing HQ."
        logger.debug(f"Drawing HQ for host nation: {self.host}")
        return self.host
        
    def shuffle(self):
        import random
        logger.debug("Shuffling the deck.")
        random.shuffle(self.cards)
        
    def add_card(self, card: Card, insert_random: bool=True) -> None:
        """Add a card to the deck."""
        if insert_random:
            import random
            position = random.randint(0, len(self.cards))
            self.cards.insert(position, card)
        else:
            self.cards.append(card)
        logger.info(f"Card {card.name} added to the deck.")