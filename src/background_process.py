from dataclasses import dataclass

from PyQt5.QtCore import (pyqtSignal)

from entity_loader import EntityLoader
from records_loader import RecordsLoader
from result_printer import ResultPrinter, ResultPrinterData
from worker import Worker


@dataclass
class BackgroundProcessArgs:
    DataFilepath: str
    TemplateFilepath: str
    OutputDirpath: str
    NumberPrefix: str
    Date: str


class BackgroundProcess(Worker):
    started = pyqtSignal()
    file_read = pyqtSignal()
    entity_processed = pyqtSignal(str, int, int)  # INN, number, count
    entity_printed = pyqtSignal(str, int, int)  # INN, number, count
    finished = pyqtSignal()

    def __init__(self, args: BackgroundProcessArgs):
        super().__init__(self._target, args)

    def _handle_starting(self):
        self.started.emit()

    def _handle_file_reading(self):
        self.file_read.emit()

    def _handle_entity_processing(self, inn: str, number: int, count: int):
        self.entity_processed.emit(inn, number, count)

    def _handle_entity_printing(self, inn: str, number: int, count: int):
        self.entity_printed.emit(inn, number, count)

    def _handle_finishing(self):
        self.finished.emit()

    def _target(self, args: BackgroundProcessArgs):
        self._handle_starting()
        self._handle_file_reading()
        records_loader = RecordsLoader()
        records_loader.load_from_xlsx(args.DataFilepath)
        records = records_loader.get_records()
        entity_loader = EntityLoader()
        entity_loader.update_from_dadata(*records_loader.get_inns())
        entity_loader.entity_processed.connect(self._handle_entity_processing)
        entities = list(entity_loader.get_entities_by_inns(*records_loader.get_inns()))
        for number, entity in enumerate(entities, start=1):
            result_printer = ResultPrinter(ResultPrinterData(f'{args.TemplateFilepath}/{number}',
                                                             args.Date))
            e_records = list(filter(entity.is_my_record, records))
            self._handle_entity_printing(entity.INN, number, len(entities))
            result_printer.print_entity(
                args.TemplateFilepath,
                f'{args.OutputDirpath}/{entity.INN}',
                entity,
                e_records
            )
        self._handle_finishing()
