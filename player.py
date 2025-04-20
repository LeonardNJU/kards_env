from re import S
from turtle import position
from deck import Deck
from hand import Hand
from order import Order
from HQ import HeadQuarters
from card import Card


class Player:
    MAX_NUTURAL_MANA=12
    MAX_BOUND_MANA=24
    def __init__(self, name, number, HQ:HeadQuarters, cards:list[Card]):
        self.name=name

        self.number=number
        
        self.deck = Deck(cards)
        self.hand :Hand = Hand(self)
        
        self.discard :list[Card]= []
        self.played :list[Card]= []
        
        self.HQ=HQ
        
        self.mana=0
        self.max_mana=0
        
        self.fatigue=0
        
        self.last_order=None
    def draw_card(self):
        self.hand.draw()
    def lose(self):
        print(self.name+" lose.")
        exit(0)
    def accept_order(self)->Order:
        # accept order from player
        order_str=input("input your order:")
        if order_str=="" and self.last_order is not None:
            print("Using last order", self.last_order)
            order=self.last_order
        else:
            try:
                order=Order(order_str)
                self.last_order=order
            except Exception as e:
                print(e)
                print("Invalid order")
                return None
        return order
    def inc_fatigue(self):
        self.fatigue+=1
        self.HQ.hurt(self.fatigue)
    def inc_mana(self):
        if self.max_mana<self.MAX_NUTURAL_MANA:
            self.max_mana+=1
        self.mana=self.max_mana

    def play_card(self, game,card:Card,args)->bool:
        '''
        play a card from hand
        return True if success
        '''
        if card.cost>self.mana:
            print("Not enough mana")
            return False
        try:
            card.play(game, self.number, *args)
            self.mana-=card.cost
            return True
        except ValueError as e:
            print(e)
            return False
        except Exception as e:
            print(e)
            return False

    
    def turn(self,game):
        from game import Game
        game:Game
        while True:
            game.paint()
            order=self.accept_order()
            if order is None:
                continue

            if order.type==Order.PLAY_CARD:
                try:
                    if self.play_card(game,self.hand[order.card_idx],order.args):
                        self.hand.pop(order.card_idx)
                except IndexError as e:
                    print(e)
                    continue
                except Exception as e:
                    print(e)
                    continue
                
            elif order.type==Order.MOVE_ATK:
                try:
                    game.field.move_atk(game,self.number, order._from, order._to)
                except ValueError as e:
                    print(e)
                    continue
                except Exception as e:
                    print(e)
                    continue
                
            elif order.type==Order.END_TURN:
                print("End turn")
                break
            else:
                print("Invalid order")
                continue