import pytest
from django.test import Client


@pytest.fixture
def client():
    yield Client()


def test_login_route(client):
    response = client.get('/triage/')
    assert response.status_code == 200
