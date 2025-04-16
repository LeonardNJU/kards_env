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


def light_infantry_card(field:Field, player:int, position):
    """
    拉一张轻步兵至指定位置
    """
    # field.join(LightInfantry(), player, position)
    field.player_rows[player].join(LightInfantry(),position)

# cards pool
cards_pool=[
    Card("轻步兵",1,light_infantry_card,CardType.UNIT,Nation.SOVIET),
]