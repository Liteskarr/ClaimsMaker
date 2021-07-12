from decimal import Decimal
from itertools import count
from functools import reduce
from operator import or_

import openpyxl
from openpyxl import load_workbook
from PyQt5.QtCore import (QObject)

from record import Record
from config import SettingsConfig


KEYWORDS = {
    'ДАТА': lambda r: {'Date': r},
    'НОМЕР': lambda r: {'Number': r},
    'СЧЕТ': lambda r: {'Account': r},
    'ИНН': lambda r: {'INN': r},
    'ИМЯ': lambda r: {'Name': r},
    'ДЕБЕТ': lambda r: {'Debit': Decimal(r).quantize(Decimal('1.00')) if r else Decimal(0)},
    'КРЕДИТ': lambda r: {'Credit': Decimal(r).quantize(Decimal('1.00')) if r else Decimal(0)},
    'ОСНОВАНИЕ': lambda r: {'Reason': r},
}


NoneRecord = Record(**reduce(or_, (func(None) for func in KEYWORDS.values()), {}))


def _find_labels(book: openpyxl.Workbook, sheet_name: str) -> dict[int, str]:
    result = {}
    sheet = book[sheet_name]
    for column in count(1):
        label = sheet.cell(row=SettingsConfig.ROW_LABEL, column=column).value
        if label in KEYWORDS:
            result[column] = label
        elif not bool(label):
            break
    return result


class RecordsLoader(QObject):
    def __init__(self):
        super().__init__()
        self._records = []
        self._errors = []

    def get_records(self) -> list[Record]:
        return self._records

    def get_inns(self) -> list[str]:
        return list(set(map(lambda r: r.INN, self.get_records())))

    def get_errors(self) -> list[Record]:
        return self._errors

    def load_from_xlsx(self, filepath: str):
        book = load_workbook(filepath)
        sheet = book[SettingsConfig.SHEET_NAME]
        labels = _find_labels(book, SettingsConfig.SHEET_NAME)
        for r in range(SettingsConfig.ROW_DATA, sheet.max_row + 1):
            kwargs = {}
            try:
                for c in range(SettingsConfig.COLUMN_START, sheet.max_column + 1):
                    if c in labels.keys():
                        kwargs.update(KEYWORDS[labels[c]](sheet.cell(row=r, column=c).value))
                self._records.append(Record(**kwargs))
            except:
                self._errors.append(**kwargs)
