from game.field import Field
from game.utils import get_opponent_player_id
from ui.row_render import row_render
from utils.constant import FIELD_WIDTH


def field_render(field: Field, perspective_id: int):
    """show the field in current player's perspective."""
    res=""
    opponent_num = get_opponent_player_id(perspective_id)
    res+=row_render(field.get_opponent_row(perspective_id))  

    if field.front_control == perspective_id:
        res+=("-" * FIELD_WIDTH+'\n')
    res+=row_render(field.get_front_row())
    if field.front_control == opponent_num:
        res+=("-" * FIELD_WIDTH+'\n')
    res+=row_render(field.get_my_row(perspective_id))
    
    return res
