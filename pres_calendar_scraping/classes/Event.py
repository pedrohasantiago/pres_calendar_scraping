from dataclasses import dataclass, field
from datetime import datetime, tzinfo
from typing import Optional, cast

from dateutil.tz import gettz

@dataclass
class Event:
    title: str
    datetime_beginning: datetime
    datetime_end: Optional[datetime]
    location: Optional[str]
    tz: tzinfo = field(repr=False, default=cast(tzinfo, gettz('America/Sao_Paulo')))