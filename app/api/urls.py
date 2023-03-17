from django.urls import path
from .authentication import (
    LogInAPI, SignUpAPI,
    test
)


urlpatterns = [
    path('sign-up', SignUpAPI.as_view(), name='sign-up'),
    path('login', LogInAPI.as_view(), name='login'),
    path('test', test, name='test'),
]
