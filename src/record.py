from datetime import datetime
from dataclasses import dataclass


@dataclass
class Record:
    Date: datetime
    Number: int
    BankId: int
    CorrectionalAccount: int
    TargetBank: str
    TargetAccount: int
    TargetName: str
    TargetINN: int
    Debit: float
    Credit: float
    Reason: str
