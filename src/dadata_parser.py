from PyQt5.QtCore import (QObject,
                          pyqtSignal)
from dadata import Dadata

from config import DadataConfig
from entity import Entity


PARTY_NAME = 'party'


def entity_from_json(data: dict) -> Entity:
    return Entity(
        Name=data['value'],
        INN=int(data['data']['inn']),
        OGRN=int(data['data']['ogrn']),
        IsActive=data['data']['state']['status'] == 'ACTIVE'
    )


class EntitiesByInnGetter(QObject):
    inn_processed = pyqtSignal(int, int)  # INN, it

    def __init__(self, inns: list[Entity], **filters):
        super().__init__()
        self._inns = inns
        self._filters = filters

    def __call__(self) -> list[Entity]:
        result = []
        dadata = Dadata(DadataConfig.TOKEN)
        for it, inn in enumerate(self._inns):
            self.inn_processed.emit(inn, it)
            try:
                response = dadata.find_by_id(PARTY_NAME, str(inn), **self._filters)
                if response:
                    result.append(entity_from_json(response[0]))
            except Exception:
                pass
        dadata.close()
        return result
