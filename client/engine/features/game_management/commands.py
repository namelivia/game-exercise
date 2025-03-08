from typing import TYPE_CHECKING

from client.engine.primitives.command import Command

from .events import (
    CreateAGameNetworkRequestEvent,
    ErrorCreatingGameEvent,
    ErrorJoiningGameEvent,
    JoinAGameNetworkRequestEvent,
    JoinExistingGameEvent,
    NewGameRequestEvent,
)

if TYPE_CHECKING:
    from uuid import UUID

    from client.engine.general_state.queue import Queue


class CreateAGame(Command):
    def __init__(self, queue: "Queue", new_game_name: str):
        super().__init__(queue, f"Create a new game called {new_game_name}")
        self.events = [CreateAGameNetworkRequestEvent(new_game_name)]


class JoinAGame(Command):
    def __init__(self, queue: "Queue", game_id: "UUID"):
        super().__init__(queue, f"Join game {game_id}")
        self.events = [JoinAGameNetworkRequestEvent(game_id)]


class ErrorCreatingGame(Command):
    def __init__(self, queue: "Queue"):
        super().__init__(queue, "Error Creating game")
        self.events = [ErrorCreatingGameEvent()]


class ErrorJoiningGame(Command):
    def __init__(self, queue: "Queue"):
        super().__init__(queue, "Error Joining game")
        self.events = [ErrorJoiningGameEvent()]


class RequestGameCreation(Command):
    def __init__(self, queue: "Queue", new_game_name: str):
        super().__init__(queue, f"Request creating a game called {new_game_name}")
        self.events = [NewGameRequestEvent(new_game_name)]


class RequestJoiningAGame(Command):
    def __init__(self, queue: "Queue", game_id: "UUID"):
        super().__init__(queue, f"Request joining game {game_id}")
        self.events = [JoinExistingGameEvent(game_id)]
