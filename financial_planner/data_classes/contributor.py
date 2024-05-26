from dataclasses import dataclass
from datetime import datetime


@dataclass
class Contributor:
    name: str
    birthday: datetime
    retirement_age: int

    def __post_init__(self):
        self.retirement_date = self.birthday.year + self.retirement_age
