from django.db import models


class Room(models.Model):
    class KindChoices(models.TextChoices):
        ENTIRE_PLACE = ("entire_place", "Entire Place")
        PRIVATE_PLACE = ("private_place", "Private Place")
        SHARED_ROOM = ("shared_room", "Shared Room")

    name = models.CharField(max_length=250)
    country = models.CharField(max_length=50, default="korea")
    city = models.CharField(max_length=80, default='seoul')
    price = models.PositiveIntegerField()
    rooms = models.PositiveIntegerField()
    toilets = models.PositiveIntegerField()
    description = models.TextField(null=True)
    address = models.CharField(max_length=250)
    pet_friendly = models.BooleanField(default=False)
    kind = models.CharField(choices=KindChoices.choices)
    user = models.ForeignKey(
        "users.User",
        related_name="user",
        db_column="user_id",
        on_delete=models.CASCADE,
    )
    amenities = models.ManyToManyField(
        "rooms.Amenity",
        related_name="amenities",
        db_table="room_amenities"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        db_table = "rooms"


class Amenity(models.Model):
    name = models.CharField(max_length=150)
    description = models.CharField(max_length=150, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        db_table = "amenities"
        verbose_name_plural = "Amenities"
