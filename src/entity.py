from dataclasses import dataclass

from src.record import Record


@dataclass
class Entity:
    Name: str
    FullName: str
    INN: str
    OGRN: str
    Address: str
    IsActive: bool

    def is_my_record(self, record: Record):
        """
        Returns True if Record relates to Entity else False.
        """
        return self.INN == record.INN
