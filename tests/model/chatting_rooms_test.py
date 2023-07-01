import pytest
from direct_messages.models import ChattingRoom


pytestmark = pytest.mark.django_db


class TestChattingRoom:
    def test_str(self):
        chatting_room = ChattingRoom()
        assert str(chatting_room) == "Chatting Room"


class TestMessage:
    def test_str(self, chatting_room_factory, user_factory, message_factory):
        chatting_room = chatting_room_factory.create()
        user = user_factory.create(name="홍길동")
        message = message_factory.create(
            text="안녕하세요.",
            chatting_room=chatting_room,
            user=user,
        )

        assert str(message) == "홍길동 says: 안녕하세요."
