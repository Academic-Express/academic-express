from django.urls import path

from . import views

app_name = 'feed'
urlpatterns = [
    path('follow', views.get_follow_feed, name='get_follow_feed'),
    path('subscription', views.get_subscription_feed, name='get_subscription_feed'),
    path('hot', views.get_hot_feed, name='get_hot_feed'),
    path('search', views.get_search_results, name='get_search_results'),
]
