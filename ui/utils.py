from utils.constant import FIELD_WIDTH

def show_banner(msg: str):
    l_len=int((FIELD_WIDTH-len(msg))/2)
    r_len=FIELD_WIDTH-len(msg)-l_len
    """Prints a banner with the given message."""
    print(f"\n{'=' * l_len}{msg}{'=' * r_len}")
