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
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password': 'testpassword',
        'confirm_password': 'testpassword'
    }
    response = client.post(url, data)

    return response
