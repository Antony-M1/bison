import pytest
from rest_framework.test import APIClient
from django.urls import reverse
# from faker import Faker
from app.models import User
client = APIClient()


@pytest.fixture(name='user_data')
def create_user():
    url = reverse('sign-up')
    data = {
        'firs_name': 'Test',
        'last_name': 'User',
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password': 'testpassword',
        'confirm_password': 'testpassword'
    }
    response = client.post(url, data)

    return response


@pytest.fixture(name='login_response')
def login_api(user_data):
    user = User.objects.get(
                    user_id=str(user_data.data.get('data').get('user_id'))
                )
    user.is_verified = True
    user.save()
    url = reverse('login')
    data = {
        'username': 'testuser',
        'password': 'testpassword',
    }
    response = client.post(url, data)
    return response
