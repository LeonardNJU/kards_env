from __future__ import annotations
from field import Field
from player import Player
from units.card_loader import load_cards_from_yaml


class Game:
    def __init__(self, players: list[Player]):
        self.turn=0
        self.field = Field()
        
        self.players: list[Player] = [None, players[0], players[1]]
        self.active_player_id = 1
        self.rival_player_id = 2
        
        self.field.player_rows[self.active_player_id].join(self.players[self.active_player_id].HQ)
        self.field.player_rows[self.rival_player_id].join(self.players[self.rival_player_id].HQ)
        
        for _ in range(4): self.players[1].hand.draw()
        for _ in range(5): self.players[2].hand.draw()
        
    def __str__(self):
        result= f"Turn {self.turn}\n"
        result+=self.players[self.rival_player_id].name+"\tCmd pts:["+str(self.players[self.rival_player_id].mana)+"/"+str(self.players[self.rival_player_id].max_mana)+"]\t"+"Cards: "+str(len(self.players[self.rival_player_id].hand))+"/"+str(len(self.players[self.rival_player_id].deck))+" cards\n\n"
        result+=self.field.__str__(self.active_player_id)+"\n"
        result+=self.players[self.active_player_id].name+"\tCmd pts:["+str(self.players[self.active_player_id].mana)+"/"+str(self.players[self.active_player_id].max_mana)+"]\t"+"Hands: "+str(len(self.players[self.active_player_id].hand))+"/"+str(len(self.players[self.active_player_id].deck))+" cards\n"
        # hands, opponent hands, deck remains
        result+="\nHands: \n"
        if self.players[self.active_player_id].hand.is_empty():
            result+="Empty\n"
        else:
            result+=f"{self.players[self.active_player_id].hand}\n"
        return result
    def paint(self):
        '''
        paint the game
        '''
        BOARD_WIDTH=40
        BAR="#"*BOARD_WIDTH
        print(BAR)
        print(self)
        print(BAR)
        print()
        
    def reschedule_phase(self,player_id:int):
        '''
        choose which card to be rescheduled
        '''
        if self.active_player_id!=player_id:
            self.active_player_id,self.rival_player_id=self.rival_player_id,self.active_player_id

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
                
                assert len(reschedule)<=len(self.players[player_id].hand)
                assert all([i in range(len(self.players[player_id].hand)) for i in reschedule])
                for i in reschedule[::-1]:
                    # TODO: check: not sure it can pop right card.
                    card=self.players[player_id].hand.pop(i)
                    self.players[player_id].deck.random_add(card)

                for _ in range(len(reschedule)):
                    self.players[player_id].hand.draw()
                break       # finish reschedule phase

            except:
                print("Invalid input")
                continue
        print("Reschedule phase end")
        self.paint()
            
    def turn_starting_phase(self, player_id:int):
        '''
        turn starting phase
        '''
        # change active player
        if self.active_player_id!=player_id:
            self.active_player_id,self.rival_player_id=self.rival_player_id,self.active_player_id
        player=self.players[self.active_player_id]
            
        '''
        turn start
        '''
        
        print("Turn start")
        
        # increase mana
        player.inc_mana()
        
        # draw card
        if not (self.turn==1 and self.active_player_id==1):
            print("Draw a card")
            player.draw_card()
            
        self.paint()

    def turn_end_phase(self, player_id:int):
        '''
        turn end
        '''
        print("Turn end")

    def turn_phase(self, active_player_id:int):
        self.turn_starting_phase(active_player_id)
        self.players[self.active_player_id].turn(self)
        self.turn_end_phase(active_player_id)

def main(pl1,pl2):
    game = Game([pl1, pl2])
    # game.reschedule_phase(1)
    # game.reschedule_phase(2)
    while True:
        game.turn+=1
        game.turn_phase(1)
        game.turn_phase(2)
    
        
if __name__=="__main__":
    # 先把卡组创建写这里
    cards = load_cards_from_yaml("units/cards.yaml")

    player1=Player("Pl1",1, [cards[0]]*39)
    player2=Player("Pl2",2, [cards[0]]*39)
    
    main(player1,player2)