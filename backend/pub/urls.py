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
        'claim/<str:resource_type>/<str:resource_id>',
        views.ResourceClaimView.as_view(),
        name='resource_claim'),
]
