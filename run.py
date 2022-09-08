""" Запуск. Настройка логирования, установка сессии и т.п. """
__author__ = 'Миннахметов М.А.'

import configparser
import logging
import os
import sys
import warnings
from typing import Optional

from debug import main

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
    """ Редактируем PATH, настраиваем сессию, порт и хост, прогреваем модули."""
    logger.info('Настройка...')

    try:
        from tqdm import tqdm
        tqdm_installed = True
    except ModuleNotFoundError:
        tqdm_installed = False

    if tqdm_installed:
        with tqdm(total=10, bar_format='{l_bar}{bar}| Прошло времени: {elapsed}') as progress_bar:
            environ_and_import_sbis(main_config, progress_bar)
            login(session_config, progress_bar)
            warm_up_modules(progress_bar)
    else:
        environ_and_import_sbis(main_config)
        login(session_config)
        warm_up_modules()

    logger.info('Настройка завершена!')


def environ_and_import_sbis(main_config: configparser.SectionProxy, progress_bar: Optional[object]):
    """Настраиваем окружение и импортируем sbis_root"""
    # PATH
    stand = main_config['STAND']
    progress_bar.set_description('Добавляем стэнд в path...')
    home = os.getcwd()
    sys.path.append(stand)
    progress_bar.update(1)

    # IMPORT SBIS
    progress_bar.set_description('Импортируем SBIS, длительная операция...')
    os.chdir(stand)
    os.environ['SBIS_HOST'] = main_config['SBIS_HOST']
    os.environ['SBIS_PORT'] = main_config['SBIS_PORT']
    os.environ['SBIS_VIRTUAL_FOLDER'] = main_config['SBIS_VIRTUAL_FOLDER']
    import sbis_root as sbis
    os.chdir(home)
    progress_bar.update(6.5)


def login(session_config: configparser.SectionProxy, progress_bar: Optional[object]):
    """Логинимся под нашим паролем и получаем сессию для установки SearchPath"""
    progress_bar.set_description('Устанавливаем сессию...')
    import sbis_root as sbis
    login = session_config['LOGIN']
    password = session_config['PASS']
    stand_type = session_config['STAND_TYPE']
    url = r'https://{stand_type}-online.sbis.ru/auth/'.format(stand_type=stand_type)
    session_id = sbis.AuthByLoginPass(url, login, password).GetSessionId()
    sbis.Session.Set(sbis.WebServerContextKey.icsSESSION_ID, session_id)
    sbis.Session.Set(sbis.WebServerContextKey.icsREQUEST_NUMBER, '1')
    sbis.SetCurrentSearchPath(f'_{session_id[:8]}, public')
    progress_bar.update(1.5)


def warm_up_modules(progress_bar: Optional[object]):
    """Прогреваем модули для устранения проблем с реимпортами"""
    from on_event import OnEndAllLoadModules
    progress_bar.set_description('Прогреваем модули')
    OnEndAllLoadModules('')
    progress_bar.set_description('Готово!')
    progress_bar.update(1.0)


if __name__ == '__main__':
    setup()
    main()
