import urllib.parse

from bs4 import BeautifulSoup

from pub.schema import ArxivCategorySchema

from . import common


def get_archive_categories(archive: str) -> list[ArxivCategorySchema]:
    """
    获取 ArXiv 分类。
    """
    url = f"https://arxiv.org/archive/{urllib.parse.quote(archive)}"
    response = common.get_session().get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')
    categories = soup.find('div', id='content').find('h2').find_next('ul').find_all('li')

    results = []
    for category in categories:
        title = category.find('b').text
        category_id, name = title.split(' - ', 1)
        description = category.find('div', class_='description').text.strip()
        results.append({
            "category_id": category_id,
            "name": name,
            "description": description,
        })

    return results


def main(args):
    categories = get_archive_categories(args.archive)
    for category in categories:
        print(category)

    if args.save:
        common.setup_database()
        save_results_to_db(categories)


def save_results_to_db(categories):
    from pub.models import ArxivCategory

    entries = [ArxivCategory(**category) for category in categories]
    ArxivCategory.objects.bulk_create(entries)


def parse_args(args=None):
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("archive", type=str, default="cs", help="ArXiv archive")
    parser.add_argument("--save", action="store_true", help="Save the results to the database")

    return parser.parse_args(args)


if __name__ == "__main__":
    main(parse_args())
