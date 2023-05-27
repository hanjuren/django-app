import pytest
from pytest_factoryboy import register
from django.utils import timezone
from datetime import timedelta

from factories import \
    UserFactory, RoomFactory, AmenityFactory, ExperienceFactory, PerkFactory, CategoryFactory, \
    ReviewFactory, WishlistFactory

from bookings.models import Booking


factories = [
    UserFactory, RoomFactory, AmenityFactory, ExperienceFactory, PerkFactory, CategoryFactory,
    ReviewFactory, WishlistFactory
]

for factory in factories:
    register(factory)


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
