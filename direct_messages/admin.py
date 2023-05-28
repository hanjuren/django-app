from django.contrib import admin
from .models import ChattingRoom, Message


class ChattingRoomAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "created_at",
        "updated_at",
    )
    list_filter = ("created_at",)


class MessageAdmin(admin.ModelAdmin):
    list_display = (
        "text",
        "user",
        "chatting_room",
        "created_at",
        "updated_at",
    )
    list_filter = ("created_at",)


admin.site.register(ChattingRoom, ChattingRoomAdmin)
admin.site.register(Message, MessageAdmin)
