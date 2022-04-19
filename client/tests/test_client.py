from unittest import TestCase
from client.general_state.queue import Queue
from client.general_state.profile.profile import Profile
from client.event_handler import EventHandler
from client.events import (
    UserTypedEvent,
    QuitGameEvent,
    UpdateGameEvent,
    JoinExistingGameEvent,
    NewGameRequestEvent,
    InitiateGameEvent,
    CreateAGameNetworkRequestEvent,
    JoinAGameNetworkRequestEvent,
    RefreshGameStatusEvent,
    RefreshGameStatusNetworkRequestEvent
)
from client.commands import (
    QuitGame,
    UserTyped,
    UpdateGame,
    InitiateGame,
    GameCreatedCommand,
    PlayerJoinedCommand,
    PlayerPlacedSymbolCommand,
    RequestGameStatus,
    RequestJoiningAGame,
    RequestGameCreation,
)
from common.messages import (
    GameMessage
)
from client.game_data import GameData
import mock


class TestClient(TestCase):
    def setUp(self):
        self.profile = mock.Mock()
        self.queue = Queue()
        self.event_handler = EventHandler()

    # These are tests for a flow Command => Event => Handler. Would I want to test handlers individually?
    @mock.patch("pygame.quit")
    @mock.patch("sys.exit")
    def test_quitting_the_game(self, m_exit, m_pygame_quit):
        QuitGame(self.profile, self.queue).execute()
        event = self.queue.pop()  # TODO: Manage the case of commands that queue several events
        assert isinstance(event, QuitGameEvent)
        client_state = mock.Mock()  # TODO: I don't like I have to define this
        self.event_handler.handle(event, client_state)
        m_pygame_quit.assert_called_once_with()
        m_exit.assert_called_once_with()

    def test_user_typing(self):
        UserTyped(self.profile, self.queue,  "f").execute()
        event = self.queue.pop()  # TODO: Manage the case of commands that queue several events
        assert isinstance(event, UserTypedEvent)
        assert event.key == "f"
        # There is no generic handler for this one, it is handled by the game on each screen

    def test_updating(self):
        # When there are new events to process these will be pushed to the queue
        already_processed_events = [
            "event_1"
        ]
        game_events = [
            "event_1",
            "event_2",
            "event_3",
        ]
        profile = Profile(
            'id',
            'name',
            'game_id',
            len(already_processed_events) - 1
        )
        UpdateGame(profile, self.queue, game_events).execute()
        event = self.queue.pop()  # TODO: Manage the case of commands that queue several events
        assert isinstance(event, UpdateGameEvent)

        client_state = mock.Mock()  # TODO: I don't like I have to define this
        client_state.profile = profile
        client_state.queue = self.queue
        self.event_handler.handle(event, client_state)

        # Unprocessed events have been calculated and pushed to the queue
        unprocessed_event_1 = self.queue.pop()
        assert unprocessed_event_1 == "event_2"
        unprocessed_event_1 = self.queue.pop()
        assert unprocessed_event_1 == "event_3"
        assert client_state.profile.game_event_pointer == 2  # And the event pointer has been updated

    def test_initializating_game(self):
        game_data = GameData(
            "some_game_id",
            "some_game_name",
            "player_1_id",
            "player_2_id",
        )

        profile = Profile(
            'id',
            'name',
            None,  # Internal game id is not set
            0
        )

        InitiateGame(
            self.profile,
            self.queue,
            game_data
        ).execute()

        client_state = mock.Mock()  # TODO: I don't like I have to define this
        client_state.profile = profile

        event = self.queue.pop()  # TODO: Manage the case of commands that queue several events
        assert isinstance(event, InitiateGameEvent)  # Event to be picked up by the game logic

        event = self.queue.pop()
        self.event_handler.handle(event, client_state)
        assert client_state.profile.game_id == "some_game_id"  # The internal game id is set

    # Game events
    def test_game_created(self):
        GameCreatedCommand(self.profile, self.queue,  "some_player_id").execute()
        # TODO: Finish this test

    def test_player_joined(self):
        PlayerJoinedCommand(self.profile, self.queue,  "some_player_id").execute()
        # TODO: Finish this test

    def test_player_placed_symbol(self):
        PlayerPlacedSymbolCommand(self.profile, self.queue,  "some_player_id", 2).execute()
        # TODO: Finish this test

    @mock.patch("client.event_handler.Channel.send_command")
    def test_request_game_status_success(self, m_send_command):

        # The server will respond with a correct game message
        m_send_command.return_value = GameMessage(
            GameData(
                'game_id',
                'game_name',
                'player_1_id',
                'player_2_id',
                [
                    'event_1',
                    'event_2',
                    'event_3',
                ]
            )
        )

        # A request to get the game status is sourced
        RequestGameStatus(self.profile, self.queue,  "some_game_id").execute()
        event = self.queue.pop()  # TODO: Manage the case of commands that queue several events
        assert isinstance(event, RefreshGameStatusEvent)

        client_state = mock.Mock()  # TODO: I don't like I have to define this
        client_state.queue = self.queue
        self.event_handler.handle(event, client_state)

        # A network request to ask for the game status for the server is sent
        event = self.queue.pop()
        assert isinstance(event, RefreshGameStatusNetworkRequestEvent)
        self.event_handler.handle(event, client_state)

        # Assert the command has been correctly sent. To test the data payload that piece of code should be refactored
        m_send_command.assert_called_once()

        # An event to update the game locally is sourced
        event = self.queue.pop()
        assert isinstance(event, UpdateGameEvent)
        # And it contains the new set of events from the server
        assert event.events == ['event_1', 'event_2', 'event_3']

    @mock.patch("client.event_handler.Channel.send_command")
    def test_request_game_status_error(self, m_send_command):
        # TODO: Write this test, should source on event to be handled on the screen
        pass
        # The server will respond with a correct game message
        # m_send_command.return_value = ErrorMessage()

    @mock.patch("client.event_handler.Channel.send_command")
    def test_request_create_new_game_success(self, m_send_command):
        m_send_command.return_value = GameMessage(
            GameData(
                'game_id',
                'game_name',
                'player_1_id',
                'player_2_id',
                [
                    'event_1',
                    'event_2',
                    'event_3',
                ]
            )
        )
        RequestGameCreation(self.profile, self.queue,  "some_game_id").execute()
        event = self.queue.pop()  # TODO: Manage the case of commands that queue several events
        assert isinstance(event, NewGameRequestEvent)

        # Handle the event
        client_state = mock.Mock()  # TODO: I don't like I have to define this
        client_state.queue = self.queue
        self.event_handler.handle(event, client_state)

        # A network request to ask for the game initialization on the server is sent
        event = self.queue.pop()
        assert isinstance(event, CreateAGameNetworkRequestEvent)
        self.event_handler.handle(event, client_state)

        # Assert the command has been correctly sent. To test the data payload that piece of code should be refactored
        m_send_command.assert_called_once()

        # An event to initalize the game locally is sourced
        event = self.queue.pop()
        assert isinstance(event, InitiateGameEvent)

        # And it contains the data to initialize the game from the server
        assert event.game_data.__dict__ == {
            "events": [],
            "id": "game_id",
            "name": "game_name",
            "player_1_id": "player_1_id",
            "player_2_id": "player_2_id",
        }

    @mock.patch("client.event_handler.Channel.send_command")
    def test_request_create_new_game_error(self, m_send_command):
        # TODO: Write this test, should source on event to be handled on the screen
        pass
        # The server will respond with a correct game message
        # m_send_command.return_value = ErrorMessage()

    @mock.patch("client.event_handler.Channel.send_command")
    def test_request_join_a_game_success(self, m_send_command):
        m_send_command.return_value = GameMessage(
            GameData(
                'game_id',
                'game_name',
                'player_1_id',
                'player_2_id',
                [
                    'event_1',
                    'event_2',
                    'event_3',
                ]
            )
        )
        RequestJoiningAGame(self.profile, self.queue,  "some_game_id").execute()
        event = self.queue.pop()  # TODO: Manage the case of commands that queue several events
        assert isinstance(event, JoinExistingGameEvent)

        # Handle the event
        client_state = mock.Mock()  # TODO: I don't like I have to define this
        client_state.queue = self.queue
        self.event_handler.handle(event, client_state)

        # A network request to ask for the game initialization on the server is sent
        event = self.queue.pop()
        assert isinstance(event, JoinAGameNetworkRequestEvent)
        self.event_handler.handle(event, client_state)

        # Assert the command has been correctly sent. To test the data payload that piece of code should be refactored
        m_send_command.assert_called_once()

        # An event to initalize the game locally is sourced
        event = self.queue.pop()
        assert isinstance(event, InitiateGameEvent)

        # And it contains the data to initialize the game from the server
        assert event.game_data.__dict__ == {
            "events": [],
            "id": "game_id",
            "name": "game_name",
            "player_1_id": "player_1_id",
            "player_2_id": "player_2_id",
        }

    @mock.patch("client.event_handler.Channel.send_command")
    def test_request_join_a_game_error(self, m_send_command):
        # TODO: Write this test, should source on event to be handled on the screen
        pass
        # The server will respond with a correct game message
        # m_send_command.return_value = ErrorMessage()
