import logging
from colorlog import ColoredFormatter

def setup_logger(name: str, level: int = logging.DEBUG) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(level)
    handler = logging.StreamHandler()
    handler.setLevel(level)
    formatter = ColoredFormatter(
        "%(log_color)s%(asctime)s [%(levelname)s] %(name)s : %(message)s",
        datefmt="%H:%M:%S",
        reset=True,
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'bold_red',
        }
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger