from dataclasses import dataclass, field
from typing import Any, List
from utils.symbols import CardType, Nation

from utils.logger import setup_logger
logger = setup_logger(__name__)


@dataclass
class Card:
    id: int
    name: str
    nation: Nation
    type: CardType
    kredits: int
    effects: List[dict] = field(default_factory=list)  # List of effects, each effect is a dict with 'action' and other keys
    params: List[dict] = field(default_factory=list)  # List of parameters, each param is a dict with 'name', 'type' and 'desc'
    def __repr__(self):
        return f"Card({self.id}, {self.name}, {self.nation}, {self.type}, {self.kredits}, {self.effects})"
    
    def params_str(self):
        """Show the parameters of the card."""
        if not self.params:
            return "<No parameters>"
        return ", ".join(f"{param['name']} ({param['type']})" for param in self.params)
    
    def args_bind(self, args: List[str]) -> dict[str, Any]:
        """Check if the given arguments match the card's parameters."""
        if len(args) != len(self.params):
            logger.warning(f"Invalid number of arguments for card {self.name}: expected {len(self.params)}, got `{len(args)}`.")
            logger.warning(f"Card params: {self.params_str()}")
            raise ValueError(f"Invalid number of arguments for card {self.name}: expected {len(self.params)}, got `{len(args)}`.")
        args_map = {}
        for i, param in enumerate(self.params):
            if param["type"] == "int":
                try:
                    args_map[param['name']] = int(args[i])
                except ValueError as e:
                    logger.warning(f"Invalid argument for parameter {param['name']}: expected int, got {args[i]}")
                    logger.warning(f"Card params: {self.params_str()}")
                    raise ValueError(
                        f"Invalid argument for parameter {param['name']}: expected int, got {args[i]}"
                    ) from e
            else:
                logger.error(f"Unknown parameter type {param['type']} for card {self.name}.")
                raise ValueError(f"Unknown parameter type {param['type']} for card {self.name}.")
        return args_map