from .game import Game
from .player import Player

def main():
    # Set up the logger

    alice= Player("Alice")
    alice.bind_deck("simulate/deck1.txt")
    bob = Player("Bob")
    bob.bind_deck("simulate/deck1.txt")
    
    game=Game(alice, bob)
    
    game.start()
    
if __name__ == "__main__":
    main()