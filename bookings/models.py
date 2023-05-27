from django.db import models


class Booking(models.Model):
    class BookingKindChoices(models.TextChoices):
        ROOM = ("room", "Room")
        EXPERIENCE = ("experience", "Experience")

    kind = models.CharField(max_length=15, choices=BookingKindChoices.choices)
    user = models.ForeignKey(
        "users.User",
        related_name="bookings",
        db_column="user_id",
        on_delete=models.CASCADE
    )
    room = models.ForeignKey(
        "rooms.Room",
        related_name="bookings",
        db_column="room_id",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    experience = models.ForeignKey(
        "experiences.Experience",
        related_name="bookings",
        db_column="experience_id",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    check_in_at = models.DateField(null=True, blank=True)
    check_out_at = models.DateField(null=True, blank=True)
    experience_time = models.DateTimeField(null=True, blank=True)
    guests = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.kind.title()} booking for: {self.user}"

    class Meta:
        db_table = "bookings"
