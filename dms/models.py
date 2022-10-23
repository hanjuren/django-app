from django.db import models
from common.models import CommonModel
from django.conf import settings


class ChattingRoom(CommonModel):

    """ChatRoom Model Definotion"""

    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
    )

    def __str__(self):
        return "Chatting Room"


class Message(CommonModel):

    """Message Modle Definition"""

    text = models.TextField()
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
    )
    room = models.ForeignKey(
        'dms.ChattingRoom',
        on_delete=models.CASCADE,
    )

    class Meta:
        db_table = "messages"

    def __str__(self):
        return f"{self.user} says: {self.text}"
