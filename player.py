from order import Order
from HQ import HeadQuarters
from card import Card


class Player:
    def __init__(self, name, deck:[Card]):
        self.name=name
        
        self.deck = deck
        self.hand = []
        self.discard = []
        self.played = []
        
        self.HQ=HeadQuarters()
        self.HQ.set_owner(self)
        
        self.mana=0
        self.max_mana=0
        
        self.fatigue=0
    def draw_card(self):
        if len(self.deck)==0:
            # into fatigue
            self.fatigue+=1
            self.HQ.HP.hurt(self.fatigue)
            return None
        card=self.deck.pop(0)
        return card
    def lose(self):
        print(self.name+" lose.")
        exit(0)
    def accept_order(self)->Order:
        # accept order from player
        pass