from dataclasses import dataclass


@dataclass
class Entity:
    Name: str
    FullName: str
    INN: str
    OGRN: str
    Address: str
    IsActive: bool
