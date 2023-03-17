import uuid
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from rest_framework_simplejwt.tokens import RefreshToken

# Create your models here.


class UserManager(BaseUserManager):

    def create_user(self, **kwargs):
        '''
        This function override from the BaseUserManager
        https://docs.djangoproject.com/en/4.0/ref/contrib/auth/#manager-methods
        Same as create_superuser(),
        but sets is_staff and is_superuser to False.
        '''
        user = kwargs
        if user['username'] is None:
            raise TypeError('username must not be None')
        if user['email'] is None:
            raise TypeError('email must not be None')

        user_ = self.model(
            username=user['username'],
            email=self.normalize_email(user['email']),
            phone_number=user.get('country_code', '') + user.
            get('phone_number', ''),
            referal_code=user.get('referal_code')
        )
        user_.set_password(user['password'])
        user_.save(self._db)
        return user_

    def create_superuser(self, username, email, password=None):
        '''
        This function override from the BaseUserManager
        https://docs.djangoproject.com/en/4.0/ref/contrib/auth/#manager-methods
        Same as create_user(), but sets is_staff and is_superuser to True.
        '''
        if password is None:
            raise TypeError('password must not be None')

        user = self.create_user(username=username,
                                email=email,
                                password=password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    user_id = models.UUIDField(default=uuid.uuid4, primary_key=True,
                               unique=True)
    username = models.CharField(max_length=255, unique=True, db_index=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    email = models.EmailField(max_length=255, unique=True, db_index=True,
                              null=False, blank=False)
    phone_number = models.CharField(max_length=15, unique=True, null=True,
                                    blank=True)
    is_email_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    REQUIRED_FIELDS = ['email']
    USERNAME_FIELD = 'username'

    # objects = UserManager()

    def __str__(self):
        return self.email

    def tokens(self):
        """return the user tokens"""
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

    class Meta:
        db_table = 'bison_user'
