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


@overload
def get_page_data(name: str) -> dict[str, ...]: ...
@overload
def get_page_data(name: str, date: str | datetime.date) -> dict[str, ...]: ...
@overload
def get_page_data(id: int) -> dict[str, ...]: ...


def get_page_data(*args, lang: str = LANG) -> dict[str, ...]:
    # Validate arguments
    # You should read it as the rules for valid input (and avoid the 'not's in the beginning)
    if not (len(args) == 1 or len(args) == 2):
        raise AttributeError(f"Expected 1 or 2 arguments, got {len(args)}")
    elif not (type(args[0]) == str or type(args[0]) == int):
        raise AttributeError(f"name argument must be string or int. Got type {type(args[0])} instead")
    elif len(args) == 2 and not (type(args[1]) == datetime.date or type(args[1]) == str):
        raise AttributeError(f"date argument must be either string or datetime.date")

    is_date: bool = len(args) == 2
    by: str = "name" if type(args[0]) == str else "id"

    if by == "id":
        id = args[0]

    else:  # By name
        name = args[0]

        print(f"{name = }")
        print(f"{is_date = }")

        if is_date:
            date = args[1]
            id = id_of_page(name, date)
        else:
            id = id_of_page(name)

    revision_res = response_for(f"https://{lang}.wikipedia.org/w/rest.php/v1/revision/{id}/bare")

    revision_res.pop("page")
    revision_res.pop("user")
    print(revision_res)

    return revision_res


def get_article_data(identifier: str | int, lang: str = LANG) -> dict[str, ...]:
    if type(identifier) == str:
        by = "name"
    else:
        by = "id"

    if by == "id":
        # Get article name using ID
        id_details = response_for(f"http://en.wikipedia.org/w/api.php",
                                  params={"action": "query", "pageids": identifier, "format": "json"})
        print(f"Article: For ID {identifier} - {id_details['query']['pages'][str(identifier)] = }")

        if "title" in id_details["query"]["pages"][str(identifier)]:
            name = id_details["query"]["pages"][str(identifier)]["title"]
        else:
            name = name_of_page(identifier)

        print(f"Article: {name = }")

    else:
        name = identifier

    response = response_for(f"https://{lang}.wikipedia.org/w/rest.php/v1/page/{name}/bare")

    out_details: dict[str, ...] = {
        "title": response["title"],
        "key": response["key"],
        "id": response["id"],
        "latest": response["latest"],
        "content_model": response["content_model"],
        "license": response["license"],
        "html_url": response["html_url"]
    }

    return out_details


@overload
def get_revision_data(name: str) -> dict[str, ...]: ...
@overload
def get_revision_data(name: str, date: str | datetime.date) -> dict[str, ...]: ...
@overload
def get_revision_data(id: int) -> dict[str, ...]: ...


def get_revision_data(*args, lang: str = LANG) -> dict[str, ...]:
    # Validate arguments
    # You should read it as the rules for valid input (and avoid the 'not's in the beginning)
    if not (len(args) == 1 or len(args) == 2):
        raise AttributeError(f"Expected 1 or 2 arguments, got {len(args)}")
    elif not (type(args[0]) == str or type(args[0]) == int):
        raise AttributeError(f"name argument must be string or int. Got type {type(args[0])} instead")
    elif len(args) == 2 and not (type(args[1]) == datetime.date or type(args[1]) == str):
        raise AttributeError(f"date argument must be either string or datetime.date")

    if type(args[0]) == str:
        by = "name"
    else:
        by = "id"

    is_date: bool = len(args) == 2
    # if type(args[0] == str):
    #     name = args[0]
    # else:
    #     id = args[0]

    if by == "id":
        id = args[0]

    else:   # By name
        name = args[0]

        if is_date:
            date = args[1]
            id = id_of_page(name, date)

        else:
            id = id_of_page(name)

    response = response_for(f"https://{lang}.wikipedia.org/w/rest.php/v1/revision/{id}/bare")
    return response

    # if is_date:
    #     date = args[1]
    #     if type(date) == str:
    #
    #         pass
    #         # response = response_for()


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


