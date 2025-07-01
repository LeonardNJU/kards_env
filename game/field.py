from game.utils import get_opponent_player_id
from object.unit import Unit
from utils.constant import FIELD_WIDTH, ROW_SIZE_MAX, ROW_TOTAL
from object.object import Object
from utils.logger import setup_logger

logger = setup_logger(__name__)

class Row:
    def __init__(self) -> None:
        self.objects = []

    def insert_object(self, obj: Object, col: int | None = None):
        """Insert an object into the row."""
        if len(self.objects) >= ROW_SIZE_MAX:
            logger.warning(f"Row is full, cannot insert object {obj}.")
            return obj
        if col is not None:
            self.objects.insert(col, obj)
        else:
            self.objects.append(obj)
        logger.debug(f"Inserted object {obj} into row.")
        return obj

    def show(self):
        """Show the objects in the row."""
        for obj in self.objects:
            print(obj, end=" ")
        print()

    def is_full(self):
        """Check if the row is full."""
        return len(self.objects) >= ROW_SIZE_MAX

    def is_empty(self):
        """Check if the row is empty."""
        return len(self.objects) == 0

    def pop(self, idx: int):
        """Remove and return the object at the specified index. And move all objects after it one step to the left.

        Args:
            idx (int): The index of the object to be removed.
        """
        if idx < 0 or idx >= len(self.objects):
            raise IndexError(
                f"Index {idx} out of range for row with {len(self.objects)} objects."
            )
        obj = self.objects.pop(idx)
        logger.debug(f"Removed object {obj} from row at index {idx}.")
        return obj


class Field:
    def __init__(self):
        """Initialize the field with an empty list of objects."""
        self.rows = [Row() for _ in range(ROW_TOTAL)]
        self.front_control = -1
    def get_my_row(self, player_id: int) -> Row:
        return self.rows[Field.player_id_to_row(player_id)]
    def get_front_row(self) -> Row:
        return self.rows[1]
    def get_opponent_row(self, player_id: int) -> Row:
        return self.rows[Field.player_id_to_row(get_opponent_player_id(player_id))]
    

    def insert_object(self, obj: Object, row: int, col: int | None = None):
        """Insert an object into the field at a specified row and column.

        Args:
            obj (Object): The object to be inserted.
            row (int): The row index where the object will be inserted. From 0 to ROW_SIZE_MAX-1.
            col (int | None, optional): The column index where the object will be inserted. Defaults to None for appending to the end of the row.

        Returns:
            Object: None if insert was successful, or the object if the row is full.
        """
        return self.rows[row].insert_object(obj, col)

    @staticmethod
    def player_id_to_row(player_id: int) -> int:
        match player_id:
            case 0:
                return 0  # Player 1's row
            case 1:
                return 2  # Player 2's row
            case _:
                raise ValueError(f"Invalid player ID: {player_id}. Must be 0 or 1.")

    def show(self, current_player_num: int):
        """show the field in current player's perspective."""
        opponent_num = (current_player_num + 1) % 2
        self.rows[Field.player_id_to_row(opponent_num)].show()  # Show the row with HQs
        if self.front_control == current_player_num:
            print("-" * FIELD_WIDTH)
        if self.front_control != -1:
            self.rows[1].show()
        else:
            print("=" * FIELD_WIDTH)
        if self.front_control == opponent_num:
            print("-" * FIELD_WIDTH)
        self.rows[
            Field.player_id_to_row(current_player_num)
        ].show()  # Show the row with units

    def flush_front_control(self):
        if self.rows[1].is_empty():
            self.front_control = -1

    def remove(self, obj: Object):
        """Remove an object from the field.

        Args:
            obj (Object): The object to be removed.
        """
        for row in self.rows:
            if obj in row.objects:
                row.objects.remove(obj)
                logger.debug(f"Removed object {obj} from field.")
                self.flush_front_control()
                return
        logger.warning(f"Object {obj} not found in field.")

    def move_unit(self, fr: int, to: int, owner_id: int, owner_kredits: int):
        """Move a unit from one position to another. Actually from 'support row `fr` col' to 'front row `to` col'.

        Args:
            fr (int): The starting position of the unit.
            to (int): The target position of the unit.
            owner_id (int): The ID of the player who owns the unit.

        Returns:
            bool: True if the move was successful, False otherwise.
        """
        # if front line is controlled by the opponent, do not allow moving units to it
        if self.front_control == get_opponent_player_id(owner_id):
            logger.warning(
                f"Player {owner_id} tried to move a unit to the opponent's front line."
            )
            return False

        # if front line is full
        if self.rows[1].is_full():
            logger.warning(
                f"Player {owner_id} tried to move a unit to the front line, but it is full."
            )
            return False

        obj = self.rows[Field.player_id_to_row(owner_id)].objects[fr]
        # then can move as long as the unit can move
        if obj and isinstance(obj, Unit) and obj.can_move():
            # if owner don;t have enough kredits to move the unit
            if owner_kredits < obj.oil:
                logger.warning(
                    f"Player {owner_id} tried to move a unit without enough kredits."
                )
                return False
            try:
                moved_obj = self.rows[Field.player_id_to_row(owner_id)].pop(fr)
                self.rows[1].insert_object(moved_obj, to)
                self.front_control = owner_id
                moved_obj.moved()
                logger.info(
                    f"Moved unit {moved_obj} from row {Field.player_id_to_row(owner_id)} col {fr} to front row col {to}."
                )
                return True
            except IndexError as e:
                logger.warning(f"Error moving unit: {e}")
                return False

    def get_obj_by_pos(self, pos: str, perspective_id: int) -> Object | None:
        """Get the object at the specified position.

        Args:
            pos (str): The row index of the object. like 's0', 'f1', 'e4'
            to (str): The column index of the object. like 'f3', 'e4'
            owner_id (int): The ID of the player who owns the object.

        Returns:
            Object: The object at the specified position, or None if not found.
        """
        if len(pos) == 2 and pos[0] in "sfe" and pos[1].isdigit():
            row = (
                1
                if pos[0] == "f"
                else (
                    self.player_id_to_row(perspective_id)
                    if pos[0] == "s"
                    else self.player_id_to_row(get_opponent_player_id(perspective_id))
                )
            )
            col = int(pos[1])
            return (
                self.rows[row].objects[col]
                if col < len(self.rows[row].objects)
                else None
            )
        return None

