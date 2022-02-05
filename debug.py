# disable=import-outside-toplevel
"""
Тесты, функции, которые нужно запустить. Чтобы запустить функцию, нужно изменить метод main.
Если нужно вовзращать результат метода, то поставтье декоратор log_result
"""
import datetime
import json
from helpers import XML_PATH, log_result

DOC_ID = 152355


def main():
    """ Вызовете метод, который нужно запустить. """
    check_before_fix(DOC_ID)

# =====================================================================================================================
# =====================================================================================================================
# =====================================================================================================================


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


def send_overload(doc_id: int, number=1, ChangeOwnership=1):
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
