import yaml
from card import Card
from const import CardType, Nation
from .effect import effect_registry

def load_cards_from_yaml(path: str):
    with open(path, 'r') as f:
        config = yaml.safe_load(f)
    card_dict = {}
    for item in config:
        card = Card(
            name=item['name'],
            cost=item['cost'],
            type=CardType[item['type']],
            nation=Nation[item['nation']],
            meta=effect_registry[item['effect']]
        )
        card_dict[item['name']] = card
    return card_dict
