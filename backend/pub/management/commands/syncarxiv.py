import argparse

from django.core.management.base import BaseCommand
from tqdm import trange

from pub.models import ArxivEntry
from utils.feed_engine import session


class Command(BaseCommand):
    help = '将 arXiv 论文数据上传到推送后端。'

    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument('--batch-size', type=int, default=256)

    def handle(self, *args, **options):
        """
        将 arXiv 论文数据上传到推送后端。
        """
        unsynced_entries = ArxivEntry.objects.filter(synced=False)

        batch_size = options['batch_size']

        for i in trange(0, len(unsynced_entries), batch_size, desc='Syncing arXiv entries'):
            batch = unsynced_entries[i:i + batch_size]
            arxiv_ids = []
            payload = []

            for entry in batch:
                arxiv_ids.append(entry.arxiv_id)
                payload.append({
                    'arxiv_id': entry.arxiv_id,
                    'content': generate_index_text(entry),
                })

            response = session.post('/arxiv/batch', json=payload)
            response.raise_for_status()

            ArxivEntry.objects.filter(arxiv_id__in=arxiv_ids).update(synced=True)


def generate_index_text(arxiv_entry: ArxivEntry) -> str:
    """
    为 arXiv 论文生成用于索引的文本。
    """
    return (
        f"Title: {arxiv_entry.title}\n"
        f"Abstract: {arxiv_entry.summary}\n"
    )
