from dataclasses import dataclass
from typing import Callable, List
from const import CardType, Nation

@dataclass
class ParamSpec:
    name: str
    type: type
    description: str = ""

@dataclass
class EffectMeta:
    func: Callable
    params: List[ParamSpec]

class Card:
    def __init__(self, name: str, cost: int, meta: EffectMeta, type: CardType, nation: Nation):
        self.name = name
        self.cost = cost
        self.meta = meta
        self.type = type
        self.nation = nation

    def play(self, game, player: int, args: List[str]):
        parsed = []
        for i, param in enumerate(self.meta.params):
            try:
                parsed.append(param.type(args[i]))
            except:
                raise ValueError(f"参数 {param.name} 类型错误，应为 {param.type.__name__}，收到：{args[i]}")
        self.meta.func(game, player, *parsed)

    def __str__(self):
        return f"{self.cost}K {self.name} {self.type.value} {self.nation.value}"
    def describe(self):
        print(self)
        for p in self.meta.params:
            print(f"  - {p.name} ({p.type.__name__})：{p.description}")

