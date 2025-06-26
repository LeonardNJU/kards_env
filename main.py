from game.game import Game
from player.player import Player


def main():
    alice = Player("Alice", "simulate/deck1.txt")
    bob = Player("Bob", "simulate/deck1.txt")

    game = Game(alice, bob)

    game.start()


if __name__ == "__main__":
    main()
