import requests
import json
import datetime

from typing import overload

from .consts import *


def to_timestamp(date: datetime.date | str) -> str:
    if type(date) == datetime.date:
        return date.strftime("%Y%m%d")
    else:  # Convert from format yyyy-mm-ddThh:mm:ssZ
        return date.split('T')[0].replace('-', '')


def from_timestamp(timestamp: str) -> datetime.date:
    if "T" in timestamp:
        date_only: str = timestamp.split('T')[0]
        date_info: tuple[int] = tuple(int(info) for info in date_only.split('-'))
        return datetime.date(date_info[0], date_info[1], date_info[2])
    else:
        return datetime.date(int(timestamp[:5]), int(timestamp[5:7]), int(timestamp[7:9]))


@overload
def id_of_page(name: str, lang: str = LANG) -> int: ...
@overload
def id_of_page(name: str, date: str | datetime.date, lang: str = LANG) -> int: ...


def id_of_page(*args, lang: str = LANG):
    # Validate input
    if len(args) != 1 and len(args) != 2:
        raise AttributeError("Expected 1 or 2 arguments")
    elif type(args[0]) != str:
        raise AttributeError("name argument must be a string")
    elif len(args) == 2 and (type(args[1]) != str and type(args[1]) != datetime.date):
        raise AttributeError("date argument must be a string or a datetime.date object")
    elif type(lang) != str:
        raise AttributeError("lang key-argument must be a string")

    # Set-up arguments
    name = args[0]
    is_date: bool = len(args) == 2

    # Get ID from args
    if is_date:
        date = args[1]

        if type(date) == datetime.date:
            date = to_timestamp(date)

        url = f"https://{lang}.wikipedia.org/w/rest.php/v1/page/{name}/history"

        response = response_for(url)["revisions"]

        # Check timestamps
        for revision in response:
            formatted_timestamp = revision["timestamp"].split('T')[0].replace('-', '')

            if formatted_timestamp <= date:
                return revision["id"]

    else:
        response = response_for(f"https://api.wikimedia.org/core/v1/wikipedia/{lang}/page/{name}/bare")

        return response["id"]


def name_of_page(id: int, lang=LANG) -> str:
    id_details = response_for(f"http://{lang}.wikipedia.org/w/api.php",
                              params={"action": "query", "pageids": id, "format": "json"})

    if "title" in id_details["query"]["pages"][str(id)]:
        return id_details["query"]["pages"][str(id)]["title"]
    else:
        revision_details = response_for(f"https://{lang}.wikipedia.org/w/rest.php/v1/revision/{id}/bare")
        return revision_details["page"]["key"]


def response_for(url: str, params: dict | None = None) -> dict | None:
    response = requests.get(url, headers=HEADERS, params=params)
    result = json.loads(response.text)

    # Handle response errors
    if response.status_code == 200:
        return result
    elif response.status_code == 400:
        raise AttributeError(f"One or more of the arguments given is invalid. "
                             f"\n{result['title']}: {result['detail']}")
    elif response.status_code == 404:
        if 'title' in result and 'detail' in result:
            raise Exception(f"No page was found for {url}. \n{result['title']}: {result['detail']}")
        elif 'messageTranslations' in result and 'en' in result['messageTranslations']:
            raise Exception(result["messageTranslations"]["en"])
    else:
        result = json.loads(response.text)
        print(f"New error: {response.status_code}, {result['title']}: {result['detail']}")
