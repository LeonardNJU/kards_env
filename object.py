class Object:
    def __init__(self,HP):
        self.HP=HP
    def hurt(self, damage:int):
        self.HP-=damage
        if self.HP<=0:
            self.die()