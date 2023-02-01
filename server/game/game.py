from typing import Optional, List, Tuple, Any
from server.engine.errors import InvalidCommandError
from common.events import (
    GameCreated,
    PlayerJoined,
    PlayerPlacedSymbol,
    ChatMessageEvent,
    PlayerWins,
)
from uuid import uuid4
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from uuid import UUID


"""
This implements the game state and the
operations that can be applied on them.

Currently joining a game and placing a symbol on the board.

Note that every command first validates (can be invalid).
And if valid sets something on the game state.
"""

PLAYERS_PER_GAME = 2


class Game:
    def __init__(self, name: str, player_id: "UUID"):
        self.id = uuid4()
        self.name = name
        self.board: List[Optional["UUID"]] = [
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
        ]
        self.players: List["UUID"] = [player_id]
        self.events: List[Any] = [GameCreated(player_id)]
        self.turn: "UUID" = player_id
        self.winner: Optional["UUID"] = None

    def _next_turn(self) -> "UUID":
        if self.turn == self.players[1]:
            return self.players[0]
        return self.players[1]

    def _evaluate_winning_line(self, line: Tuple[int, int, int]) -> Optional["UUID"]:
        player = None

        for position in line:
            if self.board[position] is None:  # Empty position
                return None
            if player is None:  # First time evaluation
                player = self.board[position]
            else:
                if self.board[position] != player:  # Mismatch
                    return None
        return player  # Line is a win!

    def _check_if_there_is_a_winner(self) -> Optional["UUID"]:
        winner_combinations = [  # All possible ways of winning
            (0, 1, 2),
            (3, 4, 5),
            (6, 7, 8),
            (0, 3, 6),
            (1, 4, 7),
            (2, 5, 8),
            (0, 4, 8),
            (2, 4, 6),
        ]
        for line in winner_combinations:
            winner = self._evaluate_winning_line(line)
            if winner is not None:  # There is a winner for the line
                self.events.append(PlayerWins(winner))
                return winner
        return None  # No winner yet

    def join(self, player_id: "UUID") -> None:
        if player_id not in self.players:
            if len(self.players) >= PLAYERS_PER_GAME:
                raise InvalidCommandError("The game is full")
            self.players.append(player_id)
            self.events.append(PlayerJoined(player_id))

    def player_can_get_status(self, player_id: "UUID") -> None:
        if player_id not in self.players:
            raise InvalidCommandError("Player has no access to the game")

    def place(self, event_id: "UUID", player: "UUID", position: int) -> None:
        if player not in self.players:
            raise InvalidCommandError("Player has no access to the game")
        if self.winner is not None:
            raise InvalidCommandError("The game is already finished")
        position = int(position)
        try:
            if len(self.players) < PLAYERS_PER_GAME:
                raise InvalidCommandError("No player 2 yet")
            if self.turn != player:
                raise InvalidCommandError("Not your turn")
            if self.board[position] is not None:
                raise InvalidCommandError("Position already taken")
            self.board[position] = player
            self.events.append(PlayerPlacedSymbol(event_id, player, position))
            self.turn = self._next_turn()
            self.winner = self._check_if_there_is_a_winner()
        except IndexError:
            raise InvalidCommandError("Position out of bounds")

    def add_chat_message(self, event_id: "UUID", player: "UUID", message: str) -> None:
        if player not in self.players:
            raise InvalidCommandError("Player has no access to the game")
        # Only players in the game can send chat messages
        self.events.append(ChatMessageEvent(event_id, player, message))
