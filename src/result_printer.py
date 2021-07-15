from dataclasses import dataclass

from PyQt5.QtCore import (QObject)

from src.entity import Entity
from src.record import Record
from src.templates_builder import build_template
from src.templates_renderer import render


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
        model_template = build_template(template_filepath)
        render(
            records,
            {
                'number': self._data.Number,
                'date': self._data.Date,
                'address': entity.Address,
                'name': entity.FullName,
            },
            model_template,
            output_filepath
        )
