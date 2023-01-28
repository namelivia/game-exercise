from typing import List, Any, TYPE_CHECKING, Iterable
from abc import ABC, abstractmethod
from server.game.game import Game
from .errors import InvalidCommandError
from .persistence import Persistence
import logging
from common.messages import (
    GameInfoMessage,
    GameEventsMessage,
    PingResponseMessage,
    GameListResponseMessage,
    GameListResponseEntry,
    ChatMessageConfirmation,
    SymbolPlacedConfirmation,
)

if TYPE_CHECKING:
    from uuid import UUID

logger = logging.getLogger(__name__)

"""
These are the commands that can be received from the server.
All the commands do the following:
1 - Load game
2 - Execute game operation
3 - Save the game
4 - And return it
"""


class Command(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def debug(self) -> None:
        pass

    def execute(self) -> Any:
        self.debug()

    # Retrieve the current game from storage
    def load_game(self, game_id: str) -> Any:
        try:
            return Persistence.load_game(str(game_id))
        except FileNotFoundError:
            logger.info("Invalid game id")
            raise InvalidCommandError("Invalid game id")

    # Create a new game
    def create_game(self, name: str, player_id: "UUID") -> Game:
        return Game(name, player_id)

    def save_game(self, new_game: Game) -> None:
        Persistence.save_game(new_game)


class PlaceSymbol(Command):
    def __init__(
        self, game_id: str, event_id: str, player_id: "UUID", position: int
    ) -> None:
        self.game_id = game_id
        self.event_id = event_id
        self.player_id = player_id
        self.position = position

    @property
    def name(self) -> str:
        return "Place a symbol on the board"

    def debug(self) -> None:
        logger.info(
            f"Game {self.game_id}: Player {self.player_id} placed a symbol on {self.position}"
        )

    def execute(self) -> Any:
        super().execute()
        game = self.load_game(self.game_id)
        game.place(self.event_id, self.player_id, self.position)
        self.save_game(game)
        return SymbolPlacedConfirmation(self.event_id)


class SendChat(Command):
    def __init__(self, game_id: str, event_id: str, player_id: "UUID", message: str):
        self.game_id = game_id
        self.event_id = event_id
        self.player_id = player_id
        self.message = message

    @property
    def name(self) -> str:
        return "Send chat message"

    def debug(self) -> None:
        logger.info(
            f"Game {self.game_id}: Player {self.player_id} says: {self.message}"
        )

    def execute(self) -> Any:
        super().execute()
        game = self.load_game(self.game_id)
        game.add_chat_message(self.event_id, self.player_id, self.message)
        self.save_game(game)
        return ChatMessageConfirmation(self.event_id)


class CreateGame(Command):
    def __init__(self, game_name: str, player_id: "UUID"):
        self.game_name = game_name
        self.player_id = player_id

    @property
    def name(self) -> str:
        return "Create a new game"

    def debug(self) -> None:
        logger.info(f"Player {self.player_id} created a game called {self.game_name}")

    def execute(self) -> Any:
        super().execute()
        game = self.create_game(self.game_name, self.player_id)
        # Persist the new game on storage
        self.save_game(game)
        return GameInfoMessage(game)


class JoinGame(Command):
    def __init__(self, game_id: str, player_id: "UUID"):
        self.game_id = game_id
        self.player_id = player_id

    def name(self) -> str:
        return "Join an existing game"

    def debug(self) -> None:
        logger.info(f"Game {self.game_id}: Player {self.player_id} is joining")

    def execute(self) -> Any:
        super().execute()
        game = self.load_game(self.game_id)
        game.join(self.player_id)
        self.save_game(game)
        return GameInfoMessage(game)


class GameStatus(Command):
    def __init__(self, game_id: str, pointer: int, player_id: "UUID"):
        self.game_id = game_id
        self.pointer = pointer
        self.player_id = player_id

    def name(self) -> str:
        return "Get game status"

    def debug(self) -> None:
        logger.info(
            f"Player {self.player_id} requested info for game: {self.game_id}, pointer {self.pointer}"
        )

    def execute(self) -> Any:
        super().execute()
        game = self.load_game(self.game_id)
        game.player_can_get_status(self.player_id)
        # TODO: There is a problem here, the list of events can be too big and therefore the message be too big
        # events = game.events[self.pointer :]
        events = game.events[self.pointer : self.pointer + 3]  # Will this work??
        return GameEventsMessage(events)


class Ping(Command):
    def name(self) -> str:
        return "Ping"

    def debug(self) -> None:
        logger.info("Ping request")

    def execute(self) -> Any:
        super().execute()
        return PingResponseMessage()


class GetGameList(Command):
    @property
    def name(self) -> str:
        return "Get game list"

    def debug(self) -> None:
        logger.info("Game list request")

    def _build_index_entry_from_game(self, game_id: str) -> GameListResponseEntry:
        game = Persistence.load_game(game_id)
        return GameListResponseEntry(game)

    def _build_index_from_games(
        self, game_ids: List[str]
    ) -> List[GameListResponseEntry]:
        return [self._build_index_entry_from_game(game_id) for game_id in game_ids]

    # Retrieve the list of games current game from storage
    def get_all_games(self) -> Iterable[str]:
        return Persistence.get_all_games()

    def execute(self) -> Any:
        super().execute()
        game_ids = self.get_all_games()
        return GameListResponseMessage(self._build_index_from_games(game_ids))
