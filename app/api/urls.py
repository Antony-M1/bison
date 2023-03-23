from django.urls import path
from .authentication import (
    LogInAPI, SignUpAPI, VerifyOTPAPI,
    ChangePasswordAPI, ForgotPasswordOTPAPI, ForgotPasswordAPI
)
from django.contrib.auth import views as django_views
from django.contrib.auth.urls import urlpatterns as django_urlpatterns

urlpatterns = [
    path('sign-up', SignUpAPI.as_view(), name='sign-up'),
    path('login', LogInAPI.as_view(), name='login'),
    path('verify-otp', VerifyOTPAPI.as_view(), name='verify-otp'),
    path('change-password', ChangePasswordAPI.as_view(),
         name='change-password'),
    path('forgot-password-otp', ForgotPasswordOTPAPI.as_view(),
         name='forgot-password-otp'),
    path('forgot-password', ForgotPasswordAPI.as_view(),
         name='forgot-password')

]
