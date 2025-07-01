from game.field import Row
from object.unit import Unit
from utils.constant import CARD_HEIGHT, ROW_SIZE_MAX


def row_render(row: Row, width: int = 16) -> str:
    """
    Render a row of objects as an ASCII art representation.

    :param row: The Row object containing the objects to render.
    :param width: The width of each object in the row.
    :return: A string representation of the row.
    """
    if row.is_empty():
        upper_half = "\n" * ((CARD_HEIGHT-1)//2)
        lower_half = "\n" * ((CARD_HEIGHT-1)//2)
        return upper_half + "=" * (width * ROW_SIZE_MAX) + lower_half

    lines = []
    top = "┌" + "─" * (width - 2) + "┐"
    lines.extend(top for _ in range(len(row.objects)))
    lines.append("\n")
    lines.extend(f"│ {obj.name[:width-4].center(width - 4)} │" for obj in row.objects)
    lines.append("\n")
    lines.extend("│" + " " * (width - 2) + "│" for _ in row.objects)
    lines.append("\n")
    for obj in row.objects:
        if isinstance(obj, Unit):
            total_length=len(str(obj.atk)) + len(str(obj.HP)) + 3
            stats_line = f'│ {f"{obj.atk}".ljust(width - total_length)}{obj.HP} │'
        else:
            total_length=len(str(obj.HP)) + 4
            stats_line = f'│ {"".ljust(width - total_length)}{obj.HP} │'
        lines.append(stats_line)
    lines.append("\n")
    lines.extend("└" + "─" * (width - 2) + "┘" for _ in range(len(row.objects)))
    lines.append("\n")

    return "".join(lines)