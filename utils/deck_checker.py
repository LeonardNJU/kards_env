from utils.constant import DECK_SIZE
from utils.symbols import Nation


def check(deck_filepath: str):
    cards=[]
    with open(deck_filepath, "r") as file:
        lines = file.readlines()

    assert lines[0].startswith(
        "HQ "
    ), "Deck file must start with 'HQ ' followed by the HQ nation name."
    host = Nation.from_str(lines[0].strip().split(" ")[1])

    assert lines[1].startswith(
        "Allied "
    ), "Deck file must start with 'Allied ' followed by the Allied nation name."
    allied = Nation.from_str(lines[1].strip().split(" ")[1])

    total_num=0
    for line in lines[2:]:
        quantity, name = line.strip().split(" ", 1)
        assert quantity.isdigit(), "Each card line must be in the format '<quantity> <card_name>'."
        quantity = int(quantity)
        # for _ in range(quantity):
        #     if card := card_registry.get_card_by_name(name):
        #         cards.append(card)
        #     else:
        #         raise ValueError(f"Card `{name}` not found in card pool.")
        total_num += quantity
    assert (
            total_num == DECK_SIZE
            # len(cards) == DECK_SIZE
    ), f"Deck size must be exactly {DECK_SIZE} cards, but found {total_num}."

    print("Deck is valid.")
    print("Host nation:", host)
    print("Allied nation:", allied)
    print("Deck size:", DECK_SIZE)


check('../simulate/deck1.txt')