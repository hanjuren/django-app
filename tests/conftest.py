import pytest
import json
from django.conf import settings
from rest_framework.test import APIClient
from pytest_factoryboy import register
from .factories import UserFactory, RoomFactory, CategoryFactory, AmenityFactory, ReviewFactory


register(UserFactory)
register(RoomFactory)
register(CategoryFactory)
register(AmenityFactory)
register(ReviewFactory)


@pytest.fixture
def override_debug_option():
    settings.DEBUG = True


class ClientRequest:
    def __init__(self, client):
        self.client = client

    def get(self, url, data=None, token=''):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
        params = {}
        if data:
            params.update(json.dumps(data))

        res = self.client.get(
            url,
            params,
            content_type="application/json",
        )
        return res

    def post(self, url, data=None, token=None):
        if token:
            self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        res = self.client.post(
            url,
            json.dumps(data),
            content_type="application/json",
        )
        return res

    def put(self, url, data=None, token=None):
        if token:
            self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        res = self.client.put(
            url,
            json.dumps(data),
            content_type="application/json"
        )
        return res

    def delete(self, url, data=None, token=None):
        if token:
            self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        res = self.client.delete(
            url,
            json.dumps(data),
            content_type="application/json",
        )
        return res


@pytest.fixture
def client():
    client = APIClient()
    return ClientRequest(client)
