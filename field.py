from operator import is_
from re import A
from const import SpecialAbility, UnitType
from object import Object
from units.unit import Unit


class Row:
    def __init__(self):
        self.slots = [None] * 5
        self.size=0
    def __str__(self):
        return "\t".join([str(slot) for slot in self.slots if slot])
    def join(self, object:Object, position:int=None):
        """
        join a unit to the row, fall to left
        """
        if position is None:
            position = self.size
        assert self.size<=5, "Row is full"
        assert position in range(5), "Position out of range"
        if self.slots[position] is not None:
            for i in range(4, position, -1):
                self.slots[i] = self.slots[i-1]
        else:
            while position>0 and self.slots[position - 1] is None:
                position -= 1
        self.slots[position] = object
        self.size+=1
    def remove(self, position:int):
        """
        remove a unit from the row
        """
        assert position in range(5), "Position out of range"
        if self.slots[position] is None:
            raise ValueError("No unit in the position")
        self.slots[position] = None
        self.size-=1
        if position<4 and self.slots[position+1] is not None:
            for i in range(position, 4):
                self.slots[i] = self.slots[i+1]
                
    def is_full(self):
        return self.slots[4] is not None
    def is_empty(self):
        return self.slots[0] is None
    
class Field:
    def __init__(self):
        self.player_rows = [None,Row(),Row()]
        self.front_row = Row()
        self.front_control = None   # None, 1 or 2
    def __str__(self,current_player:int):
        result= ""
        boarder_str="f  ==============================================\n"
        thin_boarder_str="-----------------------------------------------\n"
        opposite_player=3-current_player
        result+="e  "+str(self.player_rows[opposite_player])+"\n"
        if self.front_control==opposite_player:
            result+="f  "+str(self.front_row)+"\n"
            result+=thin_boarder_str
        elif self.front_control==current_player:
            result+=thin_boarder_str
            result+="f  "+str(self.front_row)+"\n"
        else:
            result+=boarder_str
        result+=f"s  {self.player_rows[current_player]}\n"
        return result

    def get_self_unit(self, player_id:int, position:str)->Unit:
        """
        get unit for player
        """
        assert player_id in [1,2], "Invalid player id"
        assert position[0] in ['s','f'] and int(position[1]) in range(5), "Invalid position"
        if position[0]=='s':
            position=int(position[1])
            unit=self.player_rows[player_id].slots[position]
        elif position[0]=='f':
            if self.front_control==player_id:
                position=int(position[1])
                unit=self.front_row.slots[position]
            else:
                raise ValueError("You don't control the front row")
        else:
            raise ValueError("Invalid position")
        if unit is None or isinstance(unit, Unit)==False:
            raise ValueError("No unit in the position")
        return self.player_rows[player_id].slots[position]
    def get_enemy_object(self, player_id:int, position:str)->Object:
        """
        get Object for player
        """
        assert player_id in [1,2], "Invalid player id"
        assert position[0] in ['e','f'] and int(position[1]) in range(5), "Invalid position"
        if position[0]=='e':
            position=int(position[1])
            unit=self.player_rows[3-player_id].slots[position]
        elif position[0]=='f':
            if self.front_control!=player_id:
                position=int(position[1])
                unit=self.front_row.slots[position]
            else:
                raise ValueError("Please selected enemy unit")
        else:
            raise ValueError("Invalid position")
        if unit is None:
            raise ValueError("No unit in the position")
        return self.player_rows[player_id].slots[position]
    
    def move_to_front(self, game, player_id:int, _from:str, position:int)->bool:
        '''
        move into uncontrolled front row or self controlled front row
        position checked in 1-5, not checked if line to join is full
        '''
        # check if able to move
        if self.front_row.is_full():
            raise ValueError("Front row is full")
        unit=self.get_self_unit(player_id, _from)
        if game.players[player_id].mana<unit.oil:
            raise ValueError("Not enough oil")

        # check if unit can move
        unit.move_to_front(game)
        
        # now control field
        self.front_row.join(unit, position)
        self.player_rows[player_id].remove(int(_from[1]))
        game.players[player_id].mana-=unit.oil
    
    def unit_attack(self, game,player_id:int, _from:str, _to:str)->bool:
        '''
        first to check if unit can attack,
        then attack.
        '''
        unit=self.get_self_unit(player_id, _from)
        if game.players[player_id].mana<unit.oil:
            raise ValueError("Not enough oil")
        
        # check if able to attack
        unit.able_to_atk()
        if unit.type in [UnitType.INFANTRY]:
            # check attacking range, including distance and guard and smoke
            # distance
            if (_from[0],_to[0]) not in [('s','f'),('f','e')]:
                raise ValueError("Attacking Range too short")
            # guard
            enemy=self.get_enemy_object(player_id, _to)
            if not isinstance(enemy,Unit) or (isinstance(enemy,Unit) and SpecialAbility.GUARD not in enemy.ability):
                pos=int(_to[1])
                if pos>0:
                    enemy_left=self.get_enemy_object(player_id,_to[0]+str(pos-1))
                    if isinstance(enemy_left, Unit) and SpecialAbility.GUARD in enemy.ability:
                        raise ValueError("Object has been guarded")
                if pos<4:
                    enemy_right=self.get_enemy_object(player_id,_to[0]+str(pos+1))
                    if isinstance(enemy_right, Unit) and SpecialAbility.GUARD in enemy.ability:
                        raise ValueError("Object has been guarded")
            # smoke
            if isinstance(enemy,Unit) and SpecialAbility.SMOKE in enemy.ability:
                raise ValueError("Object has been smoked")
        # TODO: other type
        
        # can attack
        unit.attack(self.get_enemy_object(player_id, _to))
        game.players[player_id].mana-=unit.oil
        
    
    def move_atk(self,game,player_id:int, _from:str, _to:str):
        """
        get target for player
        """
        assert player_id in [1,2], "Invalid player id"
        assert _to[0] in ['e','f'] and int(_to[1]) in range(5), "Invalid position"
        
        if _to[0]=='e':
            target=self.player_rows[player_id].slots[int(_to[1])]  # attack
        elif _to[0]=='f':
            if self.front_control==player_id or self.front_control==None:
                self.move_to_front(game,player_id, _from, int(_to[1]))
            else:
                target=self.front_row.slots[int(_to[1])]           # attack
        else:
            raise ValueError("Invalid position")
        
        if target is None:
            raise ValueError("No attacking target in the position")
        
        self.unit_attack(game, player_id, _from, _to)