import weakref
from object import Object


class HeadQuarters(Object):
    def __init__(self,nation):
        super().__init__(20,nation)
    def set_player(self, player):
        """_summary_

        Args:
            player (_type_): _description_

        Raises:
            ValueError: _description_
        """
        self._player_ref=weakref.ref(player)
        self.player = self._player_ref()
        if self.player is None:
            raise ValueError("Player is None")
    def __str__(self):
        return "[HQ "+str(self.HP)+"]"
    def die(self):
        self.player.lose()