import copy
from django.urls import reverse
from rest_framework import status
import pytest
from rest_framework.test import APIClient

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