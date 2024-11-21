from dataclasses import dataclass

from .util_func import name_of_page


@dataclass
class Id(int):
    id: int

    def __post_init__(self):
        if self.id < 0:
            raise ValueError(f"ID cannot be negative ({self.id})")

    def __repr__(self):
        return str(self.id)

    def __int__(self):
        return self.id

    def to_name(self):
        return name_of_page(self.id)


@dataclass(repr=False)
class ArticleId(Id): pass
@dataclass(repr=False)
class RevisionId(Id): pass
