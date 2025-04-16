from const import CardType, Nation
from field import Field
from units.light_infantry import LightInfantry


class Card:
    def __init__(self, name, cost, effect, type:CardType, nation:Nation):
        self.name = name
        self.cost = cost
        self.effect = effect
        self.type = type
        self.nation = nation
    def play(self, field:Field, player:int, position,**kwargs):
        """
        Play the card.
        """
        self.effect(field, player, position,**kwargs)
    def __str__(self):
        return str(self.cost)+"K "+self.name+" "+str(self.type.value)+" "+str(self.nation.value)

def light_infantry_card(field:Field, player:int, position,**kwargs):
    """
    拉一张轻步兵至指定位置
    """
    # field.join(LightInfantry(), player, position)
    field.player_rows[player].join(LightInfantry(),position)

# cards pool
cards_pool=[
    Card(name="轻步兵",
         cost=1,
         effect=light_infantry_card,
         type=CardType.UNIT,
         nation=Nation.SOVIET),
]