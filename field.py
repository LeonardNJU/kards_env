from object import Object


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
        
class Field:
    def __init__(self):
        self.player1_row = Row()
        self.player2_row = Row()
        self.front_row = Row()
        self.front_control = None   # None, 1 or 2
    def __str__(self,current_player:int):
        result= ""
        boarder_str="=================================================\n"
        thin_boarder_str="-----------------------------------------------\n"
        if current_player==2:
            result+=str(self.player1_row)+"\n"
            if self.front_control==1:
                result==str(self.front_row)+"\n"
                result+=thin_boarder_str
            elif self.front_control==2:
                result+=thin_boarder_str
                result+=str(self.front_row)+"\n"
            else:
                result+=boarder_str
            result+=str(self.player2_row)+"\n"
        elif current_player==1:
            result+=str(self.player2_row)+"\n"
            if self.front_control==1:
                result+=thin_boarder_str
                result+=str(self.front_row)+"\n"
            elif self.front_control==2:
                result+=str(self.front_row)+"\n"
            else:
                result+=boarder_str
            result+=str(self.player1_row)+"\n"
        else:
            raise ValueError("Invalid current player")
        return result
    