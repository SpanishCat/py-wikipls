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
        self.details: dict[str, Any] = get_page_data(name)

        # Map details to class
        self.id: int = self.details["id"]
        self.title: str = self.details["title"]
        self.key: str = self.details["key"]
        self.content_model: str = self.details["content_model"]
        self.license: dict = self.details["license"]
        self.latest: dict = self.details["latest"]
        self.html_url: str = self.details["html_url"]

    def __repr__(self):
        return f"Article({self.title}, {self.id})"

    def __eq__(self, other):
        return self.id == other.id and self.key == other.key

    def get_page(self, date: datetime.date, lang: str = "en"):
        return Page(self, date, lang)

        # todo Revisions


class Page:
    """
    The difference between a wikipy.Page and a wikipy.Article:
    Article - Collection of all versions of all languages of all dates for a single article. A 'collection' of WikiPages
    Page - One specific version of an article, in a specific date and a specific language
    """

    memory: dict = {}

    def __init__(self, article: Article, date: datetime.date, lang="en"):
        self.from_article: Article = article
        self.name = self.from_article.key
        self.date: datetime.date = date
        self.lang: str = lang

        self.details: dict[str, Any] = get_page_data(article.key)

        # Map details to class
        self.id: int = self.details["id"]
        self.title: str = self.details["title"]
        self.key: str = self.details["key"]
        self.content_model: str = self.details["content_model"]
        self.license: dict = self.details["license"]
        self.latest: dict = self.details["latest"]
        self.html_url: str = self.details["html_url"]

    def __repr__(self):
        return f"Page({self.title}, {self.date}, {self.id})"

    def __eq__(self, other):
        return self.id == other.id and self.key == other.key

    @property
    def views(self) -> int:
        if "views" not in self.memory:
            self.memory["views"]: int = get_views(self.name, self.date, self.lang)
        return self.memory["views"]

    @property
    def html(self) -> str:
        if "html" not in self.memory:
            self.memory["html"]: str = get_html(self.name)
        return self.memory["html"]

    @property
    def summary(self) -> str:
        if "summary" not in self.memory:
            self.memory["summary"]: str = get_summary(self.name)
        return self.memory["summary"]

    @property
    def media(self) -> tuple[dict, ...]:
        if "media" not in self.memory:
            self.memory["media"]: tuple[dict, ...] = get_media_details(self.name)
        return self.memory["media"]

    @property
    def as_pdf(self) -> bytes:
        if "pdf_code" not in self.memory:
            self.memory["pdf_code"]: bytes = get_pdf(self.name)
        return self.memory["pdf_code"]

    @property
    def data(self) -> dict[str, Any]:
        if "data" not in self.memory:
            self.memory["data"]: dict = get_page_data(self.name)
        return self.memory["data"]
