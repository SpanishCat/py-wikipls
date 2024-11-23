import urllib.parse

from typing import Iterable

from .util_func import *


def get_summary(key: str) -> str:
    response = response_for(f"https://en.wikipedia.org/api/rest_v1/page/summary/{key}")

    if response:
        return response["extract"]


def get_html(key: str) -> str:
    response = requests.get(f"https://en.wikipedia.org/api/rest_v1/page/html/{key}")

    if response.status_code == 200:
        return response.content.decode("utf-8")


def get_segments(key: str) -> str:
    # todo Add strict=False option that'll raise an error if response is None
    response = response_for(f"https://en.wikipedia.org/api/rest_v1/page/segments/{key}")

    if response:
        return response["segmentedContent"]


def get_pdf(key: str) -> bytes:
    response = requests.get(f"https://en.wikipedia.org/api/rest_v1/page/pdf/{key}")

    if response.status_code == 200:
        return response.content


@overload
def get_views(key: str, date: datetime.date, lang: str = consts.LANG) -> int: ...
@overload
def get_views(key: str, date: str, lang: str = consts.LANG) -> int: ...


def get_views(key: str, date: str | datetime.date, lang: str = consts.LANG) -> int:
    if isinstance(date, datetime.date):
        date = to_timestamp(date)
    elif not isinstance(date, str):
        raise AttributeError("date must be a string or a datetime.date object")

    url = u"https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/" \
          u"{}.wikipedia.org/all-access/all-agents/{}/daily/{}/{}" \
        .format(lang.lower(), urllib.parse.quote(key), date, date)

    response = response_for(url)

    return response["items"][0]["views"]


# region media
def get_media_details(key: str) -> tuple[dict, ...]:
    response = response_for(f"https://en.wikipedia.org/api/rest_v1/page/media-list/{key}")

    if response:
        return tuple(response["items"])


def get_image(details: dict[str, ...]) -> bytes:
    src_url = details["srcset"][-1]["src"]
    response = requests.get(f"https:{src_url}", headers=consts.HEADERS)
    return response.content


@overload
def get_all_images(key: str, strict: bool = False) -> tuple[bytes]: ...
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
def old_get_page_data(key: str, lang: str = consts.LANG) -> dict[str, ...]: ...
@overload
def old_get_page_data(key: str, date: str | datetime.date, lang: str = consts.LANG) -> dict[str, ...]: ...
@overload
def old_get_page_data(id: RevisionId, lang: str = consts.LANG) -> dict[str, ...]: ...


def old_get_page_data(*args, lang: str = consts.LANG) -> dict[str, ...]:
    # Validate arguments
    # You should read it as the rules for valid input (and avoid the "not"s in the beginning)
    if not (len(args) == 1 or len(args) == 2):
        raise AttributeError(f"Expected 1 or 2 arguments, got {len(args)}")
    elif not (type(args[0]) == str or type(args[0]) == RevisionId):
        raise AttributeError(f"key argument must be string or RevisionId. Got type {type(args[0])} instead")
    elif len(args) == 2 and not (type(args[1]) == datetime.date or type(args[1]) == str):
        raise AttributeError(f"date argument must be either string or datetime.date")

    is_date: bool = len(args) == 2
    by: str = "key" if type(args[0]) == str else "id"

    if by == "id":
        id = args[0]

    else:  # By key
        key = args[0]

        if is_date:
            date = args[1]
            id = id_of_page(key, date)
        else:
            id = id_of_page(key)

    revision_res = response_for(f"https://{lang}.wikipedia.org/w/rest.php/v1/revision/{id}/bare")
    revision_res.pop("page")
    revision_res.pop("user")
    return revision_res


@overload
def get_page_data(key: str, lang: str = consts.LANG) -> dict[str, ...]: ...
@overload
def get_page_data(key: str, date: str | datetime.date, lang: str = consts.LANG) -> dict[str, ...]: ...
@overload
def get_page_data(id: RevisionId, lang: str = consts.LANG) -> dict[str, ...]: ...


