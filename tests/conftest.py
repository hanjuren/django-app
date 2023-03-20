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

    def get(self, url, data=None):
        res = self.client.get(
            url,
            data or {},
            content_type="application/json"
        )
        return {
            'response': res,
            'status_code': res.status_code,
            'json_response': json.loads(res.content),
        }

    def post(self, url, data=None, token=None):
        if token:
            self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        res = self.client.post(
            url,
            json.dumps(data),
            content_type="application/json",
        )
        return res

    # def __call__(self, http_method, url, data=None):
    #     content_type = "application/json"
    #
    #     if http_method == "get":
    #         res = self.client.get(
    #             url, {}, content_type=content_type
    #         )
    #     elif http_method == "post":
    #         res = self.client.post(
    #             url,
    #             json.dumps(data),
    #             content_type=content_type
    #         )
    #     elif http_method == "del":
    #         res = self.client.delete(
    #             url, {}, content_type=content_type
    #         )
    #     else:
    #         res = self.client.put(
    #             url,
    #             json.dumps(data),
    #             content_type=content_type
    #         )
    #     return res


@pytest.fixture
def client():
    client = APIClient()
    return ClientRequest(client)
