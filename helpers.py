from pathlib import Path
import logging
import configparser


logger = logging.getLogger(__name__)
config = configparser.ConfigParser()
config.read('config.ini')
XML_PATH = Path(config['Main']['XML_PATH'])


def log_result(func_result):
    def wrapper(*args, **kwargs):
        result = func_result(*args, **kwargs)
        logger.info(f'Result of {func_result.__name__} -> {result}')
        return result
    return wrapper