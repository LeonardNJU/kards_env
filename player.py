from deck import Deck
from hand import Hand
from order import Order
from HQ import HeadQuarters
from card import Card


class Player:
    def __init__(self, name, cards:[Card]):
        self.name=name
        
        self.deck = Deck(cards)
        self.hand :Hand = Hand(self)
        
        self.discard :list[Card]= []
        self.played :list[Card]= []
        
        self.HQ=HeadQuarters(self)
        
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
        order_str=input("input your order:")
        try:
            order=Order(order_str)
        except Exception as e:
            print(e)
            print("Invalid order")
            return None
        return order
    def inc_fatigue(self):
        self.fatigue+=1
        self.HQ.hurt(self.fatigue)