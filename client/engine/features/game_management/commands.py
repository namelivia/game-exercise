from typing import TYPE_CHECKING
from client.engine.primitives.command import Command
from .events import (
    ErrorCreatingGameEvent,
    ErrorJoiningGameEvent,
    JoinExistingGameEvent,
    CreateAGameNetworkRequestEvent,
    JoinAGameNetworkRequestEvent,
    NewGameRequestEvent,
)

if TYPE_CHECKING:
    from client.engine.general_state.profile.profile import Profile
    from client.engine.general_state.queue import Queue
    from uuid import UUID


class CreateAGame(Command):
    def __init__(self, profile: "Profile", queue: "Queue", new_game_name: str):
        super().__init__(profile, queue, f"Create a new game called {new_game_name}")
        self.events = [CreateAGameNetworkRequestEvent(new_game_name)]


class JoinAGame(Command):
    def __init__(self, profile: "Profile", queue: "Queue", game_id: "UUID"):
        super().__init__(profile, queue, f"Join game {game_id}")
        self.events = [JoinAGameNetworkRequestEvent(game_id)]


class ErrorCreatingGame(Command):
    def __init__(self, profile: "Profile", queue: "Queue"):
        super().__init__(profile, queue, "Error Creating game")
        self.events = [ErrorCreatingGameEvent()]


class ErrorJoiningGame(Command):
    def __init__(self, profile: "Profile", queue: "Queue"):
        super().__init__(profile, queue, "Error Joining game")
        self.events = [ErrorJoiningGameEvent()]


class RequestGameCreation(Command):
    def __init__(self, profile: "Profile", queue: "Queue", new_game_name: str):
        super().__init__(
            profile, queue, f"Request creating a game called {new_game_name}"
        )
        self.events = [NewGameRequestEvent(new_game_name)]


class RequestJoiningAGame(Command):
    def __init__(self, profile: "Profile", queue: "Queue", game_id: "UUID"):
        super().__init__(profile, queue, f"Request joining game {game_id}")
        self.events = [JoinExistingGameEvent(game_id)]
