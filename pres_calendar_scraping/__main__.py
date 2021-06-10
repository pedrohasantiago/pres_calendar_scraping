from datetime import date, timedelta

from pandas import date_range, Timestamp

from pres_calendar_scraping.classes.CalendarPage import CalendarPage
from pres_calendar_scraping.classes.DBConnector import DBConnector
from pres_calendar_scraping.classes.Requester import Requester
from pres_calendar_scraping.db.connection import connection

MIN_EVENT_DATE = date(2019, 1, 1)  # First day of the current administration. The source returns 404 before this.

db_connector = DBConnector(connection)
requester = Requester(min_sleep_time=5, max_sleep_time=30)

db_connector.create_table_if_not_exists()
if not db_connector.is_table_empty():
    # We have to start at 1 day after the max one, or else we will
    # repeat the start day if we have to rerun.
    start_at = db_connector.get_last_in_col('datetime_beginning').datetime_beginning.date() + timedelta(days=1)
else:
    start_at = MIN_EVENT_DATE

try:
    for i, timestamp in enumerate(date_range(start_at, date.today(), freq='D')):
        timestamp: Timestamp
        day: date = timestamp.date()
        print(f'Getting calendar page for {day}')
        calendar_page = CalendarPage.from_date(day, requester)
        db_connector.insert_many(calendar_page.to_events())
        # Committing every 100 days we read
        if (i % 100 == 0) and (i > 0):
            connection.commit()
finally:
    connection.commit()
    connection.close()