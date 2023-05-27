import pytest
from pytest_factoryboy import register
from factories import \
    UserFactory, RoomFactory, AmenityFactory, ExperienceFactory, PerkFactory, CategoryFactory


factories = [
    UserFactory, RoomFactory, AmenityFactory, ExperienceFactory, PerkFactory, CategoryFactory
]

for factory in factories:
    register(factory)
