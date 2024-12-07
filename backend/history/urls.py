from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('', views.HistoryViewSet, basename='history')

urlpatterns = router.urls
