import os
import yaml
from object.unit import Unit
from utils.logger import setup_logger
logger = setup_logger(__name__)

class UnitRegistry:
    def __init__(self, unit_dir: str):
        self.units_by_id :dict[str, Unit]= {}
        self.units_by_name :dict[str, Unit] = {}
        self.id_counter = 0
        self.load_units(unit_dir)

    def load_units(self, unit_dir: str):
        for fname in os.listdir(unit_dir):
            if not fname.endswith(".yaml"):
                continue
            with open(os.path.join(unit_dir, fname), 'r', encoding='utf-8') as f:
                unit_list = yaml.safe_load(f)
                for unit_data in unit_list:
                    # 自动生成 ID
                    unit_id = f"unit_{self.id_counter}"
                    self.id_counter += 1
                    unit_data["id"] = unit_id

                    name = unit_data["name"]
                    unit_data = Unit(**unit_data)
                    self.units_by_id[unit_id] = unit_data
                    self.units_by_name[name] = unit_data
    
    def get_unit_by_id(self, unit_id: str) -> Unit | None:
        """Get a unit by its ID."""
        try:
            return self.units_by_id.get(unit_id)
        except Exception as e:
            logger.error(f"Invalid unit ID: {unit_id}. Error: {e}")
            return None
    
    def get_unit_by_name(self, name: str) -> Unit:
        """Get a unit by its name."""
        unit = self.units_by_name.get(name)
        if unit is None:
            logger.error(f"Invalid unit name: {name}. Unit not found.")
            raise ValueError(f"Invalid unit name: {name}. Unit not found.")
        return unit

unit_registry = UnitRegistry("asset/units")