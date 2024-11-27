from typing import NotRequired, Optional, TypedDict


class AuthorSchema(TypedDict):
    """
    作者。
    """
    first_name: str
    middle_name: Optional[str]
    last_name: str
    affiliation: Optional[str]


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


class ArxivCategorySchema(TypedDict):
    """
    ArXiv 分类。
    """
    category_id: str
    name: str
    description: str


class GithubRepoSchema(TypedDict):
    """
    GitHub 仓库。
    """
    repo_id: str
    name: str
    full_name: str
    description: Optional[str]
    html_url: str
    owner: 'GithubAccountSchema'

    created_at: str
    updated_at: str
    pushed_at: str

    homepage: Optional[str]
    size: int
    language: Optional[str]
    license: Optional[str]
    topics: list[str]

    stargazers_count: int
    forks_count: int
    open_issues_count: int
    network_count: int
    subscribers_count: int

    readme: Optional[str]


class GithubAccountSchema(TypedDict):
    """
    GitHub 用户。
    """
    login: str
    id: int
    type: str
    avatar_url: str
