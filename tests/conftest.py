from pytest_factoryboy import register
from .factories import UserFactory, RoomFactory, CategoryFactory, AmenityFactory, ReviewFactory


register(UserFactory)
register(RoomFactory)
register(CategoryFactory)
register(AmenityFactory)
register(ReviewFactory)
