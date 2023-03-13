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


@pytest.fixture(autouse=True)
def override_debug_option():
    settings.DEBUG = True


@pytest.fixture
def client():
    return APIClient()


def json_response(res):
    return json.loads(res.content)
