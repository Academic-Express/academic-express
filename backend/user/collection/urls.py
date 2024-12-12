from rest_framework.routers import DefaultRouter

from .views import CollectionGroupViewSet, CollectionViewSet

app_name = 'collection'

router = DefaultRouter(trailing_slash=False)
router.register(r'groups', CollectionGroupViewSet, basename='collectiongroup')
router.register(r'', CollectionViewSet, basename='collection')

urlpatterns = router.urls
