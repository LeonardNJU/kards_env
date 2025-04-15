from field import Field
from player import Player


class Game:
    def __init__(self, players: list[Player]):
        self.player1 = players[0]
        self.player2 = players[1]
        self.field = Field()
        self.current_player = self.player1
        self.opponent = self.player2
        self.winner = None
        
        self.field.player1_row.join(self.player1.HQ)
        self.field.player2_row.join(self.player2.HQ)
    def __str__(self):
        result= ""
        result+=self.opponent.name+"\tCmd pts:["+str(self.opponent.mana)+"/"+str(self.opponent.max_mana)+"]\t"+"Hands: "+str(len(self.opponent.hand))+" cards\n\n"
        result+=self.field.__str__(1 if self.current_player==self.player1 else 2)+"\n"
        result+=self.current_player.name+"\tCmd pts:["+str(self.current_player.mana)+"/"+str(self.current_player.max_mana)+"]\t"+"Hands: "+str(len(self.current_player.hand))+" cards\n\n"
        # hands, opponent hands, deck remains
        return result
        
        
if __name__=="__main__":
    game = Game([Player("Player 1"), Player("Player 2")])
    print(game)
    # Add more game logic here