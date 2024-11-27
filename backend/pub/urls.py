from django.urls import path

from . import views

app_name = 'pub'
urlpatterns = [
    path('arxiv/<str:arxiv_id>', views.get_arxiv_entry, name='get_arxiv_entry'),
    path('gh/<str:owner>/<str:repo>',
         views.get_github_repo, name='get_github_repo'),
    path('collections/', views.list_or_create_collection,
         name='list_or_create_collection'),
    path('collections/<int:collection_id>/',
         views.delete_collection, name='delete_collection'),
    path('collections/groups/', views.list_or_create_collection_group,
         name='list_or_create_collection_group'),
    path('collections/groups/<int:group_id>/', views.retrieve_update_delete_collection_group,
         name='retrieve_update_delete_collection_group'),
]
