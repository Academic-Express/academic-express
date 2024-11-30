from rest_framework_nested import routers
from django.urls import path, include
from .views import CollectionViewSet, CollectionItemViewSet

router = routers.SimpleRouter()
router.register(r'', CollectionViewSet, basename='collection')

collection_router = routers.NestedSimpleRouter(
    router, r'', lookup='collection')
collection_router.register(
    r'items', CollectionItemViewSet, basename='collection-items')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(collection_router.urls)),
]
