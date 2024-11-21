import json
import os
import urllib.parse
from concurrent.futures import ThreadPoolExecutor

from bs4 import BeautifulSoup
from github import Auth, Github, NamedUser, Repository, UnknownObjectException
from tqdm import tqdm

from pub.schema import GithubAccountSchema, GithubRepoSchema

from . import common


def get_top_repo_names(lang: str = 'python', since: str = 'daily') -> list[str]:
    url = f"https://github.com/trending/{urllib.parse.quote(lang)}"
    params = {"since": since}
    response = common.get_session().get(url, params=params)

    # Check for successful response
    if response.status_code != 200:
        raise Exception(f"Failed to fetch the page. Status code: {response.status_code}")

    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the trending repositories
    repositories = soup.find_all('article', class_='Box-row')
    repo_names = []

    for repository in repositories:
        repo_element = repository.find('h2', class_='h3 lh-condensed').find('a')
        repo_name = repo_element['href'][1:]
        repo_names.append(repo_name)

    return repo_names


def parse_repo(repo: Repository.Repository) -> GithubRepoSchema:
    try:
        readme = repo.get_readme()
    except UnknownObjectException:
        readme = None

    return {
        "repo_id": repo.id,
        "name": repo.name,
        "full_name": repo.full_name,
        "description": repo.description,
        "html_url": repo.html_url,
        "owner": parse_account(repo.owner),
        "created_at": repo.created_at.isoformat(),
        "updated_at": repo.updated_at.isoformat(),
        "pushed_at": repo.pushed_at.isoformat(),
        "homepage": repo.homepage,
        "size": repo.size,
        "language": repo.language,
        "license": repo.license and repo.license.name,
        "topics": repo.topics,
        "stargazers_count": repo.stargazers_count,
        "forks_count": repo.forks_count,
        "open_issues_count": repo.open_issues_count,
        "network_count": repo.network_count,
        "subscribers_count": repo.subscribers_count,
        "readme": readme and readme.decoded_content.decode("utf-8")
    }


def parse_account(account: NamedUser.NamedUser) -> GithubAccountSchema:
    return {
        "login": account.login,
        "id": account.id,
        "type": account.type,
        "avatar_url": account.avatar_url,
    }


def main(args):
    if not args.output and not args.save:
        raise ValueError("No output specified, use --output or --save")

    auth = Auth.Token(args.token)
    g = Github(auth=auth, user_agent=common.USER_AGENT)

    repo_names = get_top_repo_names(args.lang, args.since)
    repo_entry_list = []

    def task(repo_name):
        repo = g.get_repo(repo_name)
        return parse_repo(repo)

    with ThreadPoolExecutor(max_workers=args.jobs) as executor:
        for entry in tqdm(executor.map(task, repo_names), total=len(repo_names)):
            repo_entry_list.append(entry)

    if args.output:
        with open(args.output, 'w') as f:
            json.dump(repo_entry_list, f)
            print(file=f)

    if args.save:
        common.setup_database()
        save_results_to_db(repo_entry_list)


def save_results_to_db(results: list[GithubRepoSchema]):
    from pub.models import GithubRepo

    entries: list[GithubRepo] = []

    for result in results:
        entry = GithubRepo(**result)
        entries.append(entry)

    PK = "repo_id"
    GithubRepo.objects.bulk_create(
        entries,
        update_conflicts=True,
        update_fields=GithubRepoSchema.__annotations__.keys() - {PK},
        unique_fields={PK},
    )


def parse_args(args=None):
    import argparse

    parser = argparse.ArgumentParser(description="Crawl trending GitHub repositories")
    parser.add_argument("--token", type=str, help="GitHub personal access token")
    parser.add_argument("--lang", type=str, default="python", help="Programming language")
    parser.add_argument("--since", choices=["daily", "weekly", "monthly"], default="daily",
                        help="Trending period")
    parser.add_argument("-j", "--jobs", type=int, default=4, help="Number of jobs")
    parser.add_argument("-o", "--output", type=str, help="Output file path")
    parser.add_argument("--save", action="store_true", help="Save to database")

    args = parser.parse_args(args)
    args.token = args.token or os.environ.get("GITHUB_PAT")
    if not args.token:
        parser.error("GitHub personal access token is required.")

    return args


if __name__ == "__main__":
    main(parse_args())
