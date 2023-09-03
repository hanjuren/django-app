import json
from django.conf import settings
import pytest
from rest_framework.test import APIClient
from pytest_factoryboy import register
from django.utils import timezone
from datetime import timedelta

from factories import \
    UserFactory, RoomFactory, AmenityFactory, ExperienceFactory, PerkFactory, CategoryFactory, \
    ReviewFactory, WishlistFactory, ChattingRoomFactory, MessageFactory

from bookings.models import Booking


factories = [
    UserFactory, RoomFactory, AmenityFactory, ExperienceFactory, PerkFactory, CategoryFactory,
    ReviewFactory, WishlistFactory, ChattingRoomFactory, MessageFactory
]

for factory in factories:
    register(factory)


@pytest.fixture(autouse=True)
def override_debug_option():
    settings.DEBUG = True


class ClientRequest:
    def __init__(self, client):
        self.client = client

    def params(self, data):
        return json.dumps(data) if data else {}

    def headers(self, user=None):
        if user:
            token = user.generate_token()
            return {'HTTP_Authorization': f"Bearer {token}"}
        else:
            return {}

    def get(self, url, data=None, user=None):
        res = self.client.get(
            url,
            self.params(data),
            content_type="application/json",
            **self.headers(user),
        )
        return res

    def post(self, url, data=None, user=None, content_type="application/json"):
        if content_type == "application/json":
            params = self.params(data)
        else:
            params = data

        res = self.client.post(
            url,
            params,
            content_type=content_type,
            **self.headers(user),
        )
        return res

    def put(self, url, data=None, user=None):
        res = self.client.put(
            url,
            self.params(data),
            content_type="application/json",
            **self.headers(user),
        )
        return res

    def delete(self, url, data=None, user=None):
        res = self.client.delete(
            url,
            **self.headers(user),
        )
        return res


@pytest.fixture
def client():
    client = APIClient()
    return ClientRequest(client)


@pytest.fixture()
def create_booking():
    def _data(
            kind,
            user_id,
            guests,
            room_id=None,
            experience_id=None
    ):
        attrs = {
            'kind': kind,
            'user_id': user_id,
            'guests': guests,
            'room_id': room_id,
            'experience_id': experience_id,
        }
        if kind == 'room':
            attrs['check_in_at'] = timezone.localtime().date()
            attrs['check_out_at'] = timezone.localtime().date() + timedelta(days=1)
        else:
            attrs['experience_time'] = timezone.localtime()

        return Booking.objects.create(**attrs)
    return _data
