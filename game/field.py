from utils.constant import FIELD_WIDTH, ROW_SIZE_MAX, ROW_TOTAL
from object.object import Object
from utils.logger import setup_logger

logger = setup_logger(__name__)


class Field:
    def __init__(self):
        """Initialize the field with an empty list of objects."""
        self.field = [Row() for _ in range(ROW_TOTAL)]
        self.front_control = -1
    
    def insert_object(self, obj:Object, row:int, col:int|None = None):
        """Insert an object into the field at a specified row and column.

        Args:
            obj (Object): The object to be inserted.
            row (int): The row index where the object will be inserted. From 0 to ROW_SIZE_MAX-1.
            col (int | None, optional): The column index where the object will be inserted. Defaults to None for appending to the end of the row.

        Returns:
            Object: None if insert was successful, or the object if the row is full.
        """
        return self.field[row].insert_object(obj, col)

        
    @staticmethod
    def player_id_to_row(player_id:int) -> int:
        match player_id:
            case 0:
                return 0  # Player 1's row
            case 1:
                return 2  # Player 2's row
            case _:
                raise ValueError(f"Invalid player ID: {player_id}. Must be 0 or 1.")
            
    def show(self, current_player_num:int):
        """show the field in current player's perspective."""
        opponent_num = (current_player_num + 1) % 2
        self.field[Field.player_id_to_row(opponent_num)].show()  # Show the row with HQs
        if self.front_control==current_player_num:print('-'*FIELD_WIDTH)
        if self.front_control !=-1:
            self.field[1].show()
        else:
            print('='*FIELD_WIDTH)
        if self.front_control==opponent_num:print('-'*FIELD_WIDTH)
        self.field[Field.player_id_to_row(current_player_num)].show()  # Show the row with units
        
class Row:
    def __init__(self) -> None:
        self.objects=[]
    def insert_object(self, obj:Object, col:int|None = None):
        """Insert an object into the row."""
        if len(self.objects)>=ROW_SIZE_MAX:
            logger.info(f"Row is full, cannot insert object {obj}.")
            return obj
        if col is not None:
            self.objects.insert(col, obj)
        else:
            self.objects.append(obj)
        logger.info(f"Inserted object {obj} into row.")
        return obj
    def show(self):
        """Show the objects in the row."""
        for obj in self.objects:
            print(obj, end=" ")
        print()