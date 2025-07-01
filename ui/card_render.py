def render_card(name: str, attack: int, health: int, width: int = 16) -> str:
    """
    生成一个 ASCII 卡牌图像。
    :param name: 卡牌名称
    :param attack: 攻击力
    :param health: 血量
    :param width: 卡牌宽度（字符数），默认 16
    :return: 字符串形式的卡牌图
    """
    top = "┌" + "─" * (width - 2) + "┐"
    name_line = f"│ {name.center(width - 4)} │"
    empty_line = "│" + " " * (width - 2) + "│"
    total_length=len(str(attack)) + len(str(health)) + 3
    stats_line = f'│ {f"{attack}".ljust(width - total_length)}{health} │'
    bottom = "└" + "─" * (width - 2) + "┘"
    return "\n".join([top, name_line, empty_line, stats_line, bottom])

