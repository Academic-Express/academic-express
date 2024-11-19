from typing import NotRequired, TypedDict


class ArxivEntrySchema(TypedDict):
    """
    ArXiv 论文。
    """
    arxiv_id: str
    title: str
    summary: str
    authors: list['ArxivAuthorSchema']
    comment: NotRequired[str]
    published: str
    updated: str
    primary_category: str
    categories: list[str]
    link: str
    pdf: str


class ArxivAuthorSchema(TypedDict):
    """
    ArXiv 作者。
    """
    name: str
    affiliation: NotRequired[str]
