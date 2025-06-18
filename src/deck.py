import yaml

from src.card import Card
from src.constant import DECK_SIZE
from src.utils.str2obj import str2card_type, str2nation


def load_card_pool(card_pool_filepath: str) -> dict:
    card_pool = {}
    with open(card_pool_filepath, "r") as file:
        card_pool_str = yaml.safe_load(file)
    for card_info in card_pool_str:
        card_pool[card_info["id"]] = Card(
            card_info["id"],
            card_info["name"],
            str2nation(card_info["nation"]),
            str2card_type(card_info["type"]),
            card_info["kredits"],
        )
    return card_pool


class Deck:
    def __init__(self, deck_filepath) -> None:
        self.cards = []
        self.HQ = None
        self.allied = None
        self.load_deck(deck_filepath)

    def load_deck(self, deck_filepath):
        with open(deck_filepath, "r") as file:
            lines = file.readlines()

        assert lines[0].startswith(
            "HQ "
        ), "Deck file must start with 'HQ ' followed by the HQ nation name."
        self.HQ = str2nation(lines[0].strip().split(" ")[1])

        assert lines[1].startswith(
            "Allied "
        ), "Deck file must start with 'Allied ' followed by the Allied nation name."
        self.allied = str2nation(lines[1].strip().split(" ")[1])

        card_pool = load_card_pool("resources/card_pool.yaml")
        for line in lines[2:]:
            card_num, quantity = line.strip().split(" ")
            assert (
                card_num.startswith("#")
                and card_num[1:].isdigit()
                and quantity.isdigit()
            ), "Each card line must be in the format '#<card_number> <quantity>'."
            card_num = int(card_num[1:])
            quantity = int(quantity)
            for _ in range(quantity):
                if card_num in card_pool:
                    self.cards.append(card_pool[card_num])
                else:
                    raise ValueError(f"Card number {card_num} not found in card pool.")
        assert (
            len(self.cards) == DECK_SIZE
        ), f"Deck size must be exactly {DECK_SIZE} cards, but found {len(self.cards)}."
