from datetime import date

from pandas import date_range, Timestamp

from pres_calendar_scraping.classes.CalendarPage import CalendarPage
from pres_calendar_scraping.classes.DBConnector import DBConnector
from pres_calendar_scraping.classes.Requester import Requester
from pres_calendar_scraping.db.connection import connection

MIN_EVENT_DATE = date(2019, 1, 1)

db_connector = DBConnector(connection)
requester = Requester(seconds_between_requests=10)

if not db_connector.was_table_created():
    db_connector.create_table()
    start_at = MIN_EVENT_DATE
else:
    start_at = db_connector.get_last_in_col('datetime_beginning').datetime_beginning.date()

for i, timestamp in enumerate(date_range(start_at, date.today(), freq='D')):
    timestamp: Timestamp
    day: date = timestamp.date()
    print(f'Getting calendar page for {day}')
    calendar_page = CalendarPage.from_date(day, requester)
    db_connector.insert_many(calendar_page.to_events())
    # Committing every 100 days we read
    if (i % 100 == 0) and (i > 0):
        connection.commit()
