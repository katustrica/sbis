""" Запуск. Настройка логирования, установка сессии и т.п. """
import configparser
import logging
import os
import sys
import warnings
from time import sleep

from debug import main
from tqdm import tqdm

# Настраиваем логирование
logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)
warnings.filterwarnings("ignore")

# Считываем конифиг
config = configparser.ConfigParser()
config.read('config.ini')
main_config = config['Main']
session_config = config['Sessions']


def setup():
    """ Редактируем PATH, настраиваем сессию, порт и хост."""
    with tqdm(total=10, bar_format='{l_bar}{bar}| Прошло времени: {elapsed}') as progress_bar:
        stand = main_config['STAND']

        # PATH
        progress_bar.set_description('Добавляем стэнд в path...')
        home = os.getcwd()
        sys.path.append(stand)
        sleep(0.5)
        progress_bar.update(1)

        # IMPORT SBIS
        progress_bar.set_description('Импортируем SBIS, длительная операция...')
        os.chdir(stand)
        os.environ['SBIS_HOST'] = main_config['SBIS_HOST']
        os.environ['SBIS_PORT'] = main_config['SBIS_PORT']
        os.environ['SBIS_VIRTUAL_FOLDER'] = main_config['SBIS_VIRTUAL_FOLDER']
        import sbis_root as sbis  # disable=import-outside-toplevel
        os.chdir(home)
        progress_bar.update(7.5)

        # СЕССИЯ
        sleep(0.5)
        progress_bar.set_description('Устанавливаем сессию...')
        session_type = main_config['SESSION_TYPE'].upper()
        session = session_config[session_type]
        search_path = f"'_{session.split('-')[0]}', 'public'"

        sbis.Session.Set(0, session)
        sbis.SetCurrentSearchPath(search_path)
        sbis.Session.Set(sbis.WebServerContextKey.icsREQUEST_NUMBER, "1")
        progress_bar.set_description('Готово!')
        progress_bar.update(1.5)


if __name__ == '__main__':
    logger.info('Настройка...')
    setup()
    logger.info('Настройка завершена!')
    main()
