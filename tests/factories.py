import factory
import secrets
from users.models import User
from rooms.models import Room, Amenity


class UserFactory(factory.django.DjangoModelFactory):
    email = factory.Sequence(lambda n: f"test{n}@example.com")
    password = secrets.token_urlsafe(10)
    name = factory.Sequence(lambda n: f"Test-{n}")
    first_name = None
    last_name = None
    is_host: False
    avatar = None
    gender = "male"
    language = "kr"
    currency = "won"
    is_admin = False
    is_staff = False
    is_active = True

    class Meta:
        model = User


class RoomFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: f"Test Room - {n}")
    country = "korea"
    city = "seoul"
    price = 89000
    rooms = 1
    toilets = 1
    description = None
    address = "23 Poilsegeori-ro, Uiwang-si, Gyeonggi-do"
    pet_friendly = False
    kind = "entire_place"
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = Room


class AmenityFactory(factory.django.DjangoModelFactory):
    name = "Write Python TestCode~~"
    description = None

    class Meta:
        model = Amenity
