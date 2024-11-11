# -*- coding: hebrew -*-

import os
import json
import time
import urllib.parse
import urllib.request
import urllib.error

from datetime import date, timedelta
from typing import Final as Const

from .utils import *

# region Config
# Output
OUT_FORMAT: Const = "json"
OUT_DIR: Const = "out/"
START_DATE: Const = "20231001"

# Misc
TEST_DATE = date(2024, 11, 1)
articles = (
    ("Hamas", "en"),
    ("Palestinian_Islamic_Jihad", "en"),
    ("חמאס", "he"),
    ("הג'יהאד_האסלאמי_הפלסטיני", "he")
)
# endregion


# class Article:
#     def __init__(self, ):
#         url
#         name


class WikiPage:
    """
    The difference between a WikiPage and an Article:
    Article - Collection of all versions of all languages of all dates for a single article. A 'collection' of WikiPages
    WikiPage - One specific version of an article, in a specific date and a specific language
    """
    def __init__(self, name: str, lang="en", date=TEST_DATE): pass
        # self.views_url = get_views(name, date)
        # self.details = response_for(self.views_url)["items"][0]
        #
        # self.lang = lang
        # self.date = date
        # self.name = self.details["article"]
        # self.title = get_title(name)
        # self.views = self.details["views"]

    # todo Set getter functions



def get_page_data(article_name_: str, end_date: str, start_date: str = START_DATE, lang: str = "en") -> tuple[str] | None:
    """
    Extract information and statistics about a certain page of the Wikipedia, from a certain date(s).

    :param article_name_: Title of Wiki entry page.
    :param end_date: Date after which to stop providing data; Format: "yyyymmdd", e.g "20230225" (25.2.2023).
    :param start_date: Date from which to start providing data; Format: "yyyymmdd", e.g "20230225" (25.2.2023).
    :param lang: Language of wiki page (e.g "en", "he", "ru").
    :return: Tuple of data dictionaries for each day checked.
    """

    url = u"https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/" \
          u"{}.wikipedia.org/all-access/all-agents/{}/daily/{}/{}" \
        .format(lang.lower(), urllib.parse.quote(article_name_), start_date, end_date)

    try:
        page = urllib.request.urlopen(url).read()
    except urllib.error.URLError:
        print("Update failed, No internet connection")
        return

    page = page.decode("UTF-8")
    items = tuple(json.loads(page)["items"])
    return items
