from concurrent.futures import ThreadPoolExecutor
from google_news_feed import GoogleNewsFeed, NewsItem
from datetime import date, timedelta
from ratelimit import limits, sleep_and_retry
import pandas as pd

LANGUAGE = "nl"
COUNTRY = "NL"
QUERY = 'intitle:ongeluk OR ongeval intext:"elektrische fiets"'
DATE_RANGE = (date(2022, 1, 1), date(2023, 1, 1))
DF_FILENAME = (
    f"{date.today()}_{LANGUAGE}-{COUNTRY}_{QUERY}_{DATE_RANGE[0]}_{DATE_RANGE[1]}"
)


@sleep_and_retry
@limits(calls=3, period=1)
def query_by_day(day: date) -> list[NewsItem]:
    print(day)
    return feed.query(QUERY, before=day + timedelta(1), after=day)


feed = GoogleNewsFeed(language=LANGUAGE, country=COUNTRY)

date_range = (
    DATE_RANGE[0] + timedelta(d) for d in range((DATE_RANGE[1] - DATE_RANGE[0]).days)
)

results = [r for rs in ThreadPoolExecutor().map(query_by_day, date_range) for r in rs]

df = pd.DataFrame(results)
df.to_pickle(f"{DF_FILENAME}.pickle")
df.to_csv(f"{DF_FILENAME}.csv")
