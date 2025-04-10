from unittest import TestCase

import mock

from client.engine.commands import (
    GameCreatedInGameCommand,
    InitiateGame,
    PingTheServer,
    PlayerJoinedInGameCommand,
    PlayerWinsInGameCommand,
    QuitGame,
    SetPlayerName,
)
from client.engine.event_handler import EventHandler
from client.engine.events import (
    InitiateGameEvent,
    PingNetworkRequestEvent,
    QuitGameEvent,
    SetPlayerNameEvent,
)
from client.engine.features.game_list.commands import UpdateGameList
from client.engine.features.game_list.events import UpdateGameListEvent
from client.engine.features.game_management.commands import (
    RequestGameCreation,
    RequestJoiningAGame,
)
from client.engine.features.game_management.events import (
    CreateAGameNetworkRequestEvent,
    JoinAGameNetworkRequestEvent,
    JoinExistingGameEvent,
    NewGameRequestEvent,
)
from client.engine.features.sound.events import PlaySoundEvent
from client.engine.features.synchronization.commands import (
    RequestGameStatus,
    UpdateGame,
)
from client.engine.features.synchronization.events import (
    RefreshGameStatusEvent,
    RefreshGameStatusNetworkRequestEvent,
    UpdateGameEvent,
)
from client.engine.features.user_input.commands import UserTyped
from client.engine.features.user_input.events import UserTypedEvent
from client.engine.general_state.profile.profile import Profile
from client.engine.general_state.profile_manager import ProfileManager
from client.engine.general_state.queue import Queue
from common.game_data import GameData
from common.messages import (
    GameEventsMessage,
    GameInfoMessage,
    PingRequestMessage,
    PingResponseMessage,
)


