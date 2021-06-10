from datetime import datetime
from sqlite3 import Connection
from typing import Iterable, List, Tuple, Optional

from pres_calendar_scraping.classes.Event import Event

class DBConnector:

    def __init__(self, connection: Connection):
        self.connection = connection

    def create_table_if_not_exists(self):
        # The unique constraint is a protection against unwanted dupes.
        # If they do exist in the source, we can remove the constraint.
        command = '''
            CREATE TABLE IF NOT EXISTS events (
                title TEXT NOT NULL,
                datetime_beginning INTEGER NOT NULL,
                datetime_end INTEGER,
                location TEXT,
                CONSTRAINT temp_dupe_write_protection UNIQUE(title, datetime_beginning)
            )
        '''
        self.connection.execute(command)

    # def was_table_created(self) -> bool:
    #     command = '''
    #         SELECT name
    #         FROM sqlite_master
    #         WHERE type='table' AND name='events';
    #     '''
    #     for row in self.connection.execute(command):
    #         return True
    #     return False

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
        event_tuples: List[Tuple[str, int, Optional[int], Optional[str]]] = []
        for event in events:
            assert all(dt.tzinfo == Event.tz for dt in (event.datetime_beginning, event.datetime_end) if dt is not None)
            print(f'Will insert {event}')
            event_tuples.append(
                (
                    event.title,
                    int(event.datetime_beginning.timestamp()),
                    int(event.datetime_end.timestamp()) if event.datetime_end is not None else None,
                    event.location
                )
            )
        self.connection.executemany('INSERT INTO events VALUES (?,?,?,?);', event_tuples)

    def get_last_in_col(self, column: str) -> Event:
        command = f'''
            SELECT *
            FROM events
            ORDER BY {column} desc
            LIMIT 1;
        ''' # f-string because DB param-substitution doesn't work
        row = next(self.connection.execute(command))
        title, datetime_beginning_int, datetime_end_int, location = row
        datetime_beginning, datetime_end = (ts and datetime.fromtimestamp(ts, tz=Event.tz)
                                            for ts in (datetime_beginning_int, datetime_end_int))
        return Event(
            title,
            datetime_beginning,
            datetime_end,
            location
        )
