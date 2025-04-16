from object import Object


class HeadQuarters(Object):
    def __init__(self):
        super().__init__(HP=20)
    def set_owner(self, player):
        self.owner=player
    def __str__(self):
        return "[HQ "+str(self.HP)+"]"
    def die(self):
        self.owner.lose()