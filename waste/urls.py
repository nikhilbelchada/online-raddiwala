from rest_framework.routers import SimpleRouter, DefaultRouter
from django.conf.urls import url, include

from .views import (
    WasteViewSet,
)

router = DefaultRouter()
router.register(r'wastes', WasteViewSet, base_name='waste')

urlpatterns = [
    url(r'^', include(router.urls)),
]
