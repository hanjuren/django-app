from django.db import models


class ChattingRoom(models.Model):
    users = models.ManyToManyField(
        "users.User",
        related_name="chatting_rooms",
        db_table="chatting_room_users",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return "Chatting Room"

    class Meta:
        db_table = "chatting_rooms"


class Message(models.Model):
    text = models.TextField()
    user = models.ForeignKey(
        "users.User",
        related_name="messages",
        db_column="user_id",
        on_delete=models.SET_NULL,
        null=True,
    )
    chatting_room = models.ForeignKey(
        "direct_messages.ChattingRoom",
        related_name="messages",
        db_column="chatting_room_id",
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} says: {self.text}"

    class Meta:
        db_table = "messages"
