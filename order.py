from enum import Enum
class Order:
    '''
    Order for command.
    '''
    PLAY_CARD="pl"
    MOVE_ATK="mv"
    END_TURN="end"
    def __init__(self, command_str:str):
        '''
        Parse the order.
        '''
        commands=command_str.split(" ")
        command,args=commands[0],commands[1:]

        # play card: pl #card_id args
        if command == Order.PLAY_CARD:
            self.type=Order.PLAY_CARD
            assert '#' in args[0] and args[0].index('#')==0
            self.card_idx=int(args[0][1:])
            self.args=args[1:]
        # move and attack: mv from(line,pos) to（line,pos)
        elif command== Order.MOVE_ATK:
            self.type=Order.MOVE_ATK
            self._from=args[0]
            self._to=args[1]
            assert len(self._from)==2 and len(self._to)==2
            assert self._from[0] in ['s','f']
            assert self._to[0] in ['e','f']
            assert self._from!=self._to
            assert int(self._from[1]) in range(5)
            assert int(self._to[1]) in range(5)
            
        elif command == Order.END_TURN:
            self.type=Order.END_TURN
            
        else:
            raise ValueError("Invalid command")
        