from const import DamageSource, Nation, SpecialAbility, UnitType
from object import Object


class Unit(Object):
    def __init__(self, name:str, type:UnitType, nation:Nation, HP:int, ATK:int, oil:int, DEF:int=0,special_ability:list[SpecialAbility]=None):
        super().__init__(HP,nation)
        self.name = name
        self.ATK = ATK
        self.DEF = DEF
        self.oil = oil
        self.type = type
        
        self.is_moved = False
        self.have_attacked = 0
        
        self.ability = [] if special_ability is None else special_ability
        
        self.on_front=False
    def __str__(self):
        return f"{self.name}({self.ATK}/{self.HP})"
    
    def set_putting(self, game, player:int):
        self.game=game
        self.owner=player
        self.putting_turn=game.turn
        self.is_moved=False
        self.have_attacked=0
    
    def reset(self):
        self.is_moved=False
        self.have_attacked=0
    
    def is_putted_this_turn(self)->bool:
        return self.putting_turn==self.game.turn
    
    def move_to_front(self, game):
        if self.on_front:
            raise ValueError("Already on front row")
        if self.is_moved:
            raise ValueError("Already moved")
        if self.putting_turn is None:
            raise ValueError("Not putted yet")
        if self.is_putted_this_turn() and SpecialAbility.BLITZ not in self.ability:
            raise ValueError("Can't move in same turn as putted")
        if self.have_attacked>0  and self.type!=UnitType.TANK and SpecialAbility.ATKWITHMOVE not in self.ability:
            raise ValueError("Already attacked")
        
        self.on_front=True
        self.is_moved=True
        
        if game.field.front_control==None:
            game.field.front_control=self.owner
        
    def able_to_atk(self):
        if self.is_putted_this_turn() and SpecialAbility.BLITZ not in self.ability:
            raise ValueError("Can't attack in same turn as putted")
        if self.is_moved and self.type!=UnitType.TANK and SpecialAbility.ATKWITHMOVE not in self.ability:
            raise ValueError("Can't move and attack in same turn")
        if self.have_attacked>0 and SpecialAbility.DOUBLEHIT not in self.ability:
            raise ValueError("Can't attack twice")
        if SpecialAbility.DOUBLEHIT in self.ability and self.have_attacked>1:
            raise ValueError("Already attacked twice")
        return True
    
    def attack(self, target:Object):
        target.hurt(self.ATK, DamageSource.UNITATK)
        if SpecialAbility.SHOCK not in self.ability and isinstance(target, Unit):
            self.hurt(target.ATK, target)
        self.have_attacked+=1
    
    def die(self):
        # notify the game the unit is dead
        self.game.field.remove_unit(self.owner, self)
        del self