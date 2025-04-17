from const import SpecialAbility, UnitType
from object import Object


class Unit(Object):
    def __init__(self, name:str, type:UnitType, HP:int, ATK:int, oil:int, DEF:int=0,special_ability:list[SpecialAbility]=None):
        super().__init__(HP)
        self.name = name
        self.ATK = ATK
        self.DEF = DEF
        self.oil = oil
        self.type = type
        
        self.is_moved = False
        self.have_attacked = False
        
        self.ability = [] if special_ability is None else special_ability
        
        self.on_front=False
    def __str__(self):
        return f"{self.name}({self.ATK}/{self.HP})"
    
    def set_putting(self,player:int,turn:int):
        self.owner=player
        self.putting_turn=turn
        self.is_moved=False
        self.have_attacked=False
    
    def move_to_front(self, game):
        if self.on_front:
            raise ValueError("Already on front row")
        if self.is_moved:
            raise ValueError("Already moved")
        if self.putting_turn is None:
            raise ValueError("Not putted yet")
        if self.putting_turn==game.turn and SpecialAbility.BLITZ not in self.ability:
            raise ValueError("Can't move this turn")
        if self.have_attacked and self.type!=UnitType.TANK and SpecialAbility.ATKWITHMOVE not in self.ability:
            raise ValueError("Already attacked")
        
        self.on_front=True
        self.is_moved=True
        
        if game.field.front_control==None:
            game.field.front_control=self.owner
        
        