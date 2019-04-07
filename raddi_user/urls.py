from django.conf.urls import url

from .views import (
    CustomAuthToken,
    user_view,
    user_register,
    users_view,
    change_password_view,
)

urlpatterns = [
    url('^api-token-auth/$', CustomAuthToken.as_view(), name='api_token_auth'),
    url('^register/$', user_register, name='register-user'),
    url('^users/$', users_view, name='user-list'),
    url('^change-password/(?P<pk>[0-9]+)$', change_password_view, name='change_password'),
    url('^(?P<pk>[0-9]+)$', user_view, name="user-detail"),
]
