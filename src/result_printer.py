from dataclasses import dataclass

from PyQt5.QtCore import (QObject,
                          pyqtSignal)
from docxtpl import DocxTemplate

from entity import Entity
from record import Record
from template_builder import build


@dataclass
class ResultPrinterData:
    Number: str
    Date: str


class ResultPrinter(QObject):
    def __init__(self, data: ResultPrinterData):
        super().__init__()
        self._data = data

    def print_entity(self,
                     template_filepath: str,
                     output_filepath: str,
                     entity: Entity,
                     records: list[Record]):
        build(
            records,
            {
                'number': self._data.Number,
                'date': self._data.Date,
                'address': entity.Address,
                'name': entity.FullName,
            },
            DocxTemplate(template_filepath),
            output_filepath
        )
