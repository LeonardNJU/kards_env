from field import Field
from units.light_infantry import LightInfantry
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
    name="light_infantry",
    params=[ParamSpec("position", int, "部署的位置（0~4）")]
)
def light_infantry_card(field: Field, player: int, position: int):
    field.player_rows[player].join(LightInfantry(), position)
