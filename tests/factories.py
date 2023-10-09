import factory
import secrets

from django.utils import timezone

from users.models import User
from rooms.models import Room, Amenity
from experiences.models import Experience, Perk
from categories.models import Category
from reviews.models import Review
from wishlists.models import Wishlist
from direct_messages.models import ChattingRoom, Message
from medias.models import Photo


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
    city = "uiwang"
    price = 89000
    rooms = 1
    toilets = 1
    description = None
    address = "23 Poilsegeori-ro, Uiwang-si, Gyeonggi-do"
    pet_friendly = False
    kind = "entire_place"
    user = factory.SubFactory(UserFactory)
    category = None

    class Meta:
        model = Room


class AmenityFactory(factory.django.DjangoModelFactory):
    name = "Write Python TestCode~~"
    description = None

    class Meta:
        model = Amenity


class PerkFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: f"Test Perk - {n}")
    detail = "Test Perk detail"
    description = "Test Perk description"

    class Meta:
        model = Perk


class ExperienceFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: f"Test Experience - {n}")
    description = "Test Experience description"
    country = "korea"
    city = "uiwang"
    price = 85000
    address = "23 Poilsegeori-ro, Uiwang-si, Gyeonggi-do"
    started_at = timezone.now()
    finished_at = timezone.now()
    user = factory.SubFactory(UserFactory)
    category = None

    class Meta:
        model = Experience


class CategoryFactory(factory.django.DjangoModelFactory):
    name = "Test Rooms Category"
    kind = "rooms"

    class Meta:
        model = Category


class ReviewFactory(factory.django.DjangoModelFactory):
    payload = "Test Review"
    rating = 4
    user = factory.SubFactory(UserFactory)
    room = None
    experience = None

    class Meta:
        model = Review


class WishlistFactory(factory.django.DjangoModelFactory):
    name = "Test Wishlist"
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = Wishlist


class ChattingRoomFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ChattingRoom


class MessageFactory(factory.django.DjangoModelFactory):
    text = "test message"
    user = factory.SubFactory(UserFactory)
    chatting_room = factory.SubFactory(ChattingRoomFactory)

    class Meta:
        model = Message


class PhotoFactory(factory.django.DjangoModelFactory):
    file = "https://example.com"
    description = "test photo factory"
    room = factory.SubFactory(RoomFactory)

    class Meta:
        model = Photo
