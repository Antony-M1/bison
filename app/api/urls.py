from django.urls import path
from .authentication import (
    LogInAPI, SignUpAPI, VerifyOTPAPI
)


urlpatterns = [
    path('sign-up', SignUpAPI.as_view(), name='sign-up'),
    path('login', LogInAPI.as_view(), name='login'),
    path('verify-otp', VerifyOTPAPI.as_view(), name='verify-otp'),
]
