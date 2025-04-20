from __future__ import annotations
# from game import Game
from units.unit_light_infantry import Unit_light_Infantry
from units.unit_15th_CAVALRY import Unit_15th_CAVALRY
from card import EffectMeta, ParamSpec
from typing import Callable, List, Dict

effect_registry: Dict[str, EffectMeta] = {}

# 装饰器：用于自动注册函数为 EffectMeta
def register_effect(name: str, params: List[ParamSpec]):
    def decorator(func: Callable):
        effect_registry[name] = EffectMeta(func=func, params=params)
        return func
    return decorator

@register_effect(
    name="部署轻步兵",
    params=[ParamSpec("position", int, "部署的位置（0~4）")]
)
def card_light_infantry(game, player: int, position: int):
    unit=Unit_light_Infantry()
    game.field.player_rows[player].join(unit, position)
    unit.set_putting(game,player)
    
@register_effect(
    name="部署习致野",
    params=[ParamSpec("position", int, "部署的位置（0~4）")]
)
def card_15th_cavalry(game, player: int, position: int):
    unit=Unit_15th_CAVALRY()
    game.field.player_rows[player].join(unit, position)
    unit.set_putting(game,player)