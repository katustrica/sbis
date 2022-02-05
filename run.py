import datetime
import os
import sys
import json
import uuid
import logging
from pathlib import Path
import warnings
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

main_config = config['Main']
session_config = config['Sessions']

STAND = main_config['STAND']
SESSION = session_config['PRE_TEST']
SEARCH_PATH = f"'_{SESSION.split('-')[0]}', 'public'"
os.environ['SBIS_HOST'] = main_config['SBIS_HOST']
os.environ['SBIS_PORT'] = main_config['SBIS_PORT']
os.environ['SBIS_VIRTUAL_FOLDER'] = main_config['SBIS_VIRTUAL_FOLDER']

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)
warnings.filterwarnings("ignore")


XML_PATH = Path(r'C:\sbis\SCRIPTS\FILES')
DOC_ID = 152355

api = None


def log_result(func_result):
    def wrapper(*args, **kwargs):
        result = func_result(*args, **kwargs)
        logger.info(result)
    return wrapper


def setup(stand=STAND, session=SESSION, search_path=SEARCH_PATH):
    home = os.getcwd()
    sys.path.append(stand)

    os.chdir(stand)
    os.environ['SBIS_HOST'] = '10-176-129-231.dev-vpn.corp.tensor.ru'
    os.environ['SBIS_PORT'] = '2001'
    os.environ['SBIS_VIRTUAL_FOLDER'] = ''
    import sbis_root as sbis
    os.chdir(home)
    sbis.SetCurrentSearchPath(search_path)
    sbis.Session.Set(0, session)
    sbis.Session.Set(sbis.WebServerContextKey.icsREQUEST_NUMBER, "1")
    global api
    api = sbis

if __name__ == '__main__':
    setup(stand=STAND, session=SESSION, search_path=SEARCH_PATH)
    sbis = api
    # check_before_fix(DOC_ID)
    call_test()
    # from warehouse.egaissolutions.retail_sales import auto_transfer_in_retail
    # auto_transfer_in_retail(142981)
    # from warehouse.egaissolutions import sending
    # sending.send_act(147759, 1, '')
    # from warehouse.docs.internal.transfer.model_transfer import TransferModel
    # TransferModel().get_doc_nom_alco(145905)
    #  На серийниках прихода дополнительно проставляем статус "подтверждено" и Op=1
