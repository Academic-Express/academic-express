from django.urls import path

from . import views

app_name = 'sub'
urlpatterns = [
    path('topics', views.TopicSubscriptionsView.as_view(), name='topic_subscriptions'),
    path('topics/<int:pk>', views.TopicSubscriptionView.as_view(), name='topic_subscription'),
    path('scholars', views.ScholarSubscriptionsView.as_view(), name='scholar_subscriptions'),
    path('scholars/<int:pk>', views.ScholarSubscriptionView.as_view(), name='scholar_subscription'),
]
