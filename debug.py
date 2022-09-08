# disable=import-outside-toplevel
"""
Тесты, функции, которые нужно запустить. Чтобы запустить функцию, нужно изменить метод main.
Если нужно вовзращать результат метода, то поставтье декоратор log_result
"""
import datetime
from datetime import datetime

from helpers import log_result
from tqdm import tqdm

DOC_ID = 153845


def main():
    """ Вызовете метод, который нужно запустить. """
    test_events_lists()
    print(1)



# =====================================================================================================================
# =====================================================================================================================
# =====================================================================================================================
@log_result
def check_before_fix(doc_id: int):
    """ Проверка Check before fix"""
    from warehouse.docs.common.validation import valid_signs
    from warehouse.docs.common.validation.mass_validation import inner_check_before_fix
    from warehouse.models.repository import resolve_document_model
    validations_list = [
        valid_signs.COUNT_MORE_THAN_BATCH,
        # valid_signs.EGAIS_TRANSFER_MARKS
    ]
    doc_model = resolve_document_model('ПродИзТоргЗала', need_extension=True)
    params = {'operation': 'sendingEgais', 'need_checked_result': True}
    return inner_check_before_fix(doc_id, validations_list, doc_model, params)


@log_result
def humanize(msg: str):
    """Проверка очеловечеваний ошибок"""
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


@log_result
def get_fed_type(msg: str):
    """ Получить ФЭД тип """
    from warehouse.gis.egais.transport.search_doc import _get_fed_type
    return _get_fed_type(msg)


@log_result
def test_events_lists():
    method_names = (
        'ReturnIn.СписокХранимСобытия',
        'ДокОтгрИсх.СписокХранимСобытия',
        'ReturnOut.СписокХранимСобытия',
        'АктПостановкиЕгаис.СписокХранимСобытия',
        'АктВыпуска.СписокХранимСобытия',
        'ПеремещениеТоргЗал.СписокХранимСобытия',
        'АктСписания.СписокХранимСобытия',

        # 'ReturnIn.СписокДляПечатиСобытия',
        # 'ReturnOut.СписокДляПечатиСобытия',
        # 'АктПостановкиЕгаис.СписокДляПечатиСобытия',
        # 'АктВыпуска.СписокДляПечатиСобытия',
        # 'ПеремещениеТоргЗал.СписокДляПечатиСобытия',
        # 'АктСписания.СписокДляПечатиСобытия',
    )
    return {method_name: _get_event_list(method_name) for method_name in tqdm(method_names)}


@log_result
def test_doc_lists():
    method_names = (
        'ПеремещениеТоргЗал.СписокХраним',
    )
    return {method_name: _get_doc_list(method_name) for method_name in tqdm(method_names)}

@log_result
def test_excel_doc_lists():
    import sbis
    from warehouse.docs.egais.remains.model_remains_egais import RemainsEGAISModel
    fields = ['flat_hr', 'need_root_hr_filter_off']
    filters = sbis.Record({
        'OrgId': 43524,
        'PrefetchSessionStr': "ad7017f9-1d42-4674-8fd4-7ebd97d31367",
        'ReportDate': datetime.strptime('2022-02-22', "%Y-%m-%d").date(),
        'ReportState': 3,
        'init_contractor_data': True,
        'selectedIds': [60337653,60337534,60337464,60337511],
        'MUnitId': None,
        'vCode': "",
        'DiffFilter': None,
        'DocNomIds': [60337653,60337534,60337464,60337511],
        '@НоменклатураДокумента': [60337653,60337534,60337464,60337511],
        'СкладскойДокумент': 731378,
        'РазделФильтр': 0,
        'actions': sbis.Record({
            'calc_category': False,
            'calc_parts': False,
            'calc_shipped': False,
            'calc_totals': True,
            'calc_not_sync': False,
            'calc_gift': False,
            'calc_actual': False,
            'calc_category_supply': False,
            'calc_part_root': False,
            'calc_mu': True,
            'calc_pics': False,
            'calc_ean13': False,
            'calc_egais_codes': False,
            'calc_product_info': False,
            'to_excel': True,
            'difference_of_parts': False,
            'need_parts_set': True,
            'init_contractor_data': True
        })
    })
    RemainsEGAISModel.doc_nom_list(fields, filters, sbis.SortingList())


def _get_event_list(method_name):
    import sbis
    from warehouse.gis.egais.event_list import EgaisEventDocumentList
    fltr = sbis.Record({
        'iterative_list': True,
        'new_navigation': True,
        'onlyEgais': True,
        'position_on_today': True,
        'rp_doc': True,
        'ws4_registry': True,
        'НазваниеТипаДокумента': method_name.split('.')[0],
        'СостояниеСобытий': "Все",
        'УчитыватьИерархиюНО': True,
        'ФильтрДатаП': None,
        'ФильтрДатаС': None,
        'ФильтрОрганизацияФилиал': "-1",
        'ФильтрПометкиИскл': [],
        'ФильтрСостояниеЕГАИС': None,
    })


    nav = sbis.Navigation(
        sbis.NavigationPositionTag(),
        sbis.Record({'@НоменклатураДокумента': ''}),
        25,
        sbis.NavigationDirection.ndFORWARD,
        True
    )
    sbis.Session.MethodName = lambda: method_name
    method = 'get_documents_list_for_print' if 'ДляПечати' in method_name else 'get_documents_list'
    return getattr(EgaisEventDocumentList(fltr, nav), method)()


def _get_doc_list(method_name):
    import sbis
    from warehouse.docs.documents_list.optional_lists import OptionalDocumentList
    fltr = sbis.Record({
        "Face1Spp": None,
        "PublicGroupId": None,
        "onlyEgais": True,
        "rp_doc": True,
        "НазваниеТипаДокумента": None,
        "ФильтрДатаП": None,
        "ФильтрДатаПериод": "Все",
        "ФильтрДатаС": None,
        "ФильтрОрганизацияФилиал": "-1",
        "ФильтрОтветственноеЛицо": [],
        "ФильтрПометкиВкл": [],
        "ФильтрПометкиИскл": [],
        "ФильтрПроведенные": None,
        "ФильтрСкладРеестр": [],
        "ФильтрСостояниеЕГАИС": "0",
        "ФильтрУдаленные": None
    })

    nav = sbis.Navigation(
        sbis.NavigationPositionTag(),
        sbis.Record({'@НоменклатураДокумента': ''}),
        25,
        sbis.NavigationDirection.ndFORWARD,
        True
    )
    sbis.Session.ObjectName = lambda: method_name.split('.')[0]
    sbis.Session.MethodName = lambda: method_name

    return OptionalDocumentList(fltr, nav).get_documents_list()

