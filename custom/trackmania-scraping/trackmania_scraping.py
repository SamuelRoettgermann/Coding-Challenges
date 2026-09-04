# Not sure if this was 100% working, but it should allow one to scrape some account data for a TM2020 player.

import re
import requests
from datetime import date, datetime


ACCOUNT_ID: str = None
YEAR_FROM = 2020
YEAR_TO = 2022

if ACCOUNT_ID is None:
    raise ValueError("ACCOUNT_ID not set")


Y = 2000 # dummy leap year to allow input X-02-29 (leap day)
seasons = [('winter', (date(Y,  1,  1),  date(Y,  3, 20))),
           ('spring', (date(Y,  3, 21),  date(Y,  6, 20))),
           ('summer', (date(Y,  6, 21),  date(Y,  9, 22))),
           ('fall', (date(Y,  9, 23),  date(Y, 12, 20))),
           ('winter', (date(Y, 12, 21),  date(Y, 12, 31)))]

def get_season(now: date | datetime) -> str:
    if isinstance(now, datetime):
        now = now.date()

    now = now.replace(year=Y)
    return next(season for season, (start, end) in seasons
                if start <= now <= end)


years = range(YEAR_FROM, YEAR_TO + 1)
tm_seasons = 'winter', 'spring', 'summer', 'fall'
difficulty = 'white', 'green', 'blue', 'red', 'black'

class RESULT:
    datatype = str
    NO_MEDAL = "no medal"
    BRONZE_MEDAL = "bronze"
    SILVER_MEDAL = "silver"
    GOLD_MEDAL = "gold"
    AUTHOR_MEDAL = "author"


results: list[tuple[str, RESULT.datatype]] = []

for year in years:
    for season in tm_seasons:
        url_season: str = f"{season}-{year}"
        if year == date.today().year and get_season(date.today()) == season:
            url_season: str = "active"

        print(f"requesting {year}-{season}...", end="")
        req = requests.request("GET", f"https://seytaek.com/seasons/{url_season}/{ACCOUNT_ID}")
        text = req.text.replace(" ", "").replace("\n", "")

        finder = re.findall(r'<divclass="map([a-z]+)"data_base64-name="(\d+)"', text)
        print(f" found {len(finder)} medals")

        for find in finder:
            result, track_number = find
            x: RESULT.datatype = "fuck you"
            match result:
                case "bronze":
                    x = RESULT.BRONZE_MEDAL
                case "silver":
                    x = RESULT.SILVER_MEDAL
                case "gold":
                    x = RESULT.GOLD_MEDAL
                case "author":
                    x = RESULT.AUTHOR_MEDAL
                case "":  # should never happen
                    x = RESULT.NO_MEDAL

            results.append((f"{year}-{season}-{track_number}", x))


for track, result in results:
    print(f"{track}: {result}")