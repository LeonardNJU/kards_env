from .game import Game
from .player import Player
from src.utils.logger import setup_logger

def main():
    # Set up the logger
    logger = setup_logger(__name__)

    alice= Player("Alice")
    alice.bind_deck("simulate/deck1.txt")
    bob = Player("Bob")
    bob.bind_deck("simulate/deck1.txt")
    
    game=Game(alice, bob)
    
    logger.info(f"Starting game between {alice.name} and {bob.name}")
    game.start()
    
if __name__ == "__main__":
    main()