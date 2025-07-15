# Singleton
class Game:
    
    _game=None
    def __init__(self):
        assert Game._game is None, "Game instance already exists"
        Game._game = self
    
    @classmethod
    def get_instance(cls):
        # game should be initialized and only once
        assert cls._game is not None, "Game instance not initialized"
        return cls._game