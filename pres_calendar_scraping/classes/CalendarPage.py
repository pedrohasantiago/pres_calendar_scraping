from datetime import date, time, datetime
from functools import cached_property
from datetime import date
from typing import Iterator

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
        assert len(containers) > 0, \
            f'Found nothing in {self.response.url} with CSS selector {selector}'
        return containers

    def to_events(self) -> Iterator[Event]:
        for container in self._event_containers:
            container: Tag
            datetime_beginning, datetime_end = (datetime.combine(self.date, str_to_time(find_string_in_child(container, class_=tag_class)))
                                                for tag_class in ('compromisso-inicio', 'compromisso-fim'))
            title: str = find_string_in_child(container, class_='compromisso-titulo')
            location: str = find_string_in_child(container, class_='compromisso-local')
            yield Event(title, datetime_beginning, datetime_end, location)


def str_to_time(date_str) -> time:
    return time(*date_str.split('h'))


def find_string_in_child(parent_tag: Tag, *args, **kwargs) -> str:
    return parent_tag.find(*args, **kwargs).string