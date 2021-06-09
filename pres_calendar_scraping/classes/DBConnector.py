from datetime import datetime
from sqlite3 import Connection
from typing import Iterable, List, Tuple

from pres_calendar_scraping.classes.Event import Event

class DBConnector:

    def __init__(self, connection: Connection):
        self.connection = connection

    def create_table(self):
        command = '''
            CREATE TABLE events (
                title TEXT NOT NULL,
                datetime_beginning INTEGER NOT NULL,
                datetime_end INTEGER NOT NULL,
                location TEXT NOT NULL
            )
        '''
        self.connection.execute(command)

    def was_table_created(self) -> bool:
        command = '''
            SELECT name
            FROM sqlite_master
            WHERE type='table' AND name='events';
        '''
        for row in self.connection.execute(command):
            return True
        return False

    def is_table_empty(self) -> bool:
        command = '''
            SELECT COUNT(*)
            FROM events;
        '''
        cursor = self.connection.execute(command)
        row = cursor.fetchone()
        if row is not None and row[0] > 0:
            return False
        return True

    def insert_many(self, events: Iterable[Event]):
        """Doesn't commit."""
        event_tuples: List[Tuple[str, int, int, str]] = []
        for event in events:
            assert all(dt.tzinfo == Event.tz for dt in (event.datetime_beginning, event.datetime_end))
            print(f'Will insert {event}')
            event_tuples.append(
                (
                    event.title,
                    int(event.datetime_beginning.timestamp()),
                    int(event.datetime_end.timestamp()),
                    event.location
                )
            )
        self.connection.executemany('INSERT INTO events VALUES (?,?,?,?);', event_tuples)

    def get_last_in_col(self, column: str) -> Event:
        command = '''
            SELECT *
            FROM events
            ORDER BY ? desc
            LIMIT 1;
        '''
        row = next(self.connection.execute(command, [column]))
        title, datetime_beginning_int, datetime_end_int, location = row
        datetime_beginning, datetime_end = (datetime.fromtimestamp(ts, tz=Event.tz)
                                            for ts in (datetime_beginning_int, datetime_end_int))
        return Event(
            title,
            datetime_beginning,
            datetime_end,
            location
        )
