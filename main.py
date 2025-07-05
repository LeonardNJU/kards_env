from game.game import Game
from player.player import Player
from enum import Enum

class GameState(Enum):
    INIT = "init"
    RESCHEDULE = "reschedule"
    COMBAT = "combat"
    DONE = "done"

gameState = GameState.INIT
player1 :Player = None
player2 :Player = None
game :Game = None


def init():
    global player1, player2, game, gameState
    player1 = Player("Alice", "simulate/deck1.txt")
    player2 = Player("Bob", "simulate/deck1.txt")
    game = Game(player1, player2)
    gameState = GameState.RESCHEDULE

def update():
    pass

def draw():
    pass


if __name__ == "__main__":
    init()
    while True:
        update()
        draw()
