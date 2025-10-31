from unittest import TestCase

from engine.features.network.channel import Channel
from mock import Mock, patch


class TestChannel(TestCase):
    @patch("engine.network.channel.socket")
    @patch("engine.network.channel.pickle")
    def test_sending_a_message(self, m_pickle, m_socket):
        mocked_socket = Mock()
        m_pickle.dumps.return_value = "pickled_request"
        m_pickle.loads.return_value = "response"
        m_socket.socket.return_value.__enter__.return_value = mocked_socket
        mocked_socket.recv.return_value = "pickled_response"
        message = "request"
        response = Channel.send_command(message)
        mocked_socket.connect.assert_called_once_with(("localhost", 1234))
        mocked_socket.sendall.assert_called_once_with("pickled_request")
        m_pickle.loads.assert_called_once_with("pickled_response")
        assert response == "response"

    @patch("engine.network.channel.socket")
    @patch("engine.network.channel.pickle")
    def test_server_not_reachable(self, m_pickle, m_socket):
        mocked_socket = Mock()
        m_socket.socket.return_value.__enter__.return_value = mocked_socket
        mocked_socket.connect.side_effect = ConnectionRefusedError("No route to host")
        message = "request"
        response = Channel.send_command(message)
        assert response is None

    @patch("engine.network.channel.socket")
    @patch("engine.network.channel.pickle")
    def test_malformed_reponse(self, m_pickle, m_socket):
        mocked_socket = Mock()
        m_pickle.dumps.return_value = "pickled_request"
        m_pickle.loads.side_effect = EOFError("Malformed response")
        m_socket.socket.return_value.__enter__.return_value = mocked_socket
        mocked_socket.recv.return_value = "pickled_response"
        message = "request"
        response = Channel.send_command(message)
        mocked_socket.connect.assert_called_once_with(("localhost", 1234))
        mocked_socket.sendall.assert_called_once_with("pickled_request")
        m_pickle.loads.assert_called_once_with("pickled_response")
        assert response is None
