from datetime import datetime
from sqlite3 import Connection
from typing import Iterable, List, Tuple, Optional

from pres_calendar_scraping.classes.Event import Event

DBRow = Tuple[Optional[int], str, str, Optional[str], Optional[str]]

class DBConnector:

    def __init__(self, connection: Connection):
        self.connection = connection

    def create_table_if_not_exists(self):
        # The unique constraint is a protection against unwanted dupes.
        # If they do exist in the source, we can remove the constraint.
        command = '''
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER NOT NULL PRIMARY KEY,
                title TEXT NOT NULL,
                beginning TEXT NOT NULL,
                end TEXT,
                location TEXT,
                CONSTRAINT temp_dupe_write_protection UNIQUE(title, beginning)
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
        event_tuples: List[DBRow] = []
        for event in events:
            print(f'Will insert {event}')
            event_tuples.append(
                (
                    None,
                    event.title,
                    event.beginning.isoformat(),
                    event.end.isoformat() if event.end is not None else None,
                    event.location
                )
            )
        self.connection.executemany('INSERT INTO events VALUES (?,?,?,?,?);', event_tuples)

    def get_last_in_col(self, column: str) -> Event:
        command = f'''
            SELECT *
            FROM events
            ORDER BY {column} desc
            LIMIT 1;
        ''' # f-string because DB param-substitution doesn't work
        row: DBRow = next(self.connection.execute(command))
        _, title, beginning_str, end_str, location = row
        datetime_beginning = datetime.fromisoformat(beginning_str)
        datetime_end = datetime.fromisoformat(end_str) if end_str is not None else end_str
        return Event(
            title,
            datetime_beginning,
            datetime_end,
            location
        )
