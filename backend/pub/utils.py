from unidecode import unidecode

from .schema import AuthorSchema


def normalize_author(name: str, affiliation: str | None = None) -> AuthorSchema:
    """
    标准化作者信息。
    """
    names = unidecode(name).lower().strip().split(' ')
    first_name = names[0]
    last_name = names[-1]
    middle_name = ' '.join(names[1:-1]) if len(names) > 2 else None
    return AuthorSchema(
        first_name=first_name,
        middle_name=middle_name,
        last_name=last_name,
        affiliation=affiliation,
    )
