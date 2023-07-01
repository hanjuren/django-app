import pytest
from direct_messages.models import ChattingRoom


pytestmark = pytest.mark.django_db


class TestChattingRoom:
    def test_str(self):
        chatting_room = ChattingRoom()
        assert str(chatting_room) == "Chatting Room"
