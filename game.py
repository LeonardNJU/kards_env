from traitlets import This
from field import Field
from order import Order
from player import Player


class Game:
    def __init__(self, players: list[Player]):
        self.turn=0
        self.field = Field()
        
        self.players: list[Player] = [None, players[0], players[1]]
        self.current_player = 1
        self.opponent = 2
        
        self.field.player_rows[self.current_player].join(self.players[self.current_player].HQ)
        self.field.player_rows[self.opponent].join(self.players[self.opponent].HQ)
        
        for _ in range(4): self.players[1].hand.draw()
        for _ in range(5): self.players[2].hand.draw()
        
    def __str__(self):
        result= ""
        result+=self.players[self.opponent].name+"\tCmd pts:["+str(self.players[self.opponent].mana)+"/"+str(self.players[self.opponent].max_mana)+"]\t"+"Cards: "+str(len(self.players[self.opponent].hand))+"/"+str(len(self.players[self.opponent].deck))+" cards\n\n"
        result+=self.field.__str__(self.current_player)+"\n"
        result+=self.players[self.current_player].name+"\tCmd pts:["+str(self.players[self.current_player].mana)+"/"+str(self.players[self.current_player].max_mana)+"]\t"+"Hands: "+str(len(self.players[self.current_player].hand))+"/"+str(len(self.players[self.current_player].deck))+" cards\n"
        # hands, opponent hands, deck remains
        result+="\nHands: \n"
        result+=f"{self.players[self.current_player].hand}\n"
        return result
    def paint(self):
        '''
        paint the game
        '''
        print(self)
        
    def reschedule_phase(self,player:int):
        '''
        choose which card to be rescheduled
        '''
        if self.current_player!=player:
            self.current_player,self.opponent=self.opponent,self.current_player

        print("Reschedule phase")
        self.paint()
        while True:
            reschedule=input("Choose cards to reschedule: ")
            if reschedule.lower().startswith('n'):
                break
            try:
                reschedule=[int(i) for i in reschedule.split()]
                # unique and sorted
                reschedule=list(set(reschedule))
                reschedule.sort()
                
                assert len(reschedule)<=len(self.players[player].hand)
                assert all([i in range(len(self.players[player].hand)) for i in reschedule])
                for i in reschedule[::-1]:
                    # check: not sure it can pop right card.
                    card=self.players[player].hand.pop(i)
                    self.players[player].deck.random_add(card)

                for _ in range(len(reschedule)):
                    self.players[player].hand.draw()
                break       # finish reschedule phase

            except:
                print("Invalid input")
                continue
        print("Reschedule phase end")
        self.paint()
            
        
    def turn_phase(self, player:int):
        if self.current_player!=player:
            self.current_player,self.opponent=self.opponent,self.current_player
            
        # turn start
        if player.max_mana<12:
            player.max_mana+=1
        player.mana=player.max_mana
        
        if not (self.turn==1 and self.current_player==1):
            card=player.draw_card()
            if card is not None:
                player.hand.append(card)
        
        # turn mid
        # move, attack, play card
        while True:
            order=player.accept_order()
            # process order
            if order is None:
                continue
            elif order.type==Order.PLAY_CARD:
                if order.card_id>=len(player.hand):
                    print("Invalid card id")
                    continue
                card=player.hand.pop(order.card_id)
                if card.cost>player.mana:
                    print("Not enough mana")
                    player.hand.append(card)
                    continue
                player.mana-=card.cost
                card.play(self.field, player, order.args)
                player.played.append(card)
            elif order.type==Order.MOVE_ATK:
                pass
                
            break
            
        
        # turn end
        
        
def main(pl1,pl2):
    game = Game([pl1, pl2])
    game.reschedule_phase(1)
    game.reschedule_phase(2)
    while True:
        game.turn+=1
        game.turn_phase(1)
        game.turn_phase(2)
    
        
if __name__=="__main__":
    # 先把卡组创建写这里
    from card import cards_pool
    player1=Player("Pl1",[cards_pool[0]]*40)
    player2=Player("Pl2",[cards_pool[0]]*40)
    
    main(player1,player2)