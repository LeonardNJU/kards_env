from HQ import HeadQuarters


class Player:
    def __init__(self, name):
        self.name = name
        
        self.deck = []
        self.hand = []
        self.discard = []
        self.played = []
        
        self.HQ=HeadQuarters()
        
        self.mana=0
        self.max_mana=0