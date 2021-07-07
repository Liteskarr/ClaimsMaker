from typing import Iterator
from datetime import datetime

from record import Record


def parse_line(line: str) -> Iterator[object]:
    line = line.split('\t')
    yield datetime.strptime(line[0], '%d/%m/%y') if line[0] else None
    yield int(line[1]) if line[1] else None
    yield int(line[2]) if line[2] else None
    yield int(line[3]) if line[3] else None
    yield line[4] if line[4] else None
    yield int(line[5]) if line[5] else None
    yield line[6] if line[6] else None
    yield int(line[7]) if line[7] else None
    yield float(line[8].replace(',', '.')) if line[8] else 0
    yield float(line[9].replace(',', '.')) if line[9] else 0
    yield line[10] if line[10] else None


def parse_file(filename: str) -> Iterator[Record]:
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            yield Record(*parse_line(line))
