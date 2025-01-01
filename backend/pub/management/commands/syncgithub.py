import argparse

from django.core.management.base import BaseCommand
from tqdm import trange

from pub.models import GithubRepo
from utils.feed_engine import session


class Command(BaseCommand):
    help = '将 GitHub 仓库数据上传到推送后端。'

    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument('--batch-size', type=int, default=256)
        parser.add_argument('--all', action='store_true', help='上传所有数据')

    def handle(self, *args, **options):
        if options['all']:
            unsynced_repos = GithubRepo.objects.all()
        else:
            unsynced_repos = GithubRepo.objects.filter(synced=False)

        batch_size = options['batch_size']

        for i in trange(0, len(unsynced_repos), batch_size, desc='Syncing GitHub repos'):
            batch = unsynced_repos[i:i + batch_size]
            repo_names = []
            payload = []

            for repo in batch:
                repo_names.append(repo.full_name)
                payload.append({
                    'entry_id': repo.full_name,
                    'content': generate_index_text(repo),
                })

            response = session.post('/github/batch', json=payload)
            response.raise_for_status()

            GithubRepo.objects.filter(full_name__in=repo_names).update(synced=True)

        response = session.post('/save')
        response.raise_for_status()

        self.stdout.write(self.style.SUCCESS('Successfully synced GitHub repos.'))


def generate_index_text(github_repo: GithubRepo) -> str:
    """
    为 GitHub 仓库生成用于索引的文本。
    """
    return (
        f"Repository: {github_repo.name}\n"
        f"Description: {github_repo.description}\n"
        f"Topics: {', '.join(github_repo.topics)}\n"
    )
