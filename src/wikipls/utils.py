import requests
import json
import urllib.parse
import datetime

from typing import overload, Iterable


LANG = "en"
# HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64"}  # todo Check wiki's docs and change headers
HEADERS = {
    'User-Agent': 'MediaWiki REST API docs examples/0.1 (https://www.mediawiki.org/wiki/API_talk:REST_API)'
}


def to_timestamp(date: datetime.date) -> str:
    return date.strftime("%Y%m%d")


@overload
def get_views(name: str, date: datetime.date, lang: str = LANG) -> int: ...
@overload
def get_views(name: str, date: str, lang: str = LANG) -> int: ...


def get_views(name: str, date: str | datetime.date, lang: str = LANG) -> int:
    if isinstance(date, datetime.date):
        date = to_timestamp(date)
    elif not isinstance(date, str):
        raise AttributeError("date_ must be a string or a datetime.date object")

    url = u"https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/" \
          u"{}.wikipedia.org/all-access/all-agents/{}/daily/{}/{}" \
        .format(lang.lower(), urllib.parse.quote(name), date, date)

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


def get_media_details(name: str) -> tuple[dict, ...]:
    response = response_for(f"https://en.wikipedia.org/api/rest_v1/page/media-list/{name}")

    if response:
        return tuple(response["items"])


def get_image(details: dict[str, ...]) -> bytes:
    src_url = details["srcset"][-1]["src"]
    response = requests.get(f"https:{src_url}", headers=HEADERS)
    return response.content


@overload
def get_all_images(name: str, strict: bool = False) -> tuple[bytes]: ...
@overload
def get_all_images(details: Iterable[dict[str, ...]], strict: bool = False) -> tuple[bytes]: ...


def get_all_images(input: str | Iterable[dict[str, ...]], strict: bool = True) -> tuple[bytes]:
    if type(input) == "str":
        details: Iterable[dict[str, ...]] = get_media_details(input)
    else:
        details = input

    # Check for non-image media
    if strict:
        for media in details:
            if media["type"] != "image":
                raise AttributeError("Media list cannot contain media objects that are not images.")
    else:
        details = tuple(media for media in details if media["type"] == "image")

    [print(image) for image in details]
    all_images = tuple(get_image(image) for image in details)
    print()
    [print(image[:200]) for image in all_images]
    return all_images


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
