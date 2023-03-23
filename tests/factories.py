import secrets
import factory
from reviews.models import Review
from users.models import User
from rooms.models import Room, Amenity
from categories.models import Category


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = "test@gmail.com"
    password = secrets.token_urlsafe(10)
    username = factory.Sequence(lambda n: f"Test User - {n}")
    is_staff = True
    is_active = True
    first_name = "Py"
    last_name = "Test"
    name = "pyt"
    is_host = False
    gender = "male"
    language = "kr"
    currency = "won"


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = "test category"
    kind = "rooms"


class RoomFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Room

    name = factory.Sequence(lambda n: f"Test Room - {n}")
    country = "한국"
    city = "서울특별시"
    price = 120000
    rooms = 2
    toilets = 1
    description = "Test Room 입니다."
    address = "서울특별시 강남구 서초동"
    pet_friendly = True
    kind = "entire_place"
    owner = factory.SubFactory(UserFactory)
    category = factory.SubFactory(CategoryFactory)

    # @factory.post_generation
    # def amenities(self, create, extracted, **kwargs):
    #     print(create)
    #     if not create:
    #         # Simple build, do nothing.
    #         return
    #
    #     if extracted:
    #         # A list of groups were passed in, use them
    #         for amenity in extracted:
    #             self.amenities.add(amenity)


class AmenityFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Amenity

    name = "Write Python TestCode~~"
    description = None


class ReviewFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Review

    payload = "Test Review Payload"
    rating = 4
