from typing import List
from utils.symbols import CardType, Nation


class Card:
    def __init__(self, id: int, name: str, nation: Nation, type: CardType, kredits: int, effects: List[dict]):
        self.id = id
        self.name = name
        self.nation = nation
        self.type = type
        self.kredits = kredits
        self.effects = effects

    def __repr__(self):
        return f"Card({self.id}, {self.name}, {self.nation}, {self.type}, {self.kredits}, {self.effects})"