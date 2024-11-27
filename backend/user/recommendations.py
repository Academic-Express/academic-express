import requests
from .models import Recommendation, User
import arxiv

def fetch_arxiv_papers(topics, max_results=5):
    """
    Fetch papers from arXiv for given topics using the arxiv package.
    
    Args:
        topics (list of str): List of topics to query.
        max_results (int): Maximum number of results per topic.
        
    Returns:
        dict: Dictionary with topic as key and list of papers as value.
    """
    results = {}
    for topic in topics:
        search = arxiv.Search(
            query=topic,
            max_results=max_results,
            sort_by=arxiv.SortCriterion.SubmittedDate
        )
        papers = []
        for result in search.results():
            papers.append({
                "title": result.title,
                "url": result.entry_id,
                "authors": [author.name for author in result.authors],
                "summary": result.summary[:200] + "..."  # Truncate summary for brevity
            })
        results[topic] = papers
    return results

def fetch_github_trending():
    # Example query to fetch GitHub trending repositories
    url = "https://api.github.com/search/repositories?q=stars:>10000&sort=stars"
    response = requests.get(url)
    repos = response.json().get('items', [])
    trending_repos = [
        {"name": repo["name"], "url": repo["html_url"]} for repo in repos[:5]
    ]
    return trending_repos

def generate_recommendations(user: User):
    papers = fetch_arxiv_papers()
    repos = fetch_github_trending()

    for paper in papers:
        Recommendation.objects.create(
            user=user,
            paper_title=paper["title"],
            paper_url=paper["url"],
            repository_name="",
            repository_url=""
        )

    for repo in repos:
        Recommendation.objects.create(
            user=user,
            paper_title="",
            paper_url="",
            repository_name=repo["name"],
            repository_url=repo["url"]
        ) 