from dataclasses import dataclass

from record import Record


@dataclass
class Entity:
    Name: str
    FullName: str
    INN: str
    OGRN: str
    Address: str
    IsActive: bool

    def is_my_record(self, record: Record):
        return self.INN == record.INN
