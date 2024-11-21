import urllib.parse

from typing import Iterable

from .util_func import *


def get_summary(name: str) -> str:
    response = response_for(f"https://en.wikipedia.org/api/rest_v1/page/summary/{name}")

    if response:
        return response["extract"]


def get_html(name: str) -> str:
    response = requests.get(f"https://en.wikipedia.org/api/rest_v1/page/html/{name}")

    if response.status_code == 200:
        return response.content.decode("utf-8")


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


# region media
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


def get_all_images(image_info: str | Iterable[dict[str, ...]], strict: bool = True) -> tuple[bytes]:
    if type(image_info) == "str":
        details: Iterable[dict[str, ...]] = get_media_details(image_info)
    else:
        details = image_info

    # Check for non-image media
    if strict:
        for media in details:
            if media["type"] != "image":
                raise AttributeError("Media list cannot contain media objects that are not images.")
    else:
        details = tuple(media for media in details if media["type"] == "image")

    all_images = tuple(get_image(image) for image in details)
    return all_images

# endregion


# region data
@overload
def get_page_data(name: str, lang: str = LANG) -> dict[str, ...]: ...
@overload
def get_page_data(name: str, date: str | datetime.date, lang: str = LANG) -> dict[str, ...]: ...
@overload
def get_page_data(id: int, lang: str = LANG) -> dict[str, ...]: ...


def get_page_data(*args, lang: str = LANG) -> dict[str, ...]:
    # Validate arguments
    # You should read it as the rules for valid input (and avoid the "not"s in the beginning)
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

        if is_date:
            date = args[1]
            id = id_of_page(name, date)
        else:
            id = id_of_page(name)

    revision_res = response_for(f"https://{lang}.wikipedia.org/w/rest.php/v1/revision/{id}/bare")
    revision_res.pop("page")
    revision_res.pop("user")
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

        if "title" in id_details["query"]["pages"][str(identifier)]:
            name = id_details["query"]["pages"][str(identifier)]["title"]
        else:
            name = name_of_page(identifier)

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
    # You should read it as the rules for valid input (and avoid the "not"s in the beginning)
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

# endregion
