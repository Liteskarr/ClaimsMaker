from dataclasses import dataclass


@dataclass
class Entity:
    Name: str
    INN: int
    OGRN: int
    IsActive: bool
