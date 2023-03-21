import uuid
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, AbstractUser, User
)
from rest_framework_simplejwt.tokens import RefreshToken
from app.bison_utils.util import generate_otp


class CustomUserManager(BaseUserManager):

    def get_by_natural_key(self, username=None, email=None):
        if email:
            return self.get(email=email)
        elif username:
            return self.get(username=username)


class User(AbstractUser):
    user_id = models.UUIDField(default=uuid.uuid4, primary_key=True,
                               unique=True)
    otp = models.CharField(max_length=6, null=True, blank=True,
                           default=generate_otp)
    otp_time = models.DateTimeField(auto_now=True)
    is_verified = models.BooleanField(default=False)
    email = models.EmailField(max_length=255, unique=True, db_index=True)

    objects = CustomUserManager()

    def tokens(self):
        """return the user tokens"""
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

    class Meta:
        db_table = 'bison_user'
