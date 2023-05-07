import pytest
from pytest_factoryboy import register
from factories import UserFactory, RoomFactory, AmenityFactory


register(UserFactory)
register(RoomFactory)
register(AmenityFactory)
