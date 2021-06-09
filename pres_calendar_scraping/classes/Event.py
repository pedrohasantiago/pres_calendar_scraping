from dataclasses import dataclass
from datetime import datetime

@dataclass
class Event:
    title: str
    datetime_beginning: datetime
    datetime_end: datetime
    location: str
