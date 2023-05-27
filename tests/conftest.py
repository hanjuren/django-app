import pytest
from pytest_factoryboy import register
from factories import \
    UserFactory, RoomFactory, AmenityFactory, ExperienceFactory, PerkFactory, CategoryFactory, \
    ReviewFactory


factories = [
    UserFactory, RoomFactory, AmenityFactory, ExperienceFactory, PerkFactory, CategoryFactory,
    ReviewFactory
]

for factory in factories:
    register(factory)
