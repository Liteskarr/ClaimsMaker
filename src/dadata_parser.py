from PyQt5.QtCore import (QObject,
                          pyqtSignal)
from dadata import Dadata

from config import MainConfig
from entity import Entity


PARTY_NAME = 'party'


def entity_from_json(data: dict) -> Entity:
    return Entity(
        Name=data['value'],
        FullName=data['data']['name']['full_with_opf'],
        INN=data['data']['inn'],
        OGRN=data['data']['ogrn'],
        Address=data['data']['address']['value'],
        IsActive=data['data']['state']['status'] == 'ACTIVE',
    )


class EntitiesByInnGetter(QObject):
    entity_processed = pyqtSignal(Entity, int, int)  # entity, number, count

    def __init__(self, inns: list[str], **filters):
        super().__init__()
        self._inns = inns
        self._filters = filters

    def __call__(self) -> list[Entity]:
        result = []
        dadata = Dadata(MainConfig.TOKEN)
        for it, inn in enumerate(self._inns):
            try:
                response = dadata.find_by_id(PARTY_NAME, inn, **self._filters)
                if response:
                    result.append(entity_from_json(response[0]))
                    self.entity_processed.emit(result[-1], it, len(self._inns))
            except Exception:
                pass
        dadata.close()
        return result

    def process(self):
        return self.__call__()
