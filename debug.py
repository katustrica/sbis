import datetime
import os
import sys
import json
import uuid
import logging
from pathlib import Path
import warnings

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)
warnings.filterwarnings("ignore")

STAND = r"C:\sbis\22.1100\build\online"
SESSION = "0059fb08-0059fb09-00ba-bc391ae9dc50dd1a"  # musa - PRE-TEST-ONLINE
# SESSION = "000ba3cf-0053a934-00ba-e9be5d161eb5ad2b"  # musa - TEST-ONLINE
SEARCH_PATH = "'_0059fb08', 'public'"  # PRE-TEST-ONLINE
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


@log_result
def inflow_waybill(doc_id=None):
    from test_emul_outflow_wotech import Emul, read_xml, _get_response_in_doc
    from warehouse.gis.common.gis_enum import Gis
    from warehouse.gis.common.transport.transport_manager import TransportManager
    xmls = [
        read_xml(XML_PATH, doc_id, 'WAY_BILL_IN.xml'),
        read_xml(XML_PATH, doc_id, 'TTN_INFORM_F2_REG.xml'),
        read_xml(XML_PATH, doc_id, 'TTN_HISTORY_F2_REG.xml'),
    ]
    manager = TransportManager(Gis.EGAIS, False)
    response = _get_response_in_doc(xmls)
    manager.emulate_in_doc(response, {})

@log_result
def answer(doc_id=None):
    from test_emul_outflow_wotech import read_xml, get_response
    from warehouse.gis.common.gis_enum import Gis
    from warehouse.gis.common.transport.transport_manager import TransportManager
    xmls = [
        read_xml(XML_PATH, doc_id, 'format.xml'),
    ]
    manager = TransportManager(Gis.EGAIS, False)
    transport_key = {
        'doc_id': doc_id,
        'doc_type': 'ВнутрПрм',
        'doc_uuid': '46f8c0e7-8321-4bcd-baa1-12079372d63b',
    }
    key = json.dumps(transport_key, ensure_ascii=False)
    response = {
        'ResponseData': [{'Body': xml_body, 'Key': '1'} for xml_body in xmls],
        'Key': key
    }
    manager.emulate_answer(response, {})


@log_result
def check_before_fix(doc_id: int):
    from warehouse.docs.common.validation.mass_validation import inner_check_before_fix
    from warehouse.docs.common.validation import valid_signs
    from warehouse.models.repository import resolve_document_model
    validations_list = [
        # valid_signs.BOTH_CHECK_SERIALS_COUNT,
        # valid_signs.EGAIS_TRANSFER_MARKS
    ]
    doc_model = resolve_document_model('ВнутрПрм', need_extension=True)
    params = {'operation': 'posting', 'need_checked_result': True}
    return inner_check_before_fix(doc_id, validations_list, doc_model, params)


@log_result
def humanize(msg: str):
    from warehouse.gis.egais.events.handlers.humanize import humanize_error_text
    return humanize_error_text(msg)


@log_result
def call_test():
    from test import test
    return test()


def overload(doc_id: int, number=1, ChangeOwnership=1):
    """ Отправка Перегрузки """
    from warehouse.gis.egais.transport.send_to_egais import overload
    overload_rec = sbis.Record({
        'doc_id': doc_id,
        'transport': sbis.Record({
            'ChangeOwnership': ChangeOwnership,
            'Date': datetime.date.today(),
            'NUMBER': number,
            'ParentRoutes': [],
            'TRAN_CAR': "",
            'TRAN_COMPANY': "",
            'TRAN_CUSTOMER': "",
            'TRAN_DRIVER': "",
            'TRAN_FORWARDER': "",
            'TRAN_LOADPOINT': "123",
            'TRAN_REDIRECT': "",
            'TRAN_REGNUMBER': "123",
            'TRAN_TRAILER': "",
            'TRAN_TYPE': 419,
            'TRAN_UNLOADPOINT': "123"
        })
    })
    overload(overload_rec)