def get_page_data(*args, lang: str = consts.LANG) -> dict[str, ...]:
    # Validate arguments
    # You should read it as the rules for valid input (and avoid the "not"s in the beginning)
    if not (len(args) == 1 or len(args) == 2):
        raise AttributeError(f"Expected 1 or 2 arguments, got {len(args)}")
    elif not (type(args[0]) == str or type(args[0]) == RevisionId):
        raise AttributeError(f"key argument must be string or RevisionId. Got type {type(args[0])} instead")
    elif len(args) == 2 and not (type(args[1]) == datetime.date or type(args[1]) == str):
        raise AttributeError(f"date argument must be either string or datetime.date")

    is_date: bool = len(args) == 2
    by: str = "key" if type(args[0]) == str else "id"

    if by == "id":
        id: RevisionId = args[0]
        key: str = key_of_page(id)

    else:  # By key
        key: str = args[0]

        if is_date:
            date: datetime.date = args[1]
            id: RevisionId = id_of_page(key, date)
        else:
            id: RevisionId = id_of_page(key)

    # revision_res = requests.get(f"https://{lang}.wikipedia.org/w/index.php",
    #                             params={"title": key, "oldid": id})

    # Taken from Method 2: https://www.mediawiki.org/wiki/API:Get_the_contents_of_a_page
    revision_res = requests.get(f"https://{lang}.wikipedia.org/w/api.php",
                                params={"action": "parse",
                                        "oldid": id,
                                        "format": "json",
                                        "prop": "text",
                                        "formatversion": 2
                                        })
    print(revision_res.url)
    # print(f"https://{lang}.wikipedia.org/w/index.php?title={key}&oldid={id}")
    return revision_res.content # todo sort the JSON data


def get_article_data(identifier: str | ArticleId, lang: str = consts.LANG) -> dict[str, ...]:
    if type(identifier) == str:
        by = "key"
    else:
        by = "id"

    if by == "id":
        # Get article key using ID
        id_details = response_for(f"http://en.wikipedia.org/w/api.php",
                                  params={"action": "query", "pageids": identifier, "format": "json"})

        # fixme: Needs to get key not title
        if "title" in id_details["query"]["pages"][str(identifier)]:
            key = id_details["query"]["pages"][str(identifier)]["title"]
        else:
            key = key_of_page(identifier)

    else:
        key = identifier

    response = response_for(f"https://{lang}.wikipedia.org/w/rest.php/v1/page/{key}/bare")

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
def get_revision_data(key: str) -> dict[str, ...]: ...
@overload
def get_revision_data(key: str, date: str | datetime.date) -> dict[str, ...]: ...
@overload
def get_revision_data(id: RevisionId) -> dict[str, ...]: ...


def get_revision_data(*args, lang: str = consts.LANG) -> dict[str, ...]:
    # Validate arguments
    # You should read it as the rules for valid input (and avoid the "not"s in the beginning)
    if not (len(args) == 1 or len(args) == 2):
        raise AttributeError(f"Expected 1 or 2 arguments, got {len(args)}")
    elif not (type(args[0]) == str or type(args[0]) == RevisionId):
        raise AttributeError(f"key argument must be string or int. Got type {type(args[0])} instead")
    elif len(args) == 2 and not (type(args[1]) == datetime.date or type(args[1]) == str):
        raise AttributeError(f"date argument must be either string or datetime.date")

    if type(args[0]) == str:
        by = "key"
    else:
        by = "id"

    is_date: bool = len(args) == 2
    # if type(args[0] == str):
    #     name = args[0]
    # else:
    #     id = args[0]

    if by == "id":
        id = args[0]

    else:   # By key
        key = args[0]

        if is_date:
            date = args[1]
            id = id_of_page(key, date)

        else:
            id = id_of_page(key)

    response = response_for(f"https://{lang}.wikipedia.org/w/rest.php/v1/revision/{id}/bare")
    return response

    # if is_date:
    #     date = args[1]
    #     if type(date) == str:
    #
    #         pass
    #         # response = response_for()

# endregion
