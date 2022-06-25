from unittest import TestCase
from client.events import UserTypedEvent
from client.events import (
    GameCreatedInGameEvent,
    PlayerJoinedInGameEvent,
    PlayerPlacedSymbolInGameEvent,
)
from client.game.screens.in_game.in_game import InGame
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

    @mock.patch("client.game.commands.RequestPlaceASymbol")
    def test_user_places_a_symbol_on_the_board(self, m_place_a_symbol):
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
            [
                "player_1_id",
                "player_2_id",
            ],
        )
        screen._advance_event_pointer()
        # Assert the command has been issued

    def test_player_has_placed_a_symbol(self):
        # When a player has placed a symbol on the board music plays
        screen = InGame(
            mock.Mock(),
            [PlayerPlacedSymbolInGameEvent("player_1_id", 5)],
            "some_game_id",
            "some_game_name",
            [
                "player_1_id",
                "player_2_id",
            ],
        )
        screen._advance_event_pointer()
        # Assert the command has been issued
