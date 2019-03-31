from rest_framework.routers import SimpleRouter, DefaultRouter
from django.conf.urls import url, include

from .views import (
    WasteCategoryViewSet,
)

"""
router = SimpleRouter()
router.register(r'waste-categories', WasteCategoryViewSet, basename="waste-category")

urlpatterns = router.urls
"""
router = DefaultRouter()
router.register(r'waste-categories', WasteCategoryViewSet, base_name='waste-category')

urlpatterns = [
    url(r'^', include(router.urls)),
]
