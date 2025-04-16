from field import Field
from player import Player


class Game:
    def __init__(self, players: list[Player]):
        self.turn=0
        self.player1 = players[0]
        self.player2 = players[1]
        self.field = Field()
        self.current_player = self.player1
        self.opponent = self.player2
        self.winner = None
        
        self.field.player_rows[1].join(self.player1.HQ)
        self.field.player_rows[2].join(self.player2.HQ)
        
        for _ in range(4): self.player1.hand.append(self.player1.draw_card())
        for _ in range(5): self.player2.hand.append(self.player2.draw_card())
    def __str__(self):
        result= ""
        result+=self.opponent.name+"\tCmd pts:["+str(self.opponent.mana)+"/"+str(self.opponent.max_mana)+"]\t"+"Cards: "+str(len(self.opponent.hand))+"/"+str(len(self.opponent.deck))+" cards\n\n"
        result+=self.field.__str__(1 if self.current_player==self.player1 else 2)+"\n"
        result+=self.current_player.name+"\tCmd pts:["+str(self.current_player.mana)+"/"+str(self.current_player.max_mana)+"]\t"+"Hands: "+str(len(self.current_player.hand))+"/"+str(len(self.current_player.deck))+" cards\n"
        # hands, opponent hands, deck remains
        return result
    def reschedule_phase(self):
        pass
    def turn_phase(self, player:Player):
        if self.current_player!=player:
            self.current_player,self.opponent=self.opponent,self.current_player
            
        # turn start
        if player.max_mana<12:
            player.max_mana+=1
        player.mana=player.max_mana
        
        if not (self.turn==1 and player==self.player1):
            card=player.draw_card()
            if card is not None:
                player.hand.append(card)
        
        # turn mid
        # move, attack, play card
        while True:
            order=player.accept_order()
            # process order
            break
            
        
        # turn end
        
        
def main(pl1,pl2):
    game = Game([pl1, pl2])
    game.reschedule_phase()
    while True:
        game.turn+=1
        game.turn_phase(player1)
        game.turn_phase(player2)
    
        
if __name__=="__main__":
    from card import cards_pool
    player1=Player("Pl1",[cards_pool[0]]*40)
    player2=Player("Pl2",[cards_pool[0]]*40)
    main(player1,player2)