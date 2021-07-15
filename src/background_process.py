import os
from dataclasses import dataclass
from typing import Callable

from PyQt5.QtCore import (pyqtSignal)

from entity_loader import EntityLoader
from records_loader import RecordsLoader
from result_printer import ResultPrinter, ResultPrinterData
from worker import Worker
from record import Record
from entity import Entity


@dataclass
class BackgroundProcessArgs:
    DataFilepaths: list[str]
    TemplateFilepath: str
    OutputDirpath: str
    NumberPrefix: str
    Date: str
    Filter: Callable[[Record], bool]
    TypeFilter: dict[str, str]


class BackgroundProcess(Worker):
    started = pyqtSignal()
    record_read = pyqtSignal(str, int, int)  # filepath, number, count
    entity_processed = pyqtSignal(Entity, int, int)  # INN, number, count
    entity_printed = pyqtSignal(Entity, int, int)  # INN, number, count
    finished = pyqtSignal()

    def __init__(self, args: BackgroundProcessArgs):
        super().__init__(self._target, args)

    def _handle_starting(self):
        self.started.emit()

    def _handle_record_reading(self, filename: str, number: int, count: int):
        self.record_read.emit(filename, number, count)

    def _handle_entity_processing(self, entity: Entity, number: int, count: int):
        self.entity_processed.emit(entity, number, count)

    def _handle_entity_printing(self, entity: Entity, number: int, count: int):
        self.entity_printed.emit(entity, number, count)

    def _handle_finishing(self):
        self.finished.emit()

    def _target(self, args: BackgroundProcessArgs):
        self._handle_starting()
        records_loader = RecordsLoader()
        records_loader.record_read.connect(self._handle_record_reading)
        for path in args.DataFilepaths:
            records_loader.load_from_xlsx(path)
        records_loader.apply_filter(args.Filter)
        records = records_loader.get_records()
        entity_loader = EntityLoader()
        entity_loader.entity_processed.connect(self._handle_entity_processing)
        entity_loader.update_from_dadata(records_loader.get_inns(), **args.TypeFilter)
        entities = list(entity_loader.get_entities_by_inns(*records_loader.get_inns()))
        for number, entity in enumerate(entities, start=1):
            result_printer = ResultPrinter(ResultPrinterData(f'{args.NumberPrefix}/{number}',
                                                             args.Date))
            e_records: list[Record] = list(filter(entity.is_my_record, records))
            self._handle_entity_printing(entity, number, len(entities))
            result_printer.print_entity(
                args.TemplateFilepath,
                f'{args.OutputDirpath}/{entity.INN}.docx',
                entity,
                e_records
            )
        self._handle_finishing()
