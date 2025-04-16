from const import UnitType
from object import Object
from units.unit import Unit


class Row:
    def __init__(self):
        self.slots = [None] * 5
        self.size=0
    def __str__(self):
        return "\t".join([str(slot) for slot in self.slots if slot])
    def join(self, object:Object, positon:int=None):
        if positon is None:
            positon = self.size
        assert self.size<=5, "Row is full"
        assert positon in range(5), "Position out of range"
        if self.slots[positon] is not None:
            for i in range(4, positon, -1):
                self.slots[i] = self.slots[i-1]
        self.slots[positon] = object
        self.size+=1
        
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
    def move_atk(self, current_player:int,_from:str,_to:str):
        """
        Move and attack.
        """
        # get object
        unit:Unit=None
        if _from[0]=='s':
            unit=self.player_rows[current_player].slots[int(_from[1])]
        elif _from[0]=='f':
            if not self.front_control==current_player:
                raise ValueError("You don't control the front row")
            unit=self.front_row.slots[int(_from[1])]
        if unit is None:
            raise ValueError("No unit in the position")

        # if unit.oil>
        # if unit.is_frozen(): 

        # check to position
        opposite=3-current_player
        # attack
        if _to[0]=='e' or (_to[0]=='f' and self.front_controls==opposite):    # attack enemy
            target=None
            if _to[0]=='e':
                target=self.player_rows[opposite].slots[int(_to[1])]
            elif _to[0]=='f':
                target=self.front_row.slots[int(_to[1])]
            if target is None:
                raise ValueError("No attacking target in the position")

            # check if able to attack
            if unit.type==UnitType.INFANTRY:
                pass
            # unit.attack(target)