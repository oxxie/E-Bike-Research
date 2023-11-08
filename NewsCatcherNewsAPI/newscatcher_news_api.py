from newscatcherapi import NewsCatcherApiClient
import tomllib

CONFIG = tomllib.load(open(".env.toml", "rb"))
API_KEY = CONFIG["NEWSCATCHER_NEWS_API_KEY"]

api = NewsCatcherApiClient(x_api_key=API_KEY)

json = api.get_search_all_articles(
    q='(ongeval OR ongeluk) AND "elektrische fiets"',
    lang="nl",
    from_="30 days ago",
    countries="NL",
)

for article in json["articles"]:
    print(article["title"])
