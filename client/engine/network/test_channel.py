from unittest import TestCase
from mock import patch, Mock
from .channel import Channel


class TestChannel(TestCase):
    @patch("client.engine.network.channel.socket")
    def test_sending_a_message(self, m_socket):
        message = "some_message"
        Channel.send_command(message)
