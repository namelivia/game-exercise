from unittest import TestCase
from client.engine.features.user_input.events import UserTypedEvent
from client.engine.features.chat.events import (
    ChatMessageInGameEvent,
)
from client.engine.features.pieces.events import (
    PlayerPlacedSymbolInGameEvent,
    SymbolPlacedConfirmedInGameEvent,
    SymbolPlacedErroredEvent,
)
from client.engine.events import (
    GameCreatedInGameEvent,
    PlayerJoinedInGameEvent,
    PlayerWinsInGameEvent,
)
from client.game.screens.in_game.in_game import InGame
from client.engine.visual_regression.visual_regression import VisualRegression
import mock


class TestInGameScreen(TestCase):
    @mock.patch("client.game.commands.BackToLobby")
    def test_user_exits(self, m_back_to_lobby):
        # User types escape and returns to the lobby
        screen = InGame(
            mock.Mock(),
            [UserTypedEvent("escape")],
            "some_game_id",
            "some_game_name",
            [
                "player_1_id",
                "player_2_id",
            ],
        )
        screen._advance_event_pointer()
        m_back_to_lobby.assert_called_once()

    @mock.patch("client.game.screens.in_game.in_game.InGame._move_is_valid")
    @mock.patch("client.game.screens.in_game.in_game.RequestPlaceASymbol")
    def test_user_places_a_symbol_on_the_board(self, m_place_a_symbol, m_validation):
        m_validation.return_value = True
        # User presses the number 5 to request placing a symbol
        screen = InGame(
            mock.Mock(),
            [UserTypedEvent("5")],
            "some_game_id",
            "some_game_name",
            [
                "player_1_id",
                "player_2_id",
            ],
        )
        screen._advance_event_pointer()
        m_validation.assert_called_once_with(5)
        m_place_a_symbol.assert_called_once()

    def test_game_has_been_created(self):
        # When the game is created some music is played
        screen = InGame(
            mock.Mock(),
            [GameCreatedInGameEvent("player_1_id")],
            "some_game_id",
            "some_game_name",
            [
                "player_1_id",
                "player_2_id",
            ],
        )
        screen._advance_event_pointer()
        # Assert the command has been issued

    def test_player_has_joined(self):
        # When a player joins some music is played
        screen = InGame(
            mock.Mock(),
            [PlayerJoinedInGameEvent("player_2_id")],
            "some_game_id",
            "some_game_name",
            ["player_1_id"],
        )
        screen._advance_event_pointer()
        # Assert the command has been issued
        assert screen.data["players"] == [
            "player_1_id",
            "player_2_id",
        ]

    def test_player_has_placed_a_symbol(self):
        # When a player has placed a symbol on the board music plays
        screen = InGame(
            mock.Mock(),
            [PlayerPlacedSymbolInGameEvent("player_1_id", 5, "OK")],
            "some_game_id",
            "some_game_name",
            [
                "player_1_id",
                "player_2_id",
            ],
        )
        screen._advance_event_pointer()
        # Assert the command has been issued

    def test_in_game(self):
        self.client_state = mock.Mock()
        self.client_state.clock.get.return_value = 0  # Initial time is 0
        self.in_game = InGame(
            self.client_state,
            [],
            "some_game_id",
            "some_game_name",
            ["player_1_id"],
        )

        # Empty screen
        VisualRegression.assert_matches_snapshot(
            self.in_game,
            "./client/game/screens/in_game/tests/screenshots/in_game_start.png",
        )

        # Player 2 joins the game
        self.in_game.update(
            PlayerJoinedInGameEvent(player_id="player_2_id"),
        )

        VisualRegression.assert_matches_snapshot(
            self.in_game,
            "./client/game/screens/in_game/tests/screenshots/in_game_player_2_joins.png",
        )

        # A chat message comes
        self.in_game.update(
            ChatMessageInGameEvent(
                player_id="player_2_id", message="good luck", confirmation="OK"
            ),
        )

        VisualRegression.assert_matches_snapshot(
            self.in_game,
            "./client/game/screens/in_game/tests/screenshots/in_game_chat_message.png",
        )

        placement_event = PlayerPlacedSymbolInGameEvent(
            player_id="player_1_id", position=0, confirmation="pending"
        )
        # Player 1 places symbol
        self.in_game.update(placement_event)

        VisualRegression.assert_matches_snapshot(
            self.in_game,
            "./client/game/screens/in_game/tests/screenshots/in_game_movement_1_pending.png",
        )

        # Player 1 placement is confirmed
        self.in_game.update(
            SymbolPlacedConfirmedInGameEvent(placement_event.id),
        )

        VisualRegression.assert_matches_snapshot(
            self.in_game,
            "./client/game/screens/in_game/tests/screenshots/in_game_movement_1_confirmed.png",
        )

        # Player 2 places symbol
        self.in_game.update(
            PlayerPlacedSymbolInGameEvent(
                player_id="player_2_id", position=1, confirmation="OK"
            ),
        )

        VisualRegression.assert_matches_snapshot(
            self.in_game,
            "./client/game/screens/in_game/tests/screenshots/in_game_movement_2.png",
        )

        # Player 1 places symbol
        self.in_game.update(
            PlayerPlacedSymbolInGameEvent(
                player_id="player_1_id", position=3, confirmation="OK"
            ),
        )

        VisualRegression.assert_matches_snapshot(
            self.in_game,
            "./client/game/screens/in_game/tests/screenshots/in_game_movement_3.png",
        )

        # Player 2 places symbol
        self.in_game.update(
            PlayerPlacedSymbolInGameEvent(
                player_id="player_2_id", position=6, confirmation="OK"
            ),
        )

        VisualRegression.assert_matches_snapshot(
            self.in_game,
            "./client/game/screens/in_game/tests/screenshots/in_game_movement_4.png",
        )

        # Player attempts to place in a bad position
        bad_move = PlayerPlacedSymbolInGameEvent(
            player_id="player_1_id", position=6, confirmation="pending"
        )
        self.in_game.update(bad_move)

        VisualRegression.assert_matches_snapshot(
            self.in_game,
            "./client/game/screens/in_game/tests/screenshots/in_game_bad_movement.png",
        )

        # The movement is rejected by the server and rolled back

        self.in_game.update(
            SymbolPlacedErroredEvent(place_symbol_event_id=bad_move.id),
        )

        VisualRegression.assert_matches_snapshot(
            self.in_game,
            "./client/game/screens/in_game/tests/screenshots/in_game_bad_movement_rollback.png",
        )

        # Player 1 places symbol
        self.in_game.update(
            PlayerPlacedSymbolInGameEvent(
                player_id="player_1_id", position=4, confirmation="OK"
            ),
        )

        VisualRegression.assert_matches_snapshot(
            self.in_game,
            "./client/game/screens/in_game/tests/screenshots/in_game_movement_5.png",
        )

        # Player 2 places symbol
        self.in_game.update(
            PlayerPlacedSymbolInGameEvent(
                player_id="player_2_id", position=2, confirmation="OK"
            ),
        )

        VisualRegression.assert_matches_snapshot(
            self.in_game,
            "./client/game/screens/in_game/tests/screenshots/in_game_movement_6.png",
        )

        # Player 1 places symbol
        self.in_game.update(
            PlayerPlacedSymbolInGameEvent(
                player_id="player_1_id", position=7, confirmation="OK"
            ),
        )

        VisualRegression.assert_matches_snapshot(
            self.in_game,
            "./client/game/screens/in_game/tests/screenshots/in_game_movement_7.png",
        )

        # Player 2 places symbol
        self.in_game.update(
            PlayerPlacedSymbolInGameEvent(
                player_id="player_2_id", position=5, confirmation="OK"
            ),
        )

        VisualRegression.assert_matches_snapshot(
            self.in_game,
            "./client/game/screens/in_game/tests/screenshots/in_game_movement_8.png",
        )

        # Player 1 places symbol
        self.in_game.update(
            PlayerPlacedSymbolInGameEvent(
                player_id="player_1_id", position=8, confirmation="OK"
            ),
        )

        VisualRegression.assert_matches_snapshot(
            self.in_game,
            "./client/game/screens/in_game/tests/screenshots/in_game_movement_9.png",
        )

        # Player 1 wins
        self.in_game.update(
            PlayerWinsInGameEvent(player_id="player_1_id"),
        )

        VisualRegression.assert_matches_snapshot(
            self.in_game,
            "./client/game/screens/in_game/tests/screenshots/player_wins.png",
        )

        # Player focuses chat
        self.in_game.update(UserTypedEvent("t"))

        VisualRegression.assert_matches_snapshot(
            self.in_game,
            "./client/game/screens/in_game/tests/screenshots/in_game_chat_focused.png",
        )

        # Player types
        self.in_game.update(UserTypedEvent("g"))
        self.in_game.update(UserTypedEvent("g"))
        self.in_game.update(UserTypedEvent(" "))
        self.in_game.update(UserTypedEvent("b"))
        self.in_game.update(UserTypedEvent("r"))
        self.in_game.update(UserTypedEvent("e"))
        self.in_game.update(UserTypedEvent("backspace"))
        self.in_game.update(UserTypedEvent("o"))

        VisualRegression.assert_matches_snapshot(
            self.in_game,
            "./client/game/screens/in_game/tests/screenshots/in_game_chat_input.png",
        )

        # The chat message is displayed
        self.in_game.update(UserTypedEvent("return"))

        # TODO: Assert that the event has been sourced here.

        self.in_game.update(
            ChatMessageInGameEvent(
                player_id="player_1_id", message="gg bro", confirmation="OK"
            ),
        )

        VisualRegression.assert_matches_snapshot(
            self.in_game,
            "./client/game/screens/in_game/tests/screenshots/in_game_chat_response.png",
        )

        # Chat unfocused

        self.in_game.update(UserTypedEvent("escape"))

        VisualRegression.assert_matches_snapshot(
            self.in_game,
            "./client/game/screens/in_game/tests/screenshots/in_game_chat_unfocused.png",
        )

    def test_many_chat_messages(self):
        self.client_state = mock.Mock()
        self.client_state.clock.get.return_value = 0  # Initial time is 0
        self.in_game = InGame(
            self.client_state,
            [],
            "some_game_id",
            "some_game_name",
            ["player_1_id", "player_2_id"],
        )

        # Focus chat to check positioning
        self.in_game.update(UserTypedEvent("t"))

        # Many chat messages come
        self.in_game.update(
            ChatMessageInGameEvent(
                player_id="player_1_id", message="message 1", confirmation="OK"
            ),
        )
        self.in_game.update(
            ChatMessageInGameEvent(
                player_id="player_1_id", message="message 2", confirmation="OK"
            ),
        )
        self.in_game.update(
            ChatMessageInGameEvent(
                player_id="player_1_id", message="message 3", confirmation="OK"
            ),
        )
        self.in_game.update(
            ChatMessageInGameEvent(
                player_id="player_1_id", message="message 4", confirmation="OK"
            ),
        )
        self.in_game.update(
            ChatMessageInGameEvent(
                player_id="player_1_id", message="message 5", confirmation="OK"
            ),
        )
        self.in_game.update(
            ChatMessageInGameEvent(
                player_id="player_1_id", message="message 6", confirmation="OK"
            ),
        )
        self.in_game.update(
            ChatMessageInGameEvent(
                player_id="player_1_id", message="message 7", confirmation="OK"
            ),
        )
        self.in_game.update(
            ChatMessageInGameEvent(
                player_id="player_1_id", message="message 8", confirmation="OK"
            ),
        )
        self.in_game.update(
            ChatMessageInGameEvent(
                player_id="player_1_id", message="message 9", confirmation="OK"
            ),
        )
        self.in_game.update(
            ChatMessageInGameEvent(
                player_id="player_1_id", message="message 10", confirmation="OK"
            ),
        )

        VisualRegression.assert_matches_snapshot(
            self.in_game,
            "./client/game/screens/in_game/tests/screenshots/many_chat_messages.png",
        )
