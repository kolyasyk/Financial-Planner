from dataclasses import dataclass
from datetime import datetime


@dataclass
class Account:
    name: str
    start_date: datetime
    start_amount: float = 0.0
    gain_rate: float = 0.02
    enabled: bool = True
