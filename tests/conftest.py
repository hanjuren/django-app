import pytest
from pytest_factoryboy import register
from factories import \
    UserFactory, RoomFactory, AmenityFactory, ExperienceFactory, PerkFactory


factories = [
    UserFactory, RoomFactory, AmenityFactory, ExperienceFactory, PerkFactory,
]

for factory in factories:
    register(factory)
