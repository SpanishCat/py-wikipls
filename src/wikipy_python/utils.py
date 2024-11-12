from datetime import date
import urllib.parse
import urllib.request
import urllib.error
import json

import requests

LANG = "en"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64"}


def to_timestamp(date_: date):
    return date_.strftime("%Y%m%d")


def get_views(name: str, date_: str | date, lang=LANG):
    if isinstance(date_, date):
        date_ = to_timestamp(date_)
    elif not isinstance(date_, str):
        raise AttributeError("date_ must be a string or a datetime.date object")

    url = u"https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/" \
          u"{}.wikipedia.org/all-access/all-agents/{}/daily/{}/{}" \
        .format(lang.lower(), urllib.parse.quote(name), date_, date_)

    response = response_for(url)

    return response["items"][0]["views"]

    # try:
    #     response = urllib.request.urlopen(url).read()
    #     print(response)
    #
    # except urllib.error.HTTPError as err:
    #     print(err)
    #     if 400 in err:
    #         raise AttributeError(f"One of the arguments is invalid. Original error: {err}")
    #
    # except urllib.error.URLError:
    #     raise ConnectionError("Failed to get views: No internet connection")
    #
    # else:
    #     return json.loads(response)["items"][0]["views"]


def get_title(name: str) -> str | None:
    response = response_for(f"https://en.wikipedia.org/api/rest_v1/page/title/{name}")

    if response:
        return response["items"][0]["title"]
    else:
        return None


def get_html(name: str) -> str | None:
    response = requests.get(f"https://en.wikipedia.org/api/rest_v1/page/html/{name}")

    if response.status_code == 200:
        return response.content.decode("utf-8")


def get_summary(name: str) -> str | None:
    response = response_for(f"https://en.wikipedia.org/api/rest_v1/page/summary/{name}")

    if response:
        return response["extract"]


def get_media(name: str) -> tuple | None:
    response = response_for(f"https://en.wikipedia.org/api/rest_v1/page/media-list/{name}")

    if response:
        return tuple(response["items"])


def get_segments(name: str) -> str | None:
    # todo Add strict=False option that'll raise an error if response is None
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

    response = requests.get(url, headers=HEADERS)
    result = json.loads(response.text)

    if response.status_code == 200:
        return result
    elif response.status_code == 400:
        raise AttributeError(f"One or more of the arguments given is invalid. "
                             f"\n{result['title']}: {result['detail']}")
    elif response.status_code == 404:
        raise Exception(f"No page was found. \n{result['title']}: {result['detail']}")
    else:
        result = json.loads(response.text)
        print(f"New error: {response.status_code}, {result['title']}: {result['detail']}")


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
