import itertools
import json
import multiprocessing
import re
import sys
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from typing import Iterator, NamedTuple, Optional
from urllib.parse import urljoin

from bs4 import BeautifulSoup
from tqdm import tqdm

from pub.schema import ArxivAuthorSchema, ArxivEntrySchema

from . import common

session = common.get_session()


def fetch_arxiv_metadata(arxiv_ids: list[str]) -> list[ArxivEntrySchema]:
    url = "https://export.arxiv.org/api/query"
    data = {"id_list": ",".join(arxiv_ids), "max_results": len(arxiv_ids)}

    response = session.post(url, data=data)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch metadata: {response.status_code}")

    root = ET.fromstring(response.text)
    ns = {
        "arxiv": "http://arxiv.org/schemas/atom",
        "atom": "http://www.w3.org/2005/Atom",
    }
    entries = root.findall("atom:entry", ns)

    results: list[ArxivEntrySchema] = []
    for entry in entries:
        try:
            result = parse_entry(entry, ns)
            if result is not None:
                results.append(result)
        except Exception as e:
            print(f"Failed to parse entry: {e}", file=sys.stderr)

    return results


def parse_entry(entry: ET.Element, ns: dict) -> Optional[ArxivEntrySchema]:
    # Skip empty entries.
    if entry.find("atom:id", ns) is None:
        return None

    id = entry.find("atom:id", ns).text.split("/")[-1]
    title = entry.find("atom:title", ns).text.strip()
    summary = entry.find("atom:summary", ns).text.strip()
    authors = [parse_author(author, ns) for author in entry.findall("atom:author", ns)]
    comment = entry.find("arxiv:comment", ns)
    published = entry.find("atom:published", ns).text
    updated = entry.find("atom:updated", ns).text
    primary_category = entry.find("arxiv:primary_category", ns).get("term")
    categories = [
        category.get("term") for category in entry.findall("atom:category", ns)
    ]
    link = entry.find("atom:link[@rel='alternate']", ns).get("href")
    pdf = entry.find("atom:link[@title='pdf']", ns).get("href")

    data = {
        "arxiv_id": id,
        "title": title,
        "summary": summary,
        "authors": authors,
        "published": published,
        "updated": updated,
        "primary_category": primary_category,
        "categories": categories,
        "link": link,
        "pdf": pdf,
    }
    if comment is not None:
        data["comment"] = comment.text
    return data


def parse_author(author: ET.Element, ns: dict) -> ArxivAuthorSchema:
    name = author.find("atom:name", ns).text
    affiliation = author.find("arxiv:affiliation", ns)

    data = {
        "name": name,
    }
    if affiliation is not None:
        data["affiliation"] = affiliation.text
    return data


class ArxivIdRange(NamedTuple):
    month: str
    start: int
    end: int

    def arxiv_ids(self) -> list[str]:
        return [f"{self.month}.{i:05d}" for i in range(self.start, self.end + 1)]


def main(args):
    if not args.output and not args.save:
        raise ValueError("No output specified, use --output or --save")

    if args.output:
        out_file = open(args.output, "w")

    if args.save or args.catchup:
        common.setup_database()

    if args.catchup:
        id_ranges = get_catchup_id_ranges()
    else:
        if any(arg is None for arg in (args.month, args.start, args.end)):
            raise ValueError("Month, start, and end must be specified")
        id_ranges = [ArxivIdRange(args.month, args.start, args.end)]

    def filter_result(metadata: ArxivEntrySchema):
        return metadata["primary_category"].startswith(args.category + ".")

    with multiprocessing.Pool(processes=args.jobs) as pool:
        for id_range in id_ranges:
            batches = itertools.batched(id_range.arxiv_ids(), args.batch)
            batches = [list(batch) for batch in batches]

            for results in tqdm(
                pool.imap_unordered(fetch_arxiv_metadata, batches),
                total=len(batches),
                desc=f"Fetching {id_range.month} ({id_range.start}-{id_range.end})",
            ):
                filtered_results = list(filter(filter_result, results))

                if args.save:
                    save_results_to_db(filtered_results)

                if args.output:
                    for result in filtered_results:
                        print(json.dumps(result), file=out_file)

    if args.output:
        out_file.close()


def get_catchup_id_ranges() -> Iterator[ArxivIdRange]:
    from pub.models import ArxivEntry

    latest_entry = ArxivEntry.objects.order_by("-arxiv_id").first()
    assert latest_entry is not None, "No existing entries found"

    m = re.match(r"(\d{4}).(\d{5})v(\d+)", latest_entry.arxiv_id)
    assert m is not None, "Invalid arXiv ID format"

    latest_month = datetime.strptime(m.group(1), "%y%m")
    latest_index = int(m.group(2))
    today = datetime.now()

    while latest_month <= today:
        yield ArxivIdRange(
            month=latest_month.strftime("%y%m"),
            start=latest_index + 1,
            end=get_month_end_index(latest_month),
        )

        latest_month = (latest_month + timedelta(days=31)).replace(day=1)
        latest_index = 0


def get_month_end_index(month: datetime) -> int:
    url = f"https://arxiv.org/list/cs/{month.strftime("%Y-%m")}"
    response = session.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    page_links = soup.find("div", class_="paging").find_all("a")
    if page_links:
        last_page_url = urljoin(url, page_links[-1]["href"])
        response = session.get(last_page_url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

    entries = soup.find("dl", id="articles").find_all("dt")
    last_entry_id = entries[-1].find("a", title="Abstract")["id"]
    return int(last_entry_id.split(".")[-1]) + 1000


def save_results_to_db(results: list[ArxivEntrySchema]):
    from django.db import transaction

    from pub.models import ArxivEntry, ArxivEntryAuthor

    entries: list[ArxivEntry] = []
    author_instances: list[ArxivEntryAuthor] = []

    for result in results:
        entry = ArxivEntry(**result)
        entry.make_slug()
        entries.append(entry)
        author_instances.extend(entry.make_authors())

    with transaction.atomic():
        ArxivEntry.objects.bulk_create(entries, ignore_conflicts=True)
        ArxivEntryAuthor.objects.filter(arxiv_entry__in=entries).delete()
        ArxivEntryAuthor.objects.bulk_create(author_instances)


def parse_args(args=None):
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--month", type=str, help="Year and month in YYMM format")
    parser.add_argument("-s", "--start", type=int, help="Start index")
    parser.add_argument("-e", "--end", type=int, help="End index")
    parser.add_argument(
        "--catchup", action="store_true",
        help="Catch up to the latest index (requires --save, overrides --month, --start, --end)")
    parser.add_argument("-b", "--batch", type=int, default=200, help="Batch size")
    parser.add_argument("--category", type=str, default="cs", help="Primary category")
    parser.add_argument("-j", "--jobs", type=int, default=4, help="Number of jobs")
    parser.add_argument("-o", "--output", type=str, help="Output file path")
    parser.add_argument("--save", action="store_true", help="Save to database")
    return parser.parse_args(args)


if __name__ == "__main__":
    main(parse_args())
