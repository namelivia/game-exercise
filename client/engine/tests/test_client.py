from unittest import TestCase
from client.engine.general_state.queue import Queue
from client.engine.general_state.profile.profile import Profile
from client.engine.event_handler import EventHandler
from client.engine.events import (
    UserTypedEvent,
    SetPlayerNameEvent,
    QuitGameEvent,
    UpdateGameEvent,
    JoinExistingGameEvent,
    NewGameRequestEvent,
    InitiateGameEvent,
    CreateAGameNetworkRequestEvent,
    PingNetworkRequestEvent,
    JoinAGameNetworkRequestEvent,
    RefreshGameStatusEvent,
    RefreshGameStatusNetworkRequestEvent,
    TurnSoundOnEvent,
    TurnSoundOffEvent,
    UpdateGameListEvent,
)
from client.engine.commands import (
    QuitGame,
    UserTyped,
    UpdateGame,
    InitiateGame,
    PingTheServer,
    GameCreatedInGameCommand,
    PlayerJoinedInGameCommand,
    PlayerWinsInGameCommand,
    PlayerPlacedSymbolInGameCommand,
    RequestGameStatus,
    RequestJoiningAGame,
    RequestGameCreation,
    TurnSoundOn,
    SetPlayerName,
    TurnSoundOff,
    UpdateGameList,
)
from common.messages import (
    GameInfoMessage,
    GameEventsMessage,
    PingResponseMessage,
    PingRequestMessage,
)
from client.engine.game_data import GameData
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
        event = (
            self.queue.pop()
        )  # TODO: Manage the case of commands that queue several events
        assert isinstance(event, QuitGameEvent)
        client_state = mock.Mock()  # TODO: I don't like I have to define this
        self.event_handler.handle(event, client_state)
        m_pygame_quit.assert_called_once_with()
        m_exit.assert_called_once_with()

    @mock.patch("client.engine.persistence.persistence.Persistence.save")
    def test_turning_sound_on(self, m_save):
        profile = Profile(
            key="key",
            id="id",
            game_id="game_id",
            game_event_pointer=0,
            sound_on=False,
        )
        TurnSoundOn(self.profile, self.queue).execute()
        event = self.queue.pop()
        assert isinstance(event, TurnSoundOnEvent)
        client_state = mock.Mock()  # TODO: I don't like I have to define this
        client_state.profile = profile
        self.event_handler.handle(event, client_state)
        assert client_state.profile.sound_on is True
        m_save.assert_called_once_with(profile, "key")

    @mock.patch("client.engine.persistence.persistence.Persistence.save")
    def test_turning_sound_off(self, m_save):
        profile = Profile(
            key="key", id="id", game_id="game_id", game_event_pointer=0, sound_on=True
        )
        TurnSoundOff(self.profile, self.queue).execute()
        event = self.queue.pop()
        assert isinstance(event, TurnSoundOffEvent)
        client_state = mock.Mock()  # TODO: I don't like I have to define this
        client_state.profile = profile
        self.event_handler.handle(event, client_state)
        assert client_state.profile.sound_on is False
        m_save.assert_called_once_with(profile, "key")

    def test_user_typing(self):
        UserTyped(self.profile, self.queue, "f").execute()
        event = (
            self.queue.pop()
        )  # TODO: Manage the case of commands that queue several events
        assert isinstance(event, UserTypedEvent)
        assert event.key == "f"
        # There is no generic handler for this one, it is handled by the game on each screen

    def test_updating(self):
        # There is already one processed event, so the pointer
        # will be at 1.
        game_events = [
            "event_1",
            "event_2",
            "event_3",
        ]
        profile = Profile(
            key="key",
            id="id",
            game_id="game_id",
            game_event_pointer=1,
            sound_on=False,
        )
        UpdateGame(profile, self.queue, game_events).execute()
        event = (
            self.queue.pop()
        )  # TODO: Manage the case of commands that queue several events
        assert isinstance(event, UpdateGameEvent)

        client_state = mock.Mock()  # TODO: I don't like I have to define this
        client_state.profile = profile
        client_state.queue = self.queue
        self.event_handler.handle(event, client_state)

        # The server is responding with the three events
        unprocessed_event_1 = self.queue.pop()
        assert unprocessed_event_1 == "event_1"
        unprocessed_event_1 = self.queue.pop()
        assert unprocessed_event_1 == "event_2"
        unprocessed_event_1 = self.queue.pop()
        assert unprocessed_event_1 == "event_3"
        assert (
            client_state.profile.game_event_pointer == 4
        )  # And now the event pointer is at 3

    def test_initializating_game(self):
        game_data = GameData(
            "some_game_id", "some_game_name", ["player_1_id", "player_2_id"]
        )

        profile = Profile(
            key="key",
            id="id",
            game_id=None,  # Internal game id is not set
            game_event_pointer=0,
            sound_on=False,
        )

        InitiateGame(self.profile, self.queue, game_data).execute()

        client_state = mock.Mock()  # TODO: I don't like I have to define this
        client_state.profile = profile

        event = (
            self.queue.pop()
        )  # TODO: Manage the case of commands that queue several events
        assert isinstance(
            event, InitiateGameEvent
        )  # Event to be picked up by the game logic

        event = self.queue.pop()
        self.event_handler.handle(event, client_state)
        assert (
            client_state.profile.game_id == "some_game_id"
        )  # The internal game id is set

    # Game events
    def test_game_created(self):
        GameCreatedInGameCommand(self.profile, self.queue, "some_player_id").execute()
        # TODO: Finish this test

    def test_player_joined(self):
        PlayerJoinedInGameCommand(self.profile, self.queue, "some_player_id").execute()
        # TODO: Finish this test

    def test_player_wins(self):
        PlayerWinsInGameCommand(self.profile, self.queue, "some_player_id").execute()
        # TODO: Finish this test

    def test_player_placed_symbol(self):
        PlayerPlacedSymbolInGameCommand(
            self.profile, self.queue, "some_player_id", 2
        ).execute()
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
        RequestGameStatus(self.profile, self.queue, "some_game_id", 2).execute()
        event = (
            self.queue.pop()
        )  # TODO: Manage the case of commands that queue several events
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
        RequestGameCreation(self.profile, self.queue, "some_game_id").execute()
        event = (
            self.queue.pop()
        )  # TODO: Manage the case of commands that queue several events
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
        RequestJoiningAGame(self.profile, self.queue, "some_game_id").execute()
        event = (
            self.queue.pop()
        )  # TODO: Manage the case of commands that queue several events
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
            sound_on=False,
        )
        assert profile.name is None
        SetPlayerName(profile, self.queue, "Player name").execute()
        event = (
            self.queue.pop()
        )  # TODO: Manage the case of commands that queue several events
        assert isinstance(event, SetPlayerNameEvent)

        client_state = mock.Mock()  # TODO: I don't like I have to define this
        client_state.profile = profile
        client_state.queue = self.queue
        self.event_handler.handle(event, client_state)
        assert profile.name == "Player name"
        m_save.assert_called_once_with(profile, "key")

    @mock.patch("client.engine.event_handler.Channel.send_command")
    def test_ping_the_server_success(self, m_send_command):

        m_send_command.return_value = PingResponseMessage()

        PingTheServer(self.profile, self.queue).execute()
        event = (
            self.queue.pop()
        )  # TODO: Manage the case of commands that queue several events
        assert isinstance(event, PingNetworkRequestEvent)

        client_state = mock.Mock()  # TODO: I don't like I have to define this
        client_state.queue = self.queue
        self.event_handler.handle(event, client_state)

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
            sound_on=False,
        )
        assert profile.name is None
        UpdateGameList(profile, self.queue, ["game1", "game2", "game3"]).execute()
        event = (
            self.queue.pop()
        )  # TODO: Manage the case of commands that queue several events
        assert isinstance(event, UpdateGameListEvent)
        # Event to be picked up by the game logic
