from typing import overload

import requests
import json
import urllib.parse

from datetime import date

LANG = "en"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64"}  # todo Check wiki's docs and change headers


def to_timestamp(date_: date) -> str:
    return date_.strftime("%Y%m%d")


@overload
def get_views(name: str, date_: date, lang: str = LANG) -> int: ...
@overload
def get_views(name: str, date_: str, lang: str = LANG) -> int: ...


def get_views(name: str, date_: str | date, lang: str = LANG) -> int:
    if isinstance(date_, date):
        date_ = to_timestamp(date_)
    elif not isinstance(date_, str):
        raise AttributeError("date_ must be a string or a datetime.date object")

    url = u"https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/" \
          u"{}.wikipedia.org/all-access/all-agents/{}/daily/{}/{}" \
        .format(lang.lower(), urllib.parse.quote(name), date_, date_)

    response = response_for(url)

    return response["items"][0]["views"]


def get_html(name: str) -> str:
    response = requests.get(f"https://en.wikipedia.org/api/rest_v1/page/html/{name}")

    if response.status_code == 200:
        return response.content.decode("utf-8")


def get_summary(name: str) -> str:
    response = response_for(f"https://en.wikipedia.org/api/rest_v1/page/summary/{name}")

    if response:
        return response["extract"]


def get_media(name: str) -> tuple[dict, ...]:
    response = response_for(f"https://en.wikipedia.org/api/rest_v1/page/media-list/{name}")

    if response:
        return tuple(response["items"])


def get_segments(name: str) -> str:
    # todo Add strict=False option that'll raise an error if response is None
    response = response_for(f"https://en.wikipedia.org/api/rest_v1/page/segments/{name}")

    if response:
        return response["segmentedContent"]


def get_pdf(name: str) -> bytes:
    response = requests.get(f"https://en.wikipedia.org/api/rest_v1/page/pdf/{name}")

    if response.status_code == 200:
        return response.content


def get_page_data(name: str) -> dict:
    response = response_for(f"https://api.wikimedia.org/core/v1/wikipedia/en/page/{name}/bare")
    return response


def response_for(url: str) -> dict | None:
    response = requests.get(url, headers=HEADERS)
    result = json.loads(response.text)

    if response.status_code == 200:
        return result
    elif response.status_code == 400:
        raise AttributeError(f"One or more of the arguments given is invalid. "
                             f"\n{result['title']}: {result['detail']}")
    elif response.status_code == 404:
        if 'title' in result and 'detail' in result:
            raise Exception(f"No page was found. \n{result['title']}: {result['detail']}")
        elif 'messageTranslations' in result and 'en' in result['messageTranslations']:
            raise Exception(result["messageTranslations"]["en"])
    else:
        result = json.loads(response.text)
        print(f"New error: {response.status_code}, {result['title']}: {result['detail']}")
