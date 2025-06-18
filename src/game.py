from .player import Player


class Game:
    def __init__(self, player1 : Player, player2 : Player) -> None:
        self.player1 = player1
        self.player2 = player2
        
    def start(self):
        pass