from django.db import models


class Wishlist(models.Model):
    name = models.CharField(max_length=150)
    rooms = models.ManyToManyField(
        "rooms.Room",
        related_name="wishlists",
        db_table="wishlist_rooms",
    )
    experiences = models.ManyToManyField(
        "experiences.Experience",
        related_name="wishlists",
        db_table="wishlist_experiences"
    )
    user = models.ForeignKey(
        "users.User",
        related_name="wishlists",
        db_column="user_id",
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        db_table = "wishlists"
