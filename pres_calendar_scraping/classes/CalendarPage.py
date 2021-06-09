from datetime import date, time, datetime
from functools import cached_property
from datetime import date
from typing import Iterator, Optional, cast

from bs4 import BeautifulSoup
from bs4.element import Tag
from requests import Response

from pres_calendar_scraping.classes.Event import Event
from pres_calendar_scraping.classes.Requester import Requester

class CalendarPage:

    def __init__(self, response: Response):
        self.response = response
        self.soup = BeautifulSoup(response.content, features='lxml')

    @classmethod
    def from_date(cls, page_date: date, requester: Requester):
        url = f'https://www.gov.br/planalto/pt-br/acompanhe-o-planalto/agenda-do-presidente-da-republica/{page_date.isoformat()}'
        response = requester.request('get', url)
        return cls(response)

    @cached_property
    def date(self) -> date:
        url = self.response.url
        date_str = url.split('/')[-1]
        return date.fromisoformat(date_str)

    @property
    def _event_containers(self):
        selector = '.item-compromisso'
        containers = self.soup.select(selector)
        print(f'Found nothing in {self.response.url} with CSS selector {selector}')
        return containers

    def to_events(self) -> Iterator[Event]:
        for container in self._event_containers:
            container: Tag
            datetime_beginning, datetime_end = (datetime.combine(self.date, str_to_time(found_str), tzinfo=Event.tz) if (found_str := find_string_in_child(container, class_=tag_class)) is not None else found_str
                                                for tag_class in ('compromisso-inicio', 'compromisso-fim'))
            title = find_string_in_child(container, class_='compromisso-titulo')
            location = find_string_in_child(container, class_='compromisso-local')
            assert title is not None, title
            assert datetime_beginning is not None, datetime_beginning
            yield Event(title, datetime_beginning, datetime_end, location)


def str_to_time(date_str: str) -> time:
    hour, minutes = (int(part) for part in date_str.split('h'))
    return time(hour, minutes)


def find_string_in_child(parent_tag: Tag, *args, **kwargs) -> Optional[str]:
    tag: Optional[Tag] = parent_tag.find(*args, **kwargs)
    return (tag.text or None  # .text may return an empty string
        if tag is not None
        else None)