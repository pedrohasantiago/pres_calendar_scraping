# pres_calendar_scraping

A scraper for the [public schedule of the president of Brazil](https://www.gov.br/planalto/pt-br/acompanhe-o-planalto/agenda-do-presidente-da-republica). Analysis to be done yet.

## Motivation

I see many people on Twitter discussing how little time the current president of Brazil works, according to his public schedule. I wanted to compare times with those of previous presidents, but, unfortunately, the schedule of previous administrations isn't available anymore.

So I decided to compare the work hours throughout the current administration. Some possible questions:

- Have the work hours stayed the same since the beginning of the administration?
- Most of the work hours have been spent in what kind of events?
- What are the cities with the most events?

## Challenges

- Some events are in local time, not in official Brazilian time, `America/Sao_Paulo` (examples [here](https://www.gov.br/planalto/pt-br/acompanhe-o-planalto/agenda-do-presidente-da-republica/2019-06-28) and [here](https://www.gov.br/planalto/pt-br/acompanhe-o-planalto/agenda-do-presidente-da-republica/2019-06-26)). It is not easy to get the local timezone, though, even though that is available in the calendar page: for some events, the correct location for the provided time isn't too clear. To keep things simple, we decided to save all events with the times shown in the source (most of the times, `America/Sao_Paulo`, but not always).

## TODO

- [] Maybe distribute a copy of the DB in .csv? The current format (.sqlite3) isn't very suitable for Git.
- [] Data analysis
