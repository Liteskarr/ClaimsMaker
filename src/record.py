from dataclasses import dataclass
from decimal import Decimal


@dataclass
class Record:
    Date: str
    Number: str
    Account: str
    INN: str
    Name: str
    Debit: Decimal
    Credit: Decimal
    Reason: str
