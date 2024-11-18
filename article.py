# -*- coding: hebrew -*-
from typing import Any

from .utils import *

# Config
TEST_DATE = datetime.date(2024, 11, 1)


class Article:
    def __init__(self, name: str):
        """
        :param name: Case-sensitive
        """
        self.details: dict[str, Any] = get_article_data(name)

        # Map details to class
        self.name: str = self.details["title"]
        self.key: str = self.details["key"]
        self.id: str = self.details["id"]
        self.content_model: str = self.details["content_model"]
        self.license: dict = self.details["license"]
        self.latest: dict = self.details["latest"]
        self.html_url: str = self.details["html_url"]

    def __repr__(self):
        return f"Article({self.name}, {self.id})"

    def __eq__(self, other):
        return self.id == other.revision_id and self.key == other.key

    @overload
    def get_page(self, date: datetime.date, lang: str = "en"): ...
    @overload
    def get_page(self, lang: str = "en"): ...

    def get_page(self, *args, lang: str = "en"):
        if len(args) == 0:
            return Page(self.latest["id"], lang=lang)

        elif len(args) == 1 and type(args[0]) == datetime.date:
            return Page(self.key, args[0], lang=lang)

        else:
            raise AttributeError("Unexpected arguments")


class Page:
    """
    The difference between a wikipls.Page and a wikipls.Article:
    Article - Collection of all versions of all languages of all dates for a single article. A 'collection' of WikiPages
    Page - One specific version of an article, in a specific date and a specific language
    """

    # todo Make this accept also date: str

    memory: dict = {}
    @overload
    def __init__(self, name: str, date: datetime.date, lang="en"): ...
    @overload
    def __init__(self, page_id: int): ...

    def __init__(self, *args, lang=LANG):

        # Validate input
        if len(args) == 0:
            raise AttributeError("No arguments were provided")
        elif (len(args) > 2
              or len(args) == 1 and type(args[0]) != int
              or len(args) == 2 and (type(args[0]) != str or type(args[1]) != datetime.date)):
            raise AttributeError(f"Unexpected arguments. Args: {args}")

        using: str = "details" if len(args) == 2 else "id"
        identifier = args[0]

        # Get details
        if using == "details":
            date = args[1]
            self.article_details: dict[str, Any] = get_article_data(identifier, lang=lang)
            self.page_details: dict[str, Any] = get_page_data(identifier, date, lang=lang)
        else:  # using ID
            self.article_details: dict[str, Any] = get_article_data(identifier, lang=lang)
            self.page_details: dict[str, Any] = get_page_data(identifier, lang=lang)

        # self.title: Article = self.details["title"] # todo If got from Article object

        # Map details to class
        self.name: str = self.article_details["title"]
        self.key: str = self.article_details["key"]
        self.article_id: int = self.article_details["id"]
        self.lang: str = self.article_details["html_url"].removeprefix("https://")[:2]
        self.content_model: str = self.article_details["content_model"]
        self.license: dict = self.article_details["license"]

        self.revision_id: int = self.page_details["id"]
        self.date: datetime.date = from_timestamp(self.page_details["timestamp"])
        # todo Add self.html_url

    def __repr__(self):
        return f"Page({self.name}, {self.date}, {self.article_id})"

    def __eq__(self, other):
        return self.article_id == other.revision_id and self.key == other.key

    @property
    def views(self) -> int:
        if "views" not in self.memory:
            self.memory["views"]: int = get_views(self.key, self.date, self.lang)
        return self.memory["views"]

    @property
    def html(self) -> str:
        if "html" not in self.memory:
            self.memory["html"]: str = get_html(self.key)
        return self.memory["html"]

    @property
    def summary(self) -> str:
        if "summary" not in self.memory:
            self.memory["summary"]: str = get_summary(self.key)
        return self.memory["summary"]

    @property
    def media(self) -> tuple[dict, ...]:
        if "media" not in self.memory:
            self.memory["media"]: tuple[dict, ...] = get_media_details(self.key)
        return self.memory["media"]

    @property
    def as_pdf(self) -> bytes:
        if "pdf_code" not in self.memory:
            self.memory["pdf_code"]: bytes = get_pdf(self.key)
        return self.memory["pdf_code"]

    @property
    def data(self) -> dict[str, Any]:
        if "data" not in self.memory:
            self.memory["data"]: dict = get_page_data(self.key)
        return self.memory["data"]
