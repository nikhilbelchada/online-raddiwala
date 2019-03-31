from rest_framework.routers import SimpleRouter, DefaultRouter
from django.conf.urls import url, include

from .views import (
    OrderViewSet,
    feedback_reply_view,
)

router = DefaultRouter()
router.register(r'orders', OrderViewSet, base_name='order')

urlpatterns = [
    url(r'^orders/feedbacks/(?P<pk>[0-9]+)/$', feedback_reply_view),
    url(r'^', include(router.urls)),
]
