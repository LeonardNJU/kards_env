from const import DamageSource, Nation


class Object:
    def __init__(self,HP, nation:Nation):
        self.HP=HP
        self.nation=nation
    def hurt(self, damage:int, src=None):
        '''
        hurt the object
        :param damage: damage value
        :param src: the source of the damage
        '''
        if src==DamageSource.FATIQUE:
            # fatigue damage
            self.HP-=damage
        else:
            self.HP-=damage

        # check if the object is dead
        if self.HP<=0:
            self.die()