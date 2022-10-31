from django.db import models
from common.models import CommonModel
from django.conf import settings


class Booking(CommonModel):

    """Booking Model Definition"""

    class BookingKindChoices(models.TextChoices):
        ROOM = "room", "Room"
        EXPERIENCE = "experience", "Experience"

    kind = models.CharField(
        max_length=15,
        choices=BookingKindChoices.choices,
    )
    check_in = models.DateField(
        null=True,
        blank=True,
    )
    check_out = models.DateField(
        null=True,
        blank=True,
    )
    guests = models.PositiveIntegerField(
        default=1
    )
    experience_time = models.DateTimeField(
        null=True,
        blank=True,
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,
        related_name="bookings",
    )
    room = models.ForeignKey(
        "rooms.Room",
        null=True,
        blank=True,
        on_delete=models.DO_NOTHING,
        related_name="bookings",
    )
    experience = models.ForeignKey(
        "experiences.Experience",
        null=True,
        blank=True,
        on_delete=models.DO_NOTHING,
        related_name="bookings",
    )

    class Meta:
        db_table = "bookings"

    def __str__(self):
        return f"{self.kind.title()} booking for {self.user}"
