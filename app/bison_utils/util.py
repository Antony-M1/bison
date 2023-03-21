import copy
import os
import random
import string
from .constants import (
    SUCCESS_RESPONSE,
    ERROR_RESPONSE,
    CRITICAL_ERROR_RESPONSE,
    UNAUTHORIZED_RESPONSE
)
from django.core.mail import send_mail as mail
from django.conf import settings


def get_200_and_400_response_template():
    sucess = copy.deepcopy(SUCCESS_RESPONSE)
    error = copy.deepcopy(ERROR_RESPONSE)

    return sucess, error


def get_401_and_500_response_template():
    error_401 = copy.deepcopy(UNAUTHORIZED_RESPONSE)
    error_500 = copy.deepcopy(CRITICAL_ERROR_RESPONSE)

    return error_401, error_500


def generate_otp():
    digits = string.digits
    otp = ''.join(random.choice(digits) for i in range(6))
    return otp


def send_mail(subject=None, message=None, from_email=None, recipient_list=None,
              fail_silently=False, auth_user=None, auth_password=None,
              connection=None, html_message=None):
    mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=recipient_list,
        fail_silently=fail_silently,
    )