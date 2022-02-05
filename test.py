# import sbis
# from warehouse.docs.common.sn_api.sn_db.sn_dal import SnDal
# from warehouse.docs.common.sn_api.sn_util.sn_const import SnStatus
# from warehouse.egaissolutions.egais_state import StateEgais
# from warehouse.gis.egais.events.states import EgaisState
# from warehouse.docs.common.static_data import VisualRepresentation
# from uuid import UUID
# from vnr_set_egais_number import run
from test_emul_outflow_wotech import Emul
# import sbis


def test():
    emul = Emul(152967, 'TRANSFER_-_TRANSFER')
    emul.transfer()