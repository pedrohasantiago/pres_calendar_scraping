from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Event:
    title: str
    beginning: datetime
    end: Optional[datetime]
    location: Optional[str]