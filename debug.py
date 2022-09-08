# disable=import-outside-toplevel
"""
Тесты, функции, которые нужно запустить. Чтобы запустить функцию, нужно изменить метод main.
Если нужно вовзращать результат метода, то поставтье декоратор log_result
"""
import datetime
import json
from datetime import datetime
from typing import List

from helpers import XML_PATH, log_result
from tqdm import tqdm

DOC_ID = 153845


def main():
    """ Вызовете метод, который нужно запустить. """
    import sbis
    from warehouse.docs.documents_list.optional_lists import OptionalDocumentList

    print(1)
    print(1)
