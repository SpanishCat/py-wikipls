# -*- coding: hebrew -*-
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


class Article:
    def __init__(self, ):
        pass
    # todo


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
