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
        '<str:resource>/<str:resource_id>/claim',
        views.get_resource_claims,
        name='get_resource_claims'),
    path(
        '<str:resource>/<str:resource_id>/claim/toggle',
        views.toggle_resource_claim,
        name='toggle_resource_claim'),
]
