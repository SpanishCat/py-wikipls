# -*- coding: hebrew -*-
from typing import Any

from .get_func import *
from .type_obj import *


class Article:
    def __init__(self, key: str):
        """
        :param key: Case-sensitive
        """
        self.details: dict[str, Any] = get_article_data(key)

        # Map details to class
        self.title: str = self.details["title"]
        self.key: str = self.details["key"]
        self.id: ArticleId = ArticleId(self.details["id"])
        self.content_model: str = self.details["content_model"]
        self.license: dict = self.details["license"]
        self.html_url: str = self.details["html_url"]

        latest: dict = self.details["latest"]
        latest["id"] = RevisionId(latest["id"])
        self.latest: dict = latest

    def __repr__(self):
        return f"Article({self.title}, {self.id})"

    def __eq__(self, other):
        return self.id == other.revision_id and self.key == other.article_key

    @overload
    def get_page(self, date: datetime.date, lang: str = consts.LANG): ...
    @overload
    def get_page(self, lang: str = consts.LANG): ...

    def get_page(self, *args, lang: str = consts.LANG):
        if len(args) == 0:
            return Page(self.latest["id"], lang=lang, from_article=self)

        elif len(args) == 1 and type(args[0]) == datetime.date:
            return Page(self.key, args[0], lang=lang, from_article=self)

        else:
            raise AttributeError("Unexpected arguments")


# fixme Fix this class
class Page:
    """
    The difference between a wikipls.Page and a wikipls.Article:
    Article - Collection of all versions of all languages of all dates for a single article. A 'collection' of Pages
    Page - One specific version of an article, in a specific date and a specific language
    """

    # todo Make this accept also date: str

    memory: dict = {}
    @overload
    def __init__(self, key: str, date: datetime.date, lang: str = consts.LANG, from_article: Article = None): ...
    @overload
    def __init__(self, page_id: RevisionId, lang: str = consts.LANG, from_article: Article = None): ...

    def __init__(self, *args, lang=consts.LANG, from_article: Article = None):

        # Validate input
        if len(args) == 0:
            raise AttributeError("No arguments were provided")
        elif (len(args) > 2
              or len(args) == 1 and type(args[0]) != RevisionId
              or len(args) == 2 and (type(args[0]) != str or type(args[1]) != datetime.date)):
            raise AttributeError(f"Unexpected arguments. Args: {args}")

        by: str = "key" if len(args) == 2 else "id"
        identifier = args[0]

        # Get details
        if by == "key":
            date = args[1]
            self.article_details: dict[str, Any] = get_article_data(identifier, lang=lang)
            self.page_details: dict[str, Any] = old_get_page_data(identifier, date, lang=lang)
        else:  # using ID
            self.article_details: dict[str, Any] = get_article_data(identifier, lang=lang)
            self.page_details: dict[str, Any] = old_get_page_data(identifier, lang=lang)

        self.from_article: Article | None = from_article

        # Map details to class
        self.title: str = self.article_details["title"]
        self.key: str = self.article_details["key"]
        self.article_id: ArticleId = ArticleId(self.article_details["id"])
        self.lang: str = self.article_details["html_url"].removeprefix("https://")[:2]
        self.content_model: str = self.article_details["content_model"]
        self.license: dict = self.article_details["license"]

        self.revision_id: RevisionId = RevisionId(self.page_details["id"])
        self.date: datetime.date = from_timestamp(self.page_details["timestamp"])
        # todo Add self.html_url

    def __repr__(self):
        return f"Page({self.title}, {self.date}, {self.article_id})"

    def __eq__(self, other):
        return self.article_id == other.revision_id and self.key == other.article_key

    # region Properties
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
            self.memory["data"]: dict = old_get_page_data(self.key)
        return self.memory["data"]

    # endregion

    def get_revision(self):
        return Revision(self.revision_id, lang=self.lang)


class Revision:
    @overload
    def __init__(self, key: str, date: datetime.date, lang: str = consts.LANG): ...
    @overload
    def __init__(self, page_id: RevisionId, lang: str = consts.LANG): ...

    def __init__(self, *args, lang=consts.LANG):
        # Validate input
        if len(args) == 0:
            raise AttributeError("No arguments were provided")
        elif (len(args) > 2
              or len(args) == 1 and type(args[0]) != RevisionId
              or len(args) == 2 and (type(args[0]) != str or type(args[1]) != datetime.date)):
            raise AttributeError(f"Unexpected arguments. Args: {args}")

        by: str = "key" if len(args) == 2 else "id"
        identifier = args[0]

        # Get details
        if by == "key":
            date = args[1]
            self.details: dict[str, Any] = get_revision_data(identifier, date, lang=lang)
        else:  # using ID
            self.details: dict[str, Any] = get_revision_data(identifier, lang=lang)

        # Map details to class
        self.id: RevisionId = RevisionId(self.details["id"])
        self.size: int = self.details["size"]
        self.is_minor: bool = self.details["minor"]
        self.datetime: datetime.datetime = from_timestamp(self.details["timestamp"], out_fmt=datetime.datetime)
        self.content_model: str = self.details["content_model"]
        self.comment: str = self.details["comment"]
        self.delta: int = self.details["delta"]
        self.html_url = self.details["html_url"]

        self.lang: str = self.html_url.removeprefix("https://")[:2]

        self.article_title: str = self.details["page"]["title"]
        self.article_key: str = self.details["page"]["key"]
        self.article_id: ArticleId = self.details["page"]["id"]

        self.license: dict[str: str, str: str] = self.details["license"]
        self.user: dict[str: int, str: str] = self.details["user"]


    def __repr__(self):
        return f"Revision({self.article_title}, {self.datetime}, {self.article_id})"

    def __eq__(self, other):
        return (type(other) == Revision
                and self.article_id == other.article_id
                and self.id == other.id)
