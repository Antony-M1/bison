import copy
import uuid
import datetime
from django.urls import reverse
from rest_framework import status
import pytest
from rest_framework.test import APIClient
from app.models import User
from app.bison_utils.constants import OTP_EXPIRE_TIME
from app.bison_utils.util import generate_otp


client = APIClient()

signup_json_body = {
    'username': 'testuser',
    'email': 'testuser@example.com',
    'password': 'testpassword',
    'confirm_password': 'testpassword'
}


@pytest.mark.django_db
def test_signup_api_create(client):
    url = reverse('sign-up')
    data = copy.deepcopy(signup_json_body)
    response = client.post(url, data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['status_code'] == status.HTTP_201_CREATED

    # integrity check
    response = client.post(url, data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data['status_code'] == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_signup_api_remove_email(client):
    url = reverse('sign-up')
    data = copy.deepcopy(signup_json_body)
    del data['email']
    response = client.post(url, data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data['status_code'] == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_signup_api_missmatch_password(client):
    url = reverse('sign-up')
    data = copy.deepcopy(signup_json_body)
    data['password'] = 'testpassword-new'
    response = client.post(url, data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data['status_code'] == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_signup_api_minimum_password_length(client):
    url = reverse('sign-up')
    data = copy.deepcopy(signup_json_body)
    data['password'] = '1234567'
    data['confirm_password'] = '1234567'
    response = client.post(url, data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data['status_code'] == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_signup_api_incorrect_email_format(client):
    url = reverse('sign-up')
    data = copy.deepcopy(signup_json_body)
    data['email'] = 'testuser.com'
    response = client.post(url, data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data['status_code'] == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_otp_verification_api(user_data):
    user = User.objects.get(
        user_id=str(user_data.data.get('data').get('user_id'))
        )
    url = reverse('verify-otp')
    data = {
        'user_id': user.user_id,
        'otp': user.otp
    }
    response = client.patch(url, data)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_otp_verification_api_invalid_otp(user_data):
    user = User.objects.get(
            user_id=str(user_data.data.get('data').get('user_id'))
           )
    url = reverse('verify-otp')
    data = {
        'user_id': user.user_id,
        'otp': "0000000"
    }
    response = client.patch(url, data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_otp_verification_api_invalid_user_id(user_data):
    url = reverse('verify-otp')
    user_id = None

    def generate_user_id():
        user_id = str(uuid.uuid4())
        if User.objects.filter(user_id=user_id).exists():
            generate_user_id()
        return user_id
    if user_id is None:
        user_id = generate_user_id()

    data = {
        'user_id': user_id,
        'otp': "0000000"
    }
    response = client.patch(url, data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_otp_verification_api_otp_expired(user_data):
    user = User.objects.get(
                user_id=str(user_data.data.get('data').get('user_id'))
           )
    url = reverse('verify-otp')
    user.otp_time = (
        user.otp_time - datetime.timedelta(minutes=OTP_EXPIRE_TIME+5)
        )
    user.save()
    data = {
        'user_id': user.user_id,
        'otp': user.otp
    }
    response = client.patch(url, data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


# pytestmark = pytest.mark.django_db


@pytest.mark.django_db
class TestLoginAPI:
    url = reverse('login')

    def test_login_api_email_password(self, user_data):
        user = User.objects.get(
                    user_id=str(user_data.data.get('data').get('user_id'))
                )
        user.is_verified = True
        user.save()
        data = {
            "email": user.email,
            "password": 'testpassword'
        }
        response = client.post(self.url, data)
        assert response.status_code == status.HTTP_200_OK

    def test_login_api_username_password(self, user_data):
        user = User.objects.get(
                    user_id=str(user_data.data.get('data').get('user_id'))
                )
        user.is_verified = True
        user.save()
        data = {
            "username": user.username,
            "password": 'testpassword'
        }
        response = client.post(self.url, data)
        assert response.status_code == status.HTTP_200_OK

    def test_login_api_invalid_email_password(self, user_data):
        data = {
            "email": 'invalid.email@example.com',
            "password": 'invalidpassword'
        }
        response = client.post(self.url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_login_api_invalid_username_password(self, user_data):
        data = {
            "username": 'invalidusername',
            "password": 'invalidpassword'
        }
        response = client.post(self.url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_login_api_without_password(self):
        data = {
            "username": 'testuser',
        }
        response = client.post(self.url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_login_api_without_email_and_username(self):
        data = {
            "password": 'testpassword',
        }
        response = client.post(self.url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestChangePasswordAPI:
    url = reverse('change-password')

    def test_change_password_api(self, user_data):
        data = {
            "user_id": str(user_data.data.get('data').get('user_id')),
            "old_password": 'testpassword',
            "new_password": 'testpassword1',
            "confirm_password": 'testpassword1'
        }
        response = client.patch(self.url, data)
        assert response.status_code == status.HTTP_200_OK

        response = client.patch(self.url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_change_password_api_invalid_old_password(self, user_data):
        data = {
            "user_id": str(user_data.data.get('data').get('user_id')),
            "old_password": 'testpassword-invalid',
            "new_password": 'testpassword1',
            "confirm_password": 'testpassword1'
        }
        response = client.patch(self.url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_change_password_api_new_password_and_confirm_password_mismatch(
            self, user_data):
        data = {
            "user_id": str(user_data.data.get('data').get('user_id')),
            "old_password": 'testpassword',
            "new_password": 'testpassword1',
            "confirm_password": 'testpassword2'
        }
        response = client.patch(self.url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_change_password_api_without_user_id(self, user_data):
        data = {
            "old_password": 'testpassword',
            "new_password": 'testpassword1',
            "confirm_password": 'testpassword2'
        }
        response = client.patch(self.url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_change_password_api_without_old_password(self, user_data):
        data = {
            "user_id": str(user_data.data.get('data').get('user_id')),
            "new_password": 'testpassword1',
            "confirm_password": 'testpassword2'
        }
        response = client.patch(self.url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_change_password_api_without_new_password(self, user_data):
        data = {
            "user_id": str(user_data.data.get('data').get('user_id')),
            "old_password": 'testpassword',
            "confirm_password": 'testpassword2'
        }
        response = client.patch(self.url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_change_password_api_without_confirm_password(self, user_data):
        data = {
            "user_id": str(user_data.data.get('data').get('user_id')),
            "old_password": 'testpassword',
            "new_password": 'testpassword1'
        }
        response = client.patch(self.url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_change_password_api_empty_json_body(self, user_data):
        data = {}
        response = client.patch(self.url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestForgotPasswordOTPAPI:
    url = reverse('forgot-password-otp')

    def test_forgot_password_otp_api(self, user_data):
        data = {
            'user_id': user_data.data.get('data').get('user_id')
        }
        response = client.post(self.url, data)
        assert response.status_code == status.HTTP_200_OK

    def test_forgot_password_otp_api_invalid_user_id(self, user_data):
        user_id = None

        def generate_user_id():
            user_id = str(uuid.uuid4())
            if User.objects.filter(user_id=user_id).exists():
                generate_user_id()
            return user_id
        if user_id is None:
            user_id = generate_user_id()

        data = {
            'user_id': user_id
        }
        response = client.post(self.url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_forgot_password_otp_api_empty_json_body(self):
        data = {}
        response = client.post(self.url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestForgotPasswordAPI:
    url = reverse('forgot-password')

    def test_forgot_password_api(self, user_data):
        user_id = user_data.data.get('data').get('user_id')
        user = User.objects.get(user_id=user_id)
        data = {
            'user_id': user_id,
            'new_password': 'testpassword1',
            'confirm_password': 'testpassword1',
            'otp': user.otp
        }
        response = client.patch(self.url, data)
        assert response.status_code == status.HTTP_200_OK

    def test_forgot_password_api_invalid_user_id(self, user_data):
        user_id = None

        def generate_user_id():
            user_id = str(uuid.uuid4())
            if User.objects.filter(user_id=user_id).exists():
                generate_user_id()
            return user_id
        if user_id is None:
            user_id = generate_user_id()

        data = {
            'user_id': user_id,
            'new_password': 'testpassword1',
            'confirm_password': 'testpassword1',
            'otp': '000000'
        }
        response = client.patch(self.url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_forgot_password_api_empty_json_body(self, user_data):
        data = {}
        response = client.patch(self.url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_forgot_password_api_invalid_otp(self, user_data):
        user_id = user_data.data.get('data').get('user_id')
        user = User.objects.get(user_id=user_id)

        def generate_otp_test():
            otp = generate_otp()
            if user.otp == otp:
                generate_otp_test()
            else:
                return otp
        otp = generate_otp_test()
        data = {
            'user_id': user_id,
            'new_password': 'testpassword1',
            'confirm_password': 'testpassword1',
            'otp': otp,
        }
        response = client.patch(self.url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_forgot_password_api_invalid_new_password(self, user_data):
        user_id = user_data.data.get('data').get('user_id')
        user = User.objects.get(user_id=user_id)
        data = {
            'user_id': user_id,
            'new_password': 'testpassword1',
            'confirm_password': 'testpassword2',
            'otp': user.otp,
        }
        response = client.patch(self.url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_forgot_password_api_without_user_id(self, user_data):
        data = {
            'new_password': 'testpassword1',
            'confirm_password': 'testpassword1',
            'otp': '000000'
        }
        response = client.patch(self.url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_forgot_password_api_without_new_password(self, user_data):
        data = {
            'user_id': user_data.data.get('data').get('user_id'),
            'confirm_password': 'testpassword1',
            'otp': '000000'
        }
        response = client.patch(self.url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_forgot_password_api_without_confirm_password(self, user_data):
        data = {
            'user_id': user_data.data.get('data').get('user_id'),
            'new_password': 'testpassword1',
            'otp': '000000'
        }
        response = client.patch(self.url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_forgot_password_api_without_otp(self, user_data):
        data = {
            'user_id': user_data.data.get('data').get('user_id'),
            'new_password': 'testpassword1',
            'confirm_password': 'testpassword1',
        }
        response = client.patch(self.url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_forgot_password_api_empty_json_body(self, user_data):
        data = {}
        response = client.patch(self.url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
