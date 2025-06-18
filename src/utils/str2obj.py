from src.symbols import CardType, Nation

def str2nation(str_nation: str) -> Nation:
    """
    Convert a string representation of a nation to a Nation enum.
    Args:
        str_nation (str): The string representation of the nation.
    Returns:
        Nation: The corresponding Nation enum.
    Raises:
        ValueError: If the string does not match any valid nation.
    """
    match str_nation.strip().upper():
        case "USA":
            return Nation.USA
        case "JAPAN":
            return Nation.JAPAN
        case "GERMANY":
            return Nation.GERMANY
        case "SOVIET UNION":
            return Nation.SOVIET
        case "UK":
            return Nation.UK
        case _:
            raise ValueError(f"Invalid nation name: {str_nation}. Must be one of {list(Nation)}.")
        
def str2card_type(str_type: str) -> CardType:
    """
    Convert a string representation of a card type to a CardType enum.
    Args:
        str_type (str): The string representation of the card type.
    Returns:
        CardType: The corresponding CardType enum.
    Raises:
        ValueError: If the string does not match any valid card type.
    """
    match str_type.strip().upper():
        case "INFANTRY":
            return CardType.INFANTRY
        case _:
            raise ValueError(f"Invalid card type: {str_type}. Must be one of {list(CardType)}.")