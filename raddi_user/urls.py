from django.conf.urls import url

from .views import (
    CustomAuthToken,
    user_view,
    user_register,
)

urlpatterns = [
    url('^api-token-auth/$', CustomAuthToken.as_view(), name='api_token_auth'),
    url('^register/$', user_register, name='register-user'),
    url('^(?P<pk>[0-9]+)$', user_view, name="user-detail"),
]
