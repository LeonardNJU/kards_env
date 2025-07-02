from game.utils import get_opponent_player_id
from object.unit import Unit
from utils.constant import FIELD_WIDTH, ROW_SIZE_MAX, ROW_TOTAL, CARD_HEIGHT, FRONT_ROW
from object.object import Object
from utils.logger import setup_logger

logger = setup_logger(__name__)




class Field:
    class _Row:
        def __init__(self) -> None:
            self.objects = []

        # Show
        def debug_show(self):
            """Show the objects in the row."""
            for obj in self.objects:
                print(obj, end=" ")
            print()
    
        def render(self, width: int = 16) -> str:
            """
            Render a row of objects as an ASCII art representation.
        
            :param self: The Row object containing the objects to render.
            :param width: The width of each object in the row.
            :return: A string representation of the row.
            """
            # only front row can be empty
            if self.is_empty():
                upper_half = "\n" * ((CARD_HEIGHT-1)//2)
                lower_half = "\n" * ((CARD_HEIGHT-1)//2)
                return upper_half + "=" * (width * ROW_SIZE_MAX) + lower_half
    
            lines = []
            top = "┌" + "─" * (width - 2) + "┐"
            lines.extend(top for _ in range(len(self.objects)))
            lines.append("\n")
            lines.extend(f"│ {obj.name[:width-4].center(width - 4)} │" for obj in self.objects)
            lines.append("\n")
            lines.extend("│" + " " * (width - 2) + "│" for _ in self.objects)
            lines.append("\n")
            for obj in self.objects:
                if isinstance(obj, Unit):
                    total_length=len(str(obj.atk)) + len(str(obj.HP)) + 3
                    stats_line = f'│ {f"{obj.atk}".ljust(width - total_length)}{obj.HP} │'
                else:
                    total_length=len(str(obj.HP)) + 4
                    stats_line = f'│ {"".ljust(width - total_length)}{obj.HP} │'
                lines.append(stats_line)
            lines.append("\n")
            lines.extend("└" + "─" * (width - 2) + "┘" for _ in range(len(self.objects)))
            lines.append("\n")
    
            return "".join(lines)
    
        # Query
        def is_full(self):
            return len(self.objects) >= ROW_SIZE_MAX
        def is_empty(self):
            return len(self.objects) == 0
        def size(self):
            return len(self.objects)
        def find(self, obj: Object) -> int:
            """Find the index of an object in the row.
            
            Args:
                obj (Object): The object to be found.
                
            Returns:
                int: The index of the object in the row.
                
            Raises:
                ValueError: If the object is not found in the row.
            """
            return self.objects.index(obj)
    
        # Manipulate
        def insert_object(self, obj: Object, col: int | None = None):
            """Insert an object into the row at the specified column or append to the end.
            
            Args:
                obj (Object): The object to be inserted.
                col (int | None, optional): The column index to insert the object at. If None, appends to the end.
            
            Raises:
                ValueError: If the row is already full.
            """
            if len(self.objects) >= ROW_SIZE_MAX:
                raise ValueError(f"Row is full, cannot insert object {obj}.")
            if col is not None:
                self.objects.insert(col, obj)
            else:
                self.objects.append(obj)
    
        def pop(self, idx: int):
            """Remove and return the object at the specified index. And move all objects after it one step to the left.
    
            Args:
                idx (int): The index of the object to be removed.
                
            Returns:
                Object: The removed object.
                
            Raises:
                IndexError: If the index is out of range.
            """
            if idx < 0 or idx >= len(self.objects):
                raise IndexError(
                    f"Index {idx} out of range for row with {len(self.objects)} objects."
                )
            return self.objects.pop(idx)
        
    class Position:
        """A class to represent a position on the field."""
        def __init__(self, row: int, col: int):
            if row < 0 or row >= ROW_TOTAL:
                raise ValueError(f"Row index {row} out of range. Must be between 0 and {ROW_TOTAL - 1}.")
            if col < 0 or col >= ROW_SIZE_MAX:
                raise ValueError(f"Column index {col} out of range. Must be between 0 and {ROW_SIZE_MAX - 1}.")
            self.row = row
            self.col = col

        def __str__(self):
            return f"Position(row={self.row}, col={self.col})"

    @staticmethod
    def player_id_to_row(player_id: int) -> int:
        # noinspection PyUnreachableCode
        match player_id:
            case 0:
                return 0  # Player 1's row
            case 1:
                return 2  # Player 2's row
            case _:
                raise ValueError(f"Invalid player ID: {player_id}. Must be 0 or 1.")

    def __init__(self):
        """Initialize the field with an empty list of objects."""
        self._rows = [Field._Row() for _ in range(ROW_TOTAL)]
        self.front_control = None
        
    def _get_row(self, row: int) -> _Row:
        """Get the row at the specified index."""
        if 0 <= row < ROW_TOTAL:
            return self._rows[row]
        raise IndexError(f"Row index {row} out of range. Must be between 0 and {ROW_TOTAL - 1}.")

    def _flush_front_control(self):
        if self._rows[FRONT_ROW].is_empty():
            self.front_control = None

    def _remove(self, obj: Object):
        """Remove an object from the field.

        Args:
            obj (Object): The object to be removed.
            
        Raises:
            ValueError: If the object is not found in the field.
        """
        for i, row in enumerate(self._rows):
            try:
                idx=row.find(obj)
                if i== FRONT_ROW: self._flush_front_control()
                row.pop(idx)
            except ValueError:
                continue
        raise ValueError(f"Object {obj} not in field.")

    # Show
    def field_render(self, perspective_id: int):
        """show the field in current player's perspective."""
        res=""
        opponent_id = get_opponent_player_id(perspective_id)
        res+=self._get_row(opponent_id).render()
    
        if self.front_control == perspective_id:
            res+=("-" * FIELD_WIDTH+'\n')
        res+=self._get_row(FRONT_ROW).render()
        if self.front_control == opponent_id:
            res+=("-" * FIELD_WIDTH+'\n')
        res+=self._get_row(perspective_id).render()
    
        return res

    def debug_show(self, current_player_num: int):
        """show the field in current player's perspective."""
        opponent_num = (current_player_num + 1) % 2
        self._rows[Field.player_id_to_row(opponent_num)].debug_show()  # Show the row with HQs
        if self.front_control == current_player_num:
            print("-" * FIELD_WIDTH)
        if self.front_control != -1:
            self._rows[1].debug_show()
        else:
            print("=" * FIELD_WIDTH)
        if self.front_control == opponent_num:
            print("-" * FIELD_WIDTH)
        self._rows[
            Field.player_id_to_row(current_player_num)
        ].debug_show()  # Show the row with units

    # Queries
    def get_object(self, pos: Position) -> Object:
        """Get the object at the specified position.

        Args:
            pos (Position): The position of the object.

        Returns:
            Object: The object at the specified position.

        Raises:
            IndexError: If the position is out of range.
        """
        if pos.col >= self._get_row(pos.row).size():
            raise IndexError(f"Column index {pos.col} out of range for row {pos.row}.")
        return self._rows[pos.row].objects[pos.col]


    # Manipulate
    # noinspection PyStatementEffect
    def check_place(self, obj: Object, row: int, col: int | None = None):
        """Check if can an object be inserted into the field at a specified row and column.

        Args:
            obj (Object): The object to be inserted.
            row (int): The row index where the object will be inserted. From 0 to ROW_SIZE_MAX-1.
            col (int | None, optional): The column index where the object will be inserted. Defaults to None for appending to the end of the row.

        Returns:
            bool: True if the object can be placed, False otherwise.
        """
        obj
        col
        if row < 0 or row >= ROW_TOTAL:
            logger.warning(f"Row index {row} out of range. Must be between 0 and {ROW_TOTAL - 1}.")
            return False
        return not self._rows[row].is_full()
    def exec_place(self, obj: Object, row: int, col: int | None = None):
        """Insert an object into the field at a specified row and column.

        Args:
            obj (Object): The object to be inserted.
            row (int): The row index where the object will be inserted. From 0 to ROW_SIZE_MAX-1.
            col (int | None, optional): The column index where the object will be inserted. Defaults to None for appending to the end of the row.

        Returns:
            Object: None if insert was successful, or the object if the row is full.

        Shouldn't be used directly, use `check_place` first.
        """
        return self._rows[row].insert_object(obj, col)

    def check_move(self, _from: Position, _to: Position):
        """Check if a unit can be moved from one position to another.

        Checker for distance and availability of the move in field.
        Other checker for whether the unit can move is in `Unit`
        Checker for whether player can move a unit to the front line is in `Game`.

        Args:
            _from (Position): The starting position of the unit.
            _to (Position): The target position of the unit.

        Returns:
            bool: True if the move is valid, False otherwise.
        """
        if _from.row == FRONT_ROW or _to.row != FRONT_ROW:
            logger.warning("Move can only be made from support row to front row.")
            return False

        if self._rows[FRONT_ROW].is_full():
            logger.warning("Front row is full, cannot move into it.")
            return False

        unit = self.get_object(_from)
        if self.front_control is not None and self.front_control != unit.owner:
            logger.warning("cannot move to the front line controlled by the opponent.")
            return False

        return True
    def exec_move(self, _from: Position, _to: Position):
        """Move a unit from one position to another.

        Should be used only after `check_move` is called and returned True.
        Args:
            _from (int): The starting position of the unit.
            _to (int): The target position of the unit.
        """
        obj= self.get_object(_from)
        self._remove(obj)
        self._rows[_to.row].insert_object(obj, _to.col)
        if self.front_control is None:
            self.front_control = obj.owner
