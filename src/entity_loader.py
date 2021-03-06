from typing import Iterator

from PyQt5.QtCore import (QObject,
                          pyqtSignal)

from src.dadata_parser import EntitiesByInnGetter
from src.entity import Entity


class EntityLoader(QObject):
    entity_processed = pyqtSignal(Entity, int, int)  # entity, number, count

    def __init__(self):
        super().__init__()
        self._entities: dict[str, Entity] = {}

    def get_entities_by_inns(self, *inns: str) -> Iterator[Entity]:
        """
        For each INN returns Entity.
        :param inns: INNs.
        """
        yield from (self._entities[inn] for inn in inns if inn in self._entities)

    def update_from_dadata(self, inns: list[str], **filters):
        """
        For each INN updates Entity's data.
        :param inns: INNs.
        """
        getter = EntitiesByInnGetter(inns, **filters)
        getter.entity_processed.connect(self._handle_entity_processing)
        self._entities.update({e.INN: e for e in getter.process()})

    def _handle_entity_processing(self, entity: Entity, number: int, count: int):
        """
        Handles entity processing in EntitiesByInnGetter.
        """
        self.entity_processed.emit(entity, number, count)
