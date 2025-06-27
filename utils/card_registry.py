import os
import yaml
from card.card import Card
from utils.logger import setup_logger
logger = setup_logger(__name__)

class CardRegistry:
    def __init__(self, card_dir: str):
        self.cards_by_id :dict[str, Card]= {}
        self.cards_by_name :dict[str, Card] = {}
        self.id_counter = 0
        self.load_cards(card_dir)

    def load_cards(self, card_dir: str):
        for fname in os.listdir(card_dir):
            if not fname.endswith(".yaml"):
                continue
            with open(os.path.join(card_dir, fname), 'r', encoding='utf-8') as f:
                card_list = yaml.safe_load(f)
                for card_data in card_list:
                    # 自动生成 ID
                    card_id = f"card_{self.id_counter}"
                    self.id_counter += 1
                    card_data["id"] = card_id

                    name = card_data["name"]
                    card_data = Card(**card_data)
                    self.cards_by_id[card_id] = card_data
                    self.cards_by_name[name] = card_data
    
    def get_card_by_id(self, card_id: str) -> Card | None:
        """Get a card by its ID."""
        try:
            return self.cards_by_id.get(card_id)
        except Exception as e:
            logger.error(f"Invalid card ID: {card_id}. Error: {e}")
            return None
    
    def get_card_by_name(self, name: str) -> Card | None:
        """Get a card by its name."""
        try:
            return self.cards_by_name.get(name)
        except Exception as e:
            logger.error(f"Invalid card name: {name}. Error: {e}")
            return None

card_registry = CardRegistry("asset/cards")