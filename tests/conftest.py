import pytest
from pytest_factoryboy import register
from factories import \
    UserFactory, RoomFactory, AmenityFactory, ExperienceFactory, PerkFactory, CategoryFactory, \
    ReviewFactory, WishlistFactory


factories = [
    UserFactory, RoomFactory, AmenityFactory, ExperienceFactory, PerkFactory, CategoryFactory,
    ReviewFactory, WishlistFactory
]

for factory in factories:
    register(factory)
