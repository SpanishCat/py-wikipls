from datetime import date, datetime
import urllib.parse
import urllib.request
import urllib.error
import json

import requests

LANG = "en"


def to_timestamp(date_: date):
    print(date_.strftime("%Y%m%d"))
    return date_.strftime("%Y%m%d")
    # return f"{date.year}{date.month}{date.day}"


def get_views(name: str, date_: str | date, lang=LANG):
    if isinstance(date_, date):
        print("it is")
        date_ = to_timestamp(date_)
    else:
        print(f"{type(date_)=}")
        print(f"{type(date)=}")

    url = u"https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/" \
           u"{}.wikipedia.org/all-access/all-agents/{}/daily/{}/{}" \
        .format(lang.lower(), urllib.parse.quote(name), date_, date_)

    return response_for(url)


def get_title(name: str) -> str | None:
    response = response_for(f"https://en.wikipedia.org/api/rest_v1/page/title/{name}")

    if response:
        return response["items"][0]["title"]
    else:
        return None


def get_segments(name: str) -> str | None:
    response = response_for(f"https://en.wikipedia.org/api/rest_v1/page/segments/{name}")

    if response:
        return response["segmentedContent"]
    else:
        return None


def get_pdf(name: str):
    response = requests.get(f"https://en.wikipedia.org/api/rest_v1/page/pdf/{name}")

    if response.status_code == 200:
        return response.content


def response_for(url: str) -> dict | None:
    print(f"{url=}")
    response = requests.get(url)
    if response.status_code == 200:
        return json.loads(response.content)
    else:
        return None


# def get_views(name, lang, start_date, end_date):
#     if type(start_date) != str:
#         print(f"Start date is not string. Instead it's: {type(start_date)}")
#     if type(end_date) != str:
#         print(f"End date is not string. Instead it's: {type(start_date)}")
#
#     if type(start_date) == date:
#         start_date = to_timestamp(start_date)
#     if type(end_date) == date:
#         end_date = to_timestamp(end_date)
#
#     return u"https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/" \
#            u"{}.wikipedia.org/all-access/all-agents/{}/daily/{}/{}" \
#         .format(lang.lower(), urllib.parse.quote(name), start_date, end_date)
