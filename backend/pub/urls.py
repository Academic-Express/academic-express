from django.urls import path

from . import views

app_name = 'pub'
urlpatterns = [
    path(
        'arxiv/<str:arxiv_id>',
        views.get_arxiv_entry,
        name='get_arxiv_entry'),
    path(
        'gh/<str:owner>/<str:repo_name>',
        views.get_github_repo,
        name='get_github_repo'),
    path(
        '<str:resource_type>/<str:resource_id>/claim',
        views.resource_claim,
        name='resource_claim'),
]
