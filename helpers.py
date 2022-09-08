import logging

logger = logging.getLogger(__name__)


def log_result(func_result):
    def wrapper(*args, **kwargs):
        result = func_result(*args, **kwargs)
        logger.info(f'Result of {func_result.__name__} -> {result}')
        return result
    return wrapper