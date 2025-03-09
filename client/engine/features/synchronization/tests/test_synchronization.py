from unittest import TestCase

import mock

from client.engine.event_handler import EventHandler
from client.engine.features.synchronization.commands import (
    ProcessServerEvents,
    RefreshGameStatus,
    RequestGameStatus,
    UpdateGame,
)
from client.engine.features.synchronization.events import (
    RefreshGameStatusEvent,
    RefreshGameStatusNetworkRequestEvent,
    UpdateGameEvent,
)
from client.engine.general_state.queue import Queue
from common.messages import GameEventsMessage, GetGameStatus


class TestSynchronization(TestCase):
    def setUp(self):
        self.profile = mock.Mock()
        self.queue = Queue()
        self.event_handler = EventHandler()

    @mock.patch("client.engine.event_handler.Channel.send_command")
    @mock.patch("client.engine.features.synchronization.event_handler.UpdateGame")
    def test_refreshing_the_game_status_sucess(self, m_update, m_send_command):
        # The command is invoked
        RefreshGameStatus("game_id", 5).execute()

        event = self.queue.pop()
        assert isinstance(event, RefreshGameStatusNetworkRequestEvent)
        assert event.game_id == "game_id"
        assert event.pointer == 5

        # profile = self.profile
        self.profile.id = "player_id"
        # queue = self.queue

        # The response will be sucessful
        event_1 = mock.Mock()
        event_2 = mock.Mock()
        m_send_command.return_value = GameEventsMessage([event_1, event_2])
        self.event_handler.handle(event)

        # Assert the payload has been correctly sent.
        m_send_command.assert_called_once()
        request_message = m_send_command.call_args.args[0]
        assert isinstance(request_message, GetGameStatus)
        assert request_message.game_id == "game_id"
        assert request_message.pointer == 5
        assert request_message.player_id == "player_id"

        # Assert that the confirmation command gets called
        m_update.assert_called_once_with([event_1, event_2])

    # TODO: Currently I'm not doing anything if this request fails, and I'm not testing it either

    @mock.patch(
        "client.engine.features.synchronization.event_handler.RefreshGameStatus"
    )
    def test_requesting_the_game_status(self, m_refresh_command):
        # The command is invoked
        RequestGameStatus("game_id", 3).execute()

        event = self.queue.pop()
        assert isinstance(event, RefreshGameStatusEvent)
        assert event.game_id == "game_id"
        assert event.pointer == 3

        # profile = self.profile
        # queue = self.queue

        self.event_handler.handle(event)

        m_refresh_command.assert_called_once_with("game_id", 3)

    def test_processing_server_events(self):
        # This one is very special! It just passing all its events to the queue
        event_1 = mock.Mock()
        event_2 = mock.Mock()
        # The command is invoked
        ProcessServerEvents([event_1, event_2]).execute()

        assert self.queue.pop() == event_1
        assert self.queue.pop() == event_2

    @mock.patch(
        "client.engine.features.synchronization.event_handler.ProcessServerEvents"
    )
    def test_updating_game(self, m_process_events):
        event_1 = mock.Mock()
        event_2 = mock.Mock()
        # The command is invoked
        UpdateGame([event_1, event_2]).execute()

        event = self.queue.pop()
        assert isinstance(event, UpdateGameEvent)
        assert event.events == [event_1, event_2]

        # profile = self.profile
        # queue = self.queue
        # profile.game_event_pointer = 4

        self.event_handler.handle(event)

        # The game event pointer is updated to include these new events
        # profile.set_game_event_pointer.assert_called_once_with(6)
        m_process_events.assert_called_once_with([event_1, event_2])