class TestClient(TestCase):
    @mock.patch("client.engine.general_state.profile_manager.Persistence")
    def _initialize_test_profile(self, m_persistence):
        m_persistence.load.return_value = Profile(
            key="test_profile",
            id="player_id",
            game_id="game_id",
            game_event_pointer=None,
        )
        ProfileManager().set_profile("test_profile")

    def _initialize_test_queue(self):
        Queue().initialize(None)

    def setUp(self):
        self._initialize_test_queue()
        self._initialize_test_profile()
        self.event_handler = EventHandler()

    # These are tests for a flow Command => Event => Handler. Would I want to test handlers individually?
    @mock.patch("pygame.quit")
    @mock.patch("sys.exit")
    def test_quitting_the_game(self, m_exit, m_pygame_quit):
        QuitGame().execute()
        event = (
            Queue().pop()
        )  # TODO: Manage the case of commands that queue several events
        assert isinstance(event, QuitGameEvent)
        self.event_handler.handle(event)
        m_pygame_quit.assert_called_once_with()
        m_exit.assert_called_once_with()

    def test_user_typing(self):
        UserTyped("f").execute()
        event = (
            Queue().pop()
        )  # TODO: Manage the case of commands that queue several events
        assert isinstance(event, UserTypedEvent)
        assert event.key == "f"
        # There is no generic handler for this one, it is handled by the game on each screen

    @mock.patch("client.engine.general_state.profile_manager.Persistence")
    def test_updating(self, m_persistence):
        # There is already one processed event, so the pointer
        # will be at 1.
        game_events = [
            "event_1",
            "event_2",
            "event_3",
        ]
        m_persistence.load.return_value = Profile(
            key="key",
            id="id",
            game_id="game_id",
            game_event_pointer=1,
        )
        ProfileManager().set_profile("key")
        UpdateGame(game_events).execute()
        event = (
            Queue().pop()
        )  # TODO: Manage the case of commands that queue several events
        assert isinstance(event, UpdateGameEvent)

        self.event_handler.handle(event)

        # The server is responding with the three events
        unprocessed_event_1 = Queue().pop()
        assert unprocessed_event_1 == "event_1"
        unprocessed_event_1 = Queue().pop()
        assert unprocessed_event_1 == "event_2"
        unprocessed_event_1 = Queue().pop()
        assert unprocessed_event_1 == "event_3"
        assert (
            ProfileManager().profile.game_event_pointer == 4
        )  # And now the event pointer is at 3

    @mock.patch("client.engine.general_state.profile_manager.Persistence")
    def test_initializating_game(self, m_persistence):
        game_data = GameData(
            "some_game_id", "some_game_name", ["player_1_id", "player_2_id"]
        )

        m_persistence.load.return_value = Profile(
            key="key",
            id="id",
            game_id=None,  # Internal game id is not set
            game_event_pointer=0,
        )
        ProfileManager().set_profile("key")

        InitiateGame(game_data).execute()

        event = (
            Queue().pop()
        )  # TODO: Manage the case of commands that queue several events
        assert isinstance(event, PlaySoundEvent)

        event = (
            Queue().pop()
        )  # TODO: Manage the case of commands that queue several events
        assert isinstance(
            event, InitiateGameEvent
        )  # Event to be picked up by the game logic

        event = Queue().pop()
        self.event_handler.handle(event)
        assert (
            ProfileManager().profile.game_id == "some_game_id"
        )  # The internal game id is set

    # Game events
    def test_game_created(self):
        GameCreatedInGameCommand("some_player_id").execute()
        # TODO: Finish this test

    def test_player_joined(self):
        PlayerJoinedInGameCommand("some_player_id").execute()
        # TODO: Finish this test

    def test_player_wins(self):
        PlayerWinsInGameCommand("some_player_id").execute()
        # TODO: Finish this test

    @mock.patch("client.engine.event_handler.Channel.send_command")
    def test_request_game_status_success(self, m_send_command):
        # The server will respond with a correct game message
        m_send_command.return_value = GameEventsMessage(
            [
                "event_1",
                "event_2",
                "event_3",
            ]
        )

        # A request to get the game status is sourced
        RequestGameStatus("some_game_id", 2).execute()
        event = (
            Queue().pop()
        )  # TODO: Manage the case of commands that queue several events
        assert isinstance(event, RefreshGameStatusEvent)

        self.event_handler.handle(event)

        # A network request to ask for the game status for the server is sent
        event = Queue().pop()
        assert isinstance(event, RefreshGameStatusNetworkRequestEvent)
        self.event_handler.handle(event)

        # Assert the command has been correctly sent. To test the data payload that piece of code should be refactored
        m_send_command.assert_called_once()

        # An event to update the game locally is sourced
        event = Queue().pop()
        assert isinstance(event, UpdateGameEvent)
        # And it contains the new set of events from the server
        assert event.events == ["event_1", "event_2", "event_3"]

    @mock.patch("client.engine.event_handler.Channel.send_command")
    def test_request_game_status_error(self, m_send_command):
        # TODO: Write this test, should source on event to be handled on the screen
        pass
        # The server will respond with a correct game message
        # m_send_command.return_value = ErrorMessage()

    @mock.patch("client.engine.event_handler.Channel.send_command")
    def test_request_create_new_game_success(self, m_send_command):
        m_send_command.return_value = GameInfoMessage(
            GameData(
                "game_id",
                "game_name",
                ["player_1_id", "player_2_id"],
                [
                    "event_1",
                    "event_2",
                    "event_3",
                ],
            )
        )
        RequestGameCreation("some_game_id").execute()
        event = (
            Queue().pop()
        )  # TODO: Manage the case of commands that queue several events
        assert isinstance(event, NewGameRequestEvent)

        # Handle the event
        self.event_handler.handle(event)

        # A network request to ask for the game initialization on the server is sent
        event = Queue().pop()
        assert isinstance(event, CreateAGameNetworkRequestEvent)
        self.event_handler.handle(event)

        # Assert the command has been correctly sent. To test the data payload that piece of code should be refactored
        m_send_command.assert_called_once()

        event = (
            Queue().pop()
        )  # TODO: Manage the case of commands that queue several events
        assert isinstance(event, PlaySoundEvent)

        # An event to initalize the game locally is sourced
        event = Queue().pop()
        assert isinstance(event, InitiateGameEvent)

        # And it contains the data to initialize the game from the server
        assert event.game_data.__dict__ == {
            "events": [],
            "id": "game_id",
            "name": "game_name",
            "players": ["player_1_id", "player_2_id"],
        }

    @mock.patch("client.engine.event_handler.Channel.send_command")
    def test_request_create_new_game_error(self, m_send_command):
        # TODO: Write this test, should source on event to be handled on the screen
        pass
        # The server will respond with a correct game message
        # m_send_command.return_value = ErrorMessage()

    @mock.patch("client.engine.event_handler.Channel.send_command")
    def test_request_join_a_game_success(self, m_send_command):
        m_send_command.return_value = GameInfoMessage(
            GameData(
                "game_id",
                "game_name",
                ["player_1_id", "player_2_id"],
                [
                    "event_1",
                    "event_2",
                    "event_3",
                ],
            )
        )
        RequestJoiningAGame("some_game_id").execute()
        event = (
            Queue().pop()
        )  # TODO: Manage the case of commands that queue several events
        assert isinstance(event, JoinExistingGameEvent)

        # Handle the event
        self.event_handler.handle(event)

        # A network request to ask for the game initialization on the server is sent
        event = Queue().pop()
        assert isinstance(event, JoinAGameNetworkRequestEvent)
        self.event_handler.handle(event)

        # Assert the command has been correctly sent. To test the data payload that piece of code should be refactored
        m_send_command.assert_called_once()

        event = (
            Queue().pop()
        )  # TODO: Manage the case of commands that queue several events
        assert isinstance(event, PlaySoundEvent)

        # An event to initalize the game locally is sourced
        event = Queue().pop()
        assert isinstance(event, InitiateGameEvent)

        # And it contains the data to initialize the game from the server
        assert event.game_data.__dict__ == {
            "events": [],
            "id": "game_id",
            "name": "game_name",
            "players": ["player_1_id", "player_2_id"],
        }

    @mock.patch("client.engine.event_handler.Channel.send_command")
    def test_request_join_a_game_error(self, m_send_command):
        # TODO: Write this test, should source on event to be handled on the screen
        pass
        # The server will respond with a correct game message
        # m_send_command.return_value = ErrorMessage()

    @mock.patch("client.engine.persistence.persistence.Persistence.save")
    def test_setting_player_name(self, m_save):
        # When there are new events to process these will be pushed to the queue
        profile = Profile(
            key="key",
            id="id",
            game_id="game_id",
            game_event_pointer=0,
        )
        ProfileManager().set_profile("key")
        assert profile.name is None
        SetPlayerName("Player name").execute()
        event = (
            Queue().pop()
        )  # TODO: Manage the case of commands that queue several events
        assert isinstance(event, SetPlayerNameEvent)

        self.event_handler.handle(event)
        assert ProfileManager().profile.name == "Player name"
        # m_save.assert_called_once_with(profile, "key")
        # m_save.assert_called_once()

    @mock.patch("client.engine.event_handler.Channel.send_command")
    def test_ping_the_server_success(self, m_send_command):
        m_send_command.return_value = PingResponseMessage()

        PingTheServer().execute()
        event = (
            Queue().pop()
        )  # TODO: Manage the case of commands that queue several events
        assert isinstance(event, PingNetworkRequestEvent)

        self.event_handler.handle(event)

        # Assert the ping message has been correctly sent.
        m_send_command.assert_called_once()
        assert isinstance(m_send_command.call_args.args[0], PingRequestMessage)

    def test_updating_the_game_list(self):
        # When there are new events to process these will be pushed to the queue
        profile = Profile(
            key="key",
            id="id",
            game_id="game_id",
            game_event_pointer=0,
        )
        assert profile.name is None
        UpdateGameList(["game1", "game2", "game3"]).execute()
        event = (
            Queue().pop()
        )  # TODO: Manage the case of commands that queue several events
        assert isinstance(event, UpdateGameListEvent)
        # Event to be picked up by the game logic
