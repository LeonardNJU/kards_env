from src.symbols import CardType, Nation


class Card:
    def __init__(self, id: int, name: str, nation: Nation, type: CardType, kredits: int):
        self.id = id
        self.name = name
        self.nation = nation
        self.type = type
        self.kredits = kredits

    def __repr__(self):
        return f"Card({self.id}, {self.name}, {self.nation}, {self.type}, {self.kredits})"