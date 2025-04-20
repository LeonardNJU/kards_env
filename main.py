
from HQ import HeadQuarters
from const import Nation
from game import Game
from player import Player
from units.card_loader import load_cards_from_yaml


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
    cards = load_cards_from_yaml("units/cards.yaml")

    hq1=HeadQuarters(Nation.USA)
    hq2=HeadQuarters(Nation.USA)
    player1=Player("Pl1",1,hq1, [cards["轻步兵"]]*20+[cards["习致野"]]*19)
    player2=Player("Pl2",2,hq2, [cards["习致野"]]*39)
    hq1.set_player(player1)
    hq2.set_player(player2)
    
    main(player1,player2)